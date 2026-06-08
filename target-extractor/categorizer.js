// CGB Target Extractor - categorizer
// Pure-function group assignment. Each rule has a priority; the highest-
// priority matching rule becomes the lead's primary_group. All matches are
// preserved in secondary_groups so you can re-segment later.
//
// Used by both background.js (final export) and popup.js (live counts).

const GROUPS = [
  {
    name: "FinancialAdvisors",
    priority: 95,
    titleAny: [
      /\bCFP\b/i, /\bChFC\b/i, /\bCFA\b/i,
      /\bfinancial advisor\b/i, /\bfinancial planner\b/i,
      /\bwealth manager?\b/i, /\bwealth advisor\b/i,
      /\bregistered investment adviser\b/i, /\bRIA\b/i,
      /\binvestment advisor\b/i, /\bportfolio manager\b/i,
      /\bretirement planner\b/i,
    ],
  },
  {
    name: "FinLitExperts",
    priority: 90,
    titleAny: [
      /financial literacy/i,
      /financial education/i,
      /financial wellness/i,
      /personal finance educator/i,
      /money coach/i, /money educator/i,
      /finlit/i, /fin-lit/i,
      /jump\$?tart/i,
    ],
    companyAny: [
      /jump\$?tart/i,
      /\bnefe\b/i,
      /next gen personal finance/i,
      /\bngpf\b/i,
      /council for economic education/i,
      /financial literacy/i,
    ],
  },
  {
    name: "WritersPodcastersReporters",
    priority: 85,
    titleAny: [
      /journalist/i, /reporter/i, /correspondent/i, /columnist/i,
      /editor( in chief)?\b/i, /staff writer/i, /contributor/i,
      /podcast (host|producer)/i, /\bpodcaster\b/i, /\bhost\b/i,
      /freelance writer/i, /content creator/i,
      /\bproducer\b/i,
    ],
    companyAny: [
      /\bnews\b/i, /\btimes\b/i, /\bpost\b/i, /\bjournal\b/i,
      /\bmagazine\b/i, /\bpodcast(s)?\b/i, /\bmedia\b/i, /\bwire\b/i,
      /\bnpr\b/i, /\bpbs\b/i, /\bcnn\b/i,
    ],
  },
  {
    name: "Authors",
    priority: 80,
    titleAny: [
      /\bauthor\b/i, /children'?s book author/i, /picture book author/i,
      /illustrator/i, /\bnovelist\b/i, /book reviewer/i,
    ],
  },
  {
    name: "Librarians",
    priority: 78,
    titleAny: [
      /librarian/i, /library media specialist/i, /media specialist/i,
      /library director/i, /youth services/i, /children'?s services/i,
      /head of (the )?library/i,
    ],
    companyAny: [
      /\blibrary\b/i, /library system/i, /public library/i,
    ],
  },
  {
    name: "K5Educators",
    priority: 75,
    titleAny: [
      /\bteacher\b/i, /\beducator\b/i, /\bprincipal\b/i,
      /assistant principal/i, /vice principal/i,
      /curriculum (director|coordinator|specialist|developer)/i,
      /instructional (coach|coordinator|designer)/i,
      /reading (coach|specialist)/i, /literacy (coach|specialist)/i,
      /math (coach|specialist)/i,
      /elementary/i, /K-?5\b/i, /K-?12\b/i, /\bK-?6\b/i,
      /1st grade/i, /2nd grade/i, /3rd grade/i, /4th grade/i, /5th grade/i,
      /first grade/i, /second grade/i, /third grade/i, /fourth grade/i, /fifth grade/i,
      /\bESL\b/i, /\bELL\b/i, /special education/i, /\bSPED\b/i,
      /school counselor/i,
    ],
    companyAny: [
      /elementary school/i, /primary school/i,
      /\bISD\b/i, /school district/i, /public schools/i,
      /charter school/i, /montessori/i,
      /department of education/i, /board of education/i,
    ],
  },
  {
    name: "GovernmentAgencies",
    priority: 70,
    titleAny: [
      /state treasurer/i, /state senator/i, /state representative/i,
      /\bcommissioner\b/i, /\bsuperintendent\b/i,
      /director of (financial|consumer)/i,
      /policy (analyst|director|advisor)/i,
      /program (manager|director).*?(state|federal|county|city)/i,
      /\bgovernor\b/i,
    ],
    companyAny: [
      /\.gov\b/i,
      /department of (the )?treasury/i,
      /department of education/i,
      /\bSEC\b/i, /\bFDIC\b/i, /\bCFPB\b/i, /\bOCC\b/i, /\bFINRA\b/i,
      /federal reserve/i,
      /office of the (state )?treasurer/i,
      /state of [a-z ]+ /i,
      /\bcounty\b/i, /\bcity of\b/i, /municipal/i,
    ],
  },
  {
    name: "InstitutionalBuyers",
    priority: 65,
    titleAny: [
      /community (outreach|engagement|relations|development)/i,
      /financial education (manager|director|lead)/i,
      /\bCSR\b/i, /corporate social responsibility/i,
      /community impact/i, /community affairs/i,
      /procurement/i, /purchasing (director|manager)/i,
      /director of programs/i, /program (director|manager)/i,
      /grants (manager|director)/i,
      /executive director/i,
    ],
    companyAny: [
      /credit union/i, /\bCU\b/,
      /\bbank\b/i, /bancorp/i, /bankshares/i, /savings/i,
      /\bnonprofit\b/i, /\bfoundation\b/i,
      /united way/i, /YMCA/i, /\bclub\b/i,
      /family services/i, /community center/i,
    ],
  },
  {
    name: "Parents",
    priority: 30,
    titleAny: [
      /\bparent\b/i, /\bmom\b/i, /\bmother\b/i, /\bdad\b/i, /\bfather\b/i,
      /mommy blogger/i, /family blogger/i, /parenting/i,
      /stay.at.home/i,
    ],
  },
];

function categorize(lead) {
  const hay = `${lead.title || ""} ${lead.description || ""}`;
  const co = `${lead.company || ""}`;
  const matches = [];

  for (const g of GROUPS) {
    let hit = false;
    if (g.titleAny) {
      for (const re of g.titleAny) {
        if (re.test(hay)) {
          hit = true;
          break;
        }
      }
    }
    if (!hit && g.companyAny) {
      for (const re of g.companyAny) {
        if (re.test(co)) {
          hit = true;
          break;
        }
      }
    }
    if (hit) matches.push(g);
  }

  matches.sort((a, b) => b.priority - a.priority);
  const primary = matches[0]?.name || "Misc";
  const secondary = matches.slice(1).map((m) => m.name).join("|");
  return { primary, secondary };
}

// Expose for both classic-script (popup) and module-style (background) use.
if (typeof self !== "undefined") {
  self.CGB_CATEGORIZER = { categorize, GROUPS };
}
if (typeof module !== "undefined") {
  module.exports = { categorize, GROUPS };
}
