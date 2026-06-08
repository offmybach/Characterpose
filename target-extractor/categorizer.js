// CGB Target Extractor - categorizer
// Mirrors the taxonomy in LinkedIn_connections_grouped_by_category.xlsx so
// fresh captures slot into the existing master spreadsheet without
// re-categorizing by hand.
//
// Each group declares:
//   priority: higher wins when a lead matches multiple groups
//   relevance: default Clarence Relevance for the group (High/Medium/Low)
//   reason: default Grouping Reason string used in the master CSV
//   tags: default Tags string (pipe-separated)
//   anyOf: array of regexes — any hit qualifies the group
//   requireAlso: array of regex-arrays — each inner array must have at
//                least one hit. Use for two-feature gates like
//                "kids AND money" for YouthFinLit.
//
// Match algorithm:
//   1. Score every group against the lead.
//   2. Drop Peripheral / NeedsReview if any main group matched.
//   3. Primary = highest-priority match. Secondary = the rest.
//   4. If nothing matched at all → NeedsReview.

// "Families" is too weak — financial advisors say "helping families" all
// day. KIDS requires explicit child/youth language.
const KIDS = [
  /\bkids?\b/i, /\bchildren'?s?\b/i, /\byouth\b/i,
  /\bgrade\s?(school|s)?\b/i, /\belementary\b/i, /\bK-?(5|6|8|12)\b/i,
  /\bteen(s|ager)?\b/i, /\bjuvenile\b/i,
  /\bpicture book\b/i, /kidlit/i, /parent.child/i,
];

const MONEY = [
  /financial literacy/i, /financial education/i, /financial wellness/i,
  /personal finance/i, /\bmoney\b/i, /\bfinance\b/i, /\bfinancial\b/i,
  /\bbudget(ing)?\b/i, /\bsav(ings|ing)\b/i, /\binvest(ing|ment)?\b/i,
  /\bretirement\b/i, /\bwealth\b/i, /\bfin(-?| )lit\b/i,
  /\beconom(y|ic|ics)\b/i,
];

const SCHOOL = [
  /\bschool\b/i, /\bclassroom\b/i, /\bstudent\b/i, /\bcurriculum\b/i,
  /\beducat(or|ion|ional)\b/i, /\binstructional\b/i, /\bteach(er|ing)\b/i,
  /\bdistrict\b/i, /\bISD\b/, /\bprincipal\b/i, /\bsuperintendent\b/i,
  /\bCTE\b/, /\bESL\b/, /\bELL\b/,
];

const GROUPS = [
  // ---- Publishing wins over Authors when "Publisher/Ghost Publisher" hits
  {
    name: "Publishing / Book Pros / Printers",
    priority: 102,
    relevance: "Medium",
    reason: "Useful for book production, publishing advice, reviews, or printing/channel support.",
    tags: "author/book",
    anyOf: [
      /\bpublisher\b/i, /publishing consultant/i,
      /book designer/i, /book design/i, /book editor/i,
      /editor.in.chief.*?book/i, /\bghost (writer|publisher)\b/i,
      /\btypesett(er|ing)\b/i, /\bprinter\b/i,
      /author services/i, /book production/i,
      /literary agent/i, /book marketer/i,
      /\billustration agent\b/i,
    ],
  },

  // ---- Authors above Youth FinLit: if "Author" is in the headline AND
  // there's kid-money context, the book-creator identity wins. Founders of
  // youth-money orgs (no "Author" word) still go to Youth FinLit below.
  {
    name: "Authors / Illustrators / KidLit",
    priority: 100,
    relevance: "High",
    reason: "Author/creator contact; strongest when tied to children, money, or education.",
    tags: "author/book",
    anyOf: [
      /\bauthor\b/i, /\billustrator\b/i, /author-illustrator/i,
      /kidlit/i, /children'?s? book/i, /picture book/i, /\bnovelist\b/i,
      /\bbook reviewer\b/i,
    ],
  },

  // ---- Bullseye for non-author kid-money: founders, orgs, programs ----
  {
    name: "Youth Financial Literacy",
    priority: 98,
    relevance: "High",
    reason: "Direct Clarence-adjacent audience: children's money education.",
    tags: "kids/youth|financial literacy|teacher/school",
    anyOf: [/.*/],
    requireAlso: [KIDS, MONEY],
  },

  // ---- Librarians ------------------------------------------------------
  {
    name: "Librarians / Libraries",
    priority: 92,
    relevance: "High",
    reason: "Library and reader-discovery contact for a children's financial-literacy book.",
    tags: "library",
    anyOf: [
      /librarian/i, /library media specialist/i, /media specialist/i,
      /library director/i, /youth services/i, /children'?s services/i,
      /\bstoryti?me\b/i, /\bSTEM librarian\b/i, /\bcatalog(er|ing)\b/i,
    ],
    companyAnyOf: [
      /\blibrary\b/i, /\blibraries\b/i, /library system/i, /public library/i,
    ],
  },

  // ---- EdTech / Curriculum --------------------------------------------
  {
    name: "EdTech / Curriculum / Program Design",
    priority: 90,
    relevance: "High",
    reason: "Curriculum, implementation, or educational product contact.",
    tags: "teacher/school|marketing/sales",
    anyOf: [
      /\bedtech\b/i, /ed.?tech consultant/i,
      /curriculum (designer|director|coordinator|developer|specialist)/i,
      /instructional (designer|coordinator|coach)/i,
      /learning (designer|experience)/i,
      /\bimplementation (director|lead|manager)\b/i,
      /educational (product|game|technology)/i,
      /AI in education/i, /partnerships? manager.*?educat/i,
    ],
  },

  // ---- Teachers (classroom) above FinLit Educators -------------------
  // "Teacher Professional Development | Personal Finance Educator" → Teachers,
  // because the teacher role is the dominant signal even when finlit hits too.
  {
    name: "Teachers / School Educators",
    priority: 88,
    relevance: "High",
    reason: "School/teacher channel for classroom adoption, recommendations, or educator feedback.",
    tags: "teacher/school",
    anyOf: [
      /\bteachers?\b/i, /classroom teacher/i, /elementary teacher/i,
      /\bprincipal\b/i, /assistant principal/i, /vice principal/i,
      /\binstructional coach\b/i, /reading (coach|specialist)/i,
      /literacy (coach|specialist)/i, /math (coach|specialist)/i,
      /\bCTE\b/, /business teacher/i, /personal finance teacher/i,
      /school counselor/i, /\bSPED\b/, /special education/i,
      /1st grade/i, /2nd grade/i, /3rd grade/i, /4th grade/i, /5th grade/i,
      /first grade/i, /second grade/i, /third grade/i, /fourth grade/i,
      /K-?(5|6|8|12)\b/i,
      /teacher professional development/i,
      /early childhood (lead )?educator/i,
      /(business|math|reading|literacy)\s+instructor\b/i,
      /\bKS[123]\b/i, /phase leader/i, /school governor/i,
      /\bNPQSL\b/i,
    ],
    companyAnyOf: [
      /elementary school/i, /primary school/i, /middle school/i,
      /\bISD\b/, /school district/i, /public schools/i,
      /charter school/i, /montessori/i,
    ],
  },

  // ---- FinLit Educators / Advocates ------------------------------------
  {
    name: "Financial Literacy Educators / Advocates",
    priority: 85,
    relevance: "High",
    reason: "Financial-literacy professional likely aligned with the book's mission.",
    tags: "financial literacy",
    anyOf: [
      /financial literacy/i, /financial education/i, /financial educator/i,
      /\bCFEI®?\b/i, /\bCFEd®?\b/i,
      /certified financial education/i,
      /personal finance (educator|instructor|teacher)/i,
      /money educator/i, /money coach.*?educator/i,
      /teach (money|financial)/i, /money basics/i,
      /\bfinlit\b/i, /fin-?lit/i,
      /financial engagement/i, /financial empowerment/i,
      /financial inclusion advocate/i, /financial capability/i,
      /financial well.?being/i,
      /director of education.*outreach/i,
      /director of education at (Troutwood|Banzai)/i,
      /\bDave Ramsey\b/i, /\bRamsey Solutions\b/i,
    ],
    companyAnyOf: [
      /jump\$?tart/i, /\bnefe\b/i, /next gen personal finance/i, /\bNGPF\b/,
      /council for economic education/i, /\bNFEC\b/, /financial literacy/i,
      /\bFINRA\b.*foundation/i,
      /\bTroutwood\b/i, /\bBanzai\b/i,
    ],
  },

  // ---- Academic / Researchers -----------------------------------------
  {
    name: "Academic / Researchers / Professors",
    priority: 78,
    relevance: "Medium",
    reason: "Academic credibility, research, economics/education, or expert review contact.",
    tags: "academic/research",
    anyOf: [
      /\bprofessor\b/i, /assistant professor/i, /associate professor/i,
      /\blecturer\b/i, /\bdean\b/i, /department chair/i,
      /\bresearcher\b/i, /academic researcher/i,
      /\bPhD\b/, /research scientist/i,
      /economics educat/i, /research institute/i,
      /institute for [a-z ]*?(policy|research|economic)/i,
      /policy research/i, /economic policy/i,
      /graduate school of business/i,
    ],
    companyAnyOf: [
      /\buniversity\b/i, /\bcollege\b(?! sav)/i, /\bschool of business\b/i,
      /institute for/i, /research center/i, /\bSIEPR\b/,
    ],
  },

  // ---- Financial Advisors / Planners / Insurance ----------------------
  {
    name: "Financial Advisors / Planners / Insurance",
    priority: 75,
    relevance: "Medium",
    reason: "Potential referral, client-gift, family-finance, or sponsorship contact.",
    tags: "advisor/planner",
    anyOf: [
      /\bCFP®?\b/i, /\bChFC®?\b/i, /\bCFA\b/, /\bCDFA®?\b/i,
      /\bCRC®?\b/i, /\bCRPC®?\b/i, /\bRICP®?\b/i, /\bBFA®?\b/i,
      /\bAAMS®?\b/i, /\bCLU®?\b/i,
      /\bfinancial advisor\b/i, /\bfinancial planner\b/i,
      /financial planning/i, /\bfinancial professional\b/i,
      /wealth (manager|advisor|management)/i,
      /\bRIA\b/, /registered investment adviser/i,
      /insurance (agent|advisor|professional|agency)/i,
      /life and health insurance/i, /life insurance/i,
      /retirement (specialist|planner|income|plan|expert)/i,
      /protect retirement/i, /predictable income/i,
      /tax.?free retirement/i, /estate planning/i,
      /\bfiduciary\b/i, /portfolio manager/i, /investment.{0,15}(advisor|manager|operations|specialist)/i,
      /financial insights/i, /financial dadvisor/i,
      /empowering financial advisors?/i,
      /vice president planning/i, /\bVP.{0,5}planning\b/i,
      /financial psychologist/i, /family money guy/i,
    ],
    companyAnyOf: [
      /\binsurance\b/i, /\bMassMutual\b/i, /\bAllianz\b/i,
      /\bMerrill\b/i, /\bMorgan Stanley\b/i, /Edward Jones/i,
      /Wells Fargo Advisors/i, /Northwestern Mutual/i,
      /Beacon Pointe Advisors/i,
    ],
  },

  // ---- Financial Coaches / Wellness / Therapy -------------------------
  {
    name: "Financial Coaches / Wellness / Therapy",
    priority: 72,
    relevance: "Medium",
    reason: "Related financial-behavior audience, but not always child/book specific.",
    tags: "coach/therapy",
    anyOf: [
      /financial coach/i, /money coach\b/i, /financial therapist/i,
      /financial wellness/i, /financial wellbeing/i,
      /\bAFC®?\b/i, /\bFBS®?\b/i, /accredited financial counselor/i,
      /money mentor/i, /financial mentor/i,
      /behavioral finance/i, /financial behavior/i,
      /financial advocate/i, /financial habitudes/i,
      /financial health coach/i, /money habitudes/i,
      /motivational interviewing/i,
    ],
  },

  // ---- Bankers / Credit Unions / Financial Institutions ---------------
  {
    name: "Bankers / Financial Institutions",
    priority: 70,
    relevance: "Medium",
    reason: "Institutional financial-services contact; useful for sponsorships, bulk buys, or community programs.",
    tags: "bank/credit union",
    anyOf: [
      /community (banker|banking|outreach.*bank)/i,
      /branch (manager|leader|president)/i,
      /community development.*?(bank|credit union)/i,
      /community engagement.*?(bank|credit union)/i,
      /financial institutions?/i, /payments industry/i,
      /platform and payments/i,
    ],
    companyAnyOf: [
      /credit union/i, /\bCUNA\b/,
      /\bbank\b/i, /\bbancorp\b/i, /bankshares/i,
      /savings (bank|institution)/i, /community bank/i,
      /\bfintech\b/i,
      /SavvyMoney/i, /\bPYMNTS\b/i,
      /Wealthsimple/i, /Scotiabank/i,
      /Federal Reserve/i, /Consumer Financial Protection Bureau/i,
      /\bCFPB\b/, /Department of Finance/i, /Department of Treasury/i,
      /Idaho Department of Finance/i,
    ],
  },

  // ---- Nonprofit / Government / Policy --------------------------------
  {
    name: "Nonprofit / Government / Policy",
    priority: 65,
    relevance: "Medium",
    reason: "Institutional, policy, foundation, or community outreach contact.",
    tags: "nonprofit/govt",
    anyOf: [
      /executive director/i, /program (director|manager)\b/i,
      /grants (manager|director)/i, /\bphilanthropy\b/i,
      /policy (analyst|director|advisor)/i,
      /community (outreach|engagement|impact|relations|affairs)/i,
      /financial inclusion/i, /economic mobility/i,
      /coalition (lead|director|manager)/i,
      /\bcommissioner\b/i, /state treasurer/i,
      /director of programs/i,
    ],
    companyAnyOf: [
      /\bfoundation\b/i, /\bnonprofit\b/i, /\bnon-profit\b/i,
      /united way/i, /\bYMCA\b/, /family services/i,
      /community center/i, /community action/i,
      /\.gov\b/i, /department of (the )?treasury/i, /department of education/i,
      /federal reserve/i, /\bCFPB\b/, /\bFDIC\b/, /\bSEC\b/, /\bOCC\b/,
      /\bFINRA\b/, /office of the (state )?treasurer/i,
      /state of [a-z ]+/i, /\bcounty\b/i, /\bcity of\b/i, /municipal/i,
    ],
  },

  // ---- Media / Content / Speakers -------------------------------------
  {
    name: "Media / Content / Speakers",
    priority: 55,
    relevance: "Medium",
    reason: "Potential publicity, review, interview, or content amplification contact.",
    tags: "media/content",
    anyOf: [
      /\bjournalist\b/i, /\breporter\b/i, /\bcorrespondent\b/i,
      /\bcolumnist\b/i, /staff writer/i, /\bcontributor\b/i,
      /podcast (host|producer)/i, /\bpodcaster\b/i,
      /\bhost\b/i, /\bproducer\b/i, /content creator/i,
      /freelance writer/i, /personal finance writer/i,
      /\bspeaker\b/i, /keynote speaker/i,
      /public affairs strateg/i, /media executive/i,
    ],
    companyAnyOf: [
      /\bnews\b/i, /\btimes\b/i, /\bjournal\b/i, /\bmagazine\b/i,
      /\bpodcast(s)?\b/i, /\bmedia\b/i, /\bNPR\b/, /\bPBS\b/, /\bCNN\b/,
      /\bCBS\b/, /\bNBC\b/, /\bABC News\b/i,
    ],
  },

  // ---- Marketing / Sales / Partnerships -------------------------------
  {
    name: "Marketing / Sales / Partnerships",
    priority: 35,
    relevance: "Low",
    reason: "Commercial or outreach contact; relevance depends on finance/education overlap.",
    tags: "marketing/sales",
    anyOf: [
      /marketing (operations|director|manager|lead|communications|specialist)/i,
      /head of marketing/i, /digital marketing/i,
      /marketing communications/i,
      /sales (director|manager|operations)/i,
      /business development/i, /\bpartnerships?\b/i,
      /brand (manager|director|partnerships|at)/i,
      /sponsorship/i, /account executive/i,
      /senior sales/i, /acquisition (engine|manager|specialist)/i,
      /personal brand/i,
    ],
  },

  // ---- Peripheral (low-signal, kept separate) -------------------------
  {
    name: "Peripheral / Not Clarence-specific",
    priority: 10,
    relevance: "Low",
    reason: "Obviously outside the Clarence/children/financial literacy lane.",
    tags: "",
    anyOf: [
      /physical therapist/i, /physical therapy/i,
      /\bESPN\b/, /sports analyst/i, /football analyst/i,
      /sports.{0,3}(&|and).{0,3}entertainment/i,
      /eyeglass/i, /\boptometr/i,
      /future of work architect/i,
      /\bFAFSA\b/, /college planning strategist/i, /scholarship strateg/i,
      /major gifts director/i, /fundraising professional/i,
      /human care services/i, /\bhealthcare\b/i,
      /medical students/i, /audio engineering/i, /music therapy/i,
      /human resources/i, /\bSHRM\b/, /\bSHRM-CP\b/,
      /manager effectiveness/i, /scenario.based learning/i,
      /ESG.*sustainability/i, /governance.*sustainability/i,
      /real estate capital/i, /scholar hotels/i,
    ],
  },
];

// "Needs Review" is the catch-all when nothing matches at all.
const NEEDS_REVIEW = {
  name: "Needs Review / Miscellaneous",
  relevance: "Medium",
  reason: "No clean category from the source headline; review manually.",
  tags: "",
};

const anyMatch = (regexes, hay) => regexes.some((re) => re.test(hay));

function categorize(lead) {
  // Include name in the haystack — LinkedIn names often carry credential
  // suffixes (Jen Dawson, CFP®; Andrew Lewis, CFEI®; JW Harris, Ph.D., CFP®)
  // which are the strongest signals for Advisors / FinLit Educators / Coaches.
  const hay = `${lead.name || ""} ${lead.headline || lead.title || ""} ${lead.description || ""}`;
  const co = `${lead.company || ""}`;
  // Company keywords often appear in the headline (Sales Nav cards include
  // "Title @ Company"). Match companyAnyOf against headline as a fallback.
  const coOrHay = `${co} ${hay}`;
  const matches = [];

  for (const g of GROUPS) {
    let qualifies = false;
    if (g.anyOf && anyMatch(g.anyOf, hay)) qualifies = true;
    if (!qualifies && g.companyAnyOf && anyMatch(g.companyAnyOf, coOrHay)) qualifies = true;
    if (!qualifies) continue;
    if (g.requireAlso) {
      const allHit = g.requireAlso.every((inner) => anyMatch(inner, hay) || anyMatch(inner, co));
      if (!allHit) continue;
    }
    matches.push(g);
  }

  // Peripheral is a hard override — if those keywords hit, the lead is
  // out of lane regardless of what else matched (e.g. a "Podcast Host" who
  // is actually a Football Analyst at CBS Sports).
  const peripheral = matches.find((m) => m.name === "Peripheral / Not Clarence-specific");
  if (peripheral) {
    const others = matches.filter((m) => m !== peripheral).map((m) => m.name).join("|");
    return {
      primary: peripheral.name,
      relevance: peripheral.relevance,
      reason: peripheral.reason,
      tags: peripheral.tags,
      secondary: others,
    };
  }

  const usable = matches;

  if (!usable.length) {
    return {
      primary: NEEDS_REVIEW.name,
      relevance: NEEDS_REVIEW.relevance,
      reason: NEEDS_REVIEW.reason,
      tags: NEEDS_REVIEW.tags,
      secondary: "",
    };
  }

  usable.sort((a, b) => b.priority - a.priority);
  const top = usable[0];
  const secondary = usable.slice(1).map((m) => m.name).join("|");
  // Merge tags from all matched groups, dedup, pipe-separated.
  const tagSet = new Set();
  for (const m of usable) {
    if (!m.tags) continue;
    for (const t of m.tags.split("|")) if (t) tagSet.add(t);
  }
  return {
    primary: top.name,
    relevance: top.relevance,
    reason: top.reason,
    tags: Array.from(tagSet).join("|"),
    secondary,
  };
}

if (typeof self !== "undefined") {
  self.CGB_CATEGORIZER = { categorize, GROUPS, NEEDS_REVIEW };
}
if (typeof module !== "undefined") {
  module.exports = { categorize, GROUPS, NEEDS_REVIEW };
}
