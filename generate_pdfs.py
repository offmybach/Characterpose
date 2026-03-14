#!/usr/bin/env python3
"""Generate educator resource PDFs for Clarence Gets a Bargain."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import KeepTogether

OUT = "downloads"
ORANGE = colors.HexColor("#ff6b2b")
NAVY   = colors.HexColor("#1a3a5c")
GREEN  = colors.HexColor("#16a34a")
LGRAY  = colors.HexColor("#f8fafc")
MGRAY  = colors.HexColor("#6b7280")
WHITE  = colors.white

def base_styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle("Cover", fontName="Helvetica-Bold", fontSize=28,
                          textColor=NAVY, alignment=TA_CENTER, spaceAfter=10))
    s.add(ParagraphStyle("CoverSub", fontName="Helvetica", fontSize=14,
                          textColor=ORANGE, alignment=TA_CENTER, spaceAfter=6))
    s.add(ParagraphStyle("CoverMini", fontName="Helvetica", fontSize=11,
                          textColor=MGRAY, alignment=TA_CENTER, spaceAfter=4))
    s.add(ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=20,
                          textColor=NAVY, spaceBefore=18, spaceAfter=8))
    s.add(ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=15,
                          textColor=NAVY, spaceBefore=14, spaceAfter=6))
    s.add(ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=12,
                          textColor=ORANGE, spaceBefore=10, spaceAfter=4))
    s.add(ParagraphStyle("Body", fontName="Helvetica", fontSize=10.5,
                          textColor=colors.HexColor("#333333"),
                          leading=16, spaceAfter=6, alignment=TA_JUSTIFY))
    s.add(ParagraphStyle("BulletItem", fontName="Helvetica", fontSize=10.5,
                          textColor=colors.HexColor("#333333"),
                          leading=16, spaceAfter=4, leftIndent=18,
                          bulletIndent=6))
    s.add(ParagraphStyle("Label", fontName="Helvetica-Bold", fontSize=10,
                          textColor=GREEN, spaceAfter=3))
    s.add(ParagraphStyle("Small", fontName="Helvetica", fontSize=9,
                          textColor=MGRAY, spaceAfter=4))
    s.add(ParagraphStyle("Center", fontName="Helvetica", fontSize=10.5,
                          alignment=TA_CENTER, spaceAfter=6))
    return s

def doc(filename, title):
    path = os.path.join(OUT, filename)
    d = SimpleDocTemplate(path, pagesize=letter,
                          leftMargin=0.85*inch, rightMargin=0.85*inch,
                          topMargin=0.9*inch, bottomMargin=0.9*inch,
                          title=title, author="Jonathan Bach")
    return d

def hr(w=6.3*inch):
    return HRFlowable(width=w, thickness=1.2, color=colors.HexColor("#e2e8f0"),
                      spaceAfter=10, spaceBefore=4)

def badge(text, s):
    return Paragraph(
        f'<font color="#ffffff"><b>&nbsp; {text} &nbsp;</b></font>',
        ParagraphStyle("badge", fontName="Helvetica-Bold", fontSize=9,
                       textColor=WHITE, backColor=GREEN,
                       borderRadius=4, alignment=TA_CENTER, spaceAfter=8))

# ──────────────────────────────────────────────────────────────
# 1. EDUCATOR PREVIEW
# ──────────────────────────────────────────────────────────────
def make_educator_preview():
    d = doc("educator-preview.pdf", "Educator Preview – Clarence Gets a Bargain")
    s = base_styles()
    story = []

    # Cover page
    story += [
        Spacer(1, 1.2*inch),
        Paragraph("EDUCATOR PREVIEW", s["CoverSub"]),
        Paragraph("Clarence Gets a Bargain", s["Cover"]),
        Spacer(1, 0.1*inch),
        Paragraph("A Complete 4-Week Financial Literacy Module", s["CoverMini"]),
        Paragraph("Written & Illustrated by Jonathan Bach", s["CoverMini"]),
        Spacer(1, 0.4*inch),
        Paragraph("Ages 5–9  •  Grades K–5  •  32 Pages  •  Full Color", s["CoverMini"]),
        Spacer(1, 0.6*inch),
        Paragraph("This 12-page preview is for institutional review by chapter directors,\ncurriculum coordinators, and classroom educators.", s["CoverMini"]),
        Spacer(1, 0.4*inch),
        Paragraph("All educator materials are FREE.", ParagraphStyle("FreeBadge",
            fontName="Helvetica-Bold", fontSize=13, textColor=GREEN,
            alignment=TA_CENTER)),
        PageBreak(),
    ]

    # Welcome
    story += [
        Paragraph("Welcome from the Author", s["H1"]), hr(),
        Paragraph(
            "Dear Educator, Librarian, or Community Program Leader,", s["Body"]),
        Paragraph(
            "<i>Clarence Gets a Bargain</i> was born from a simple belief: the best time to teach "
            "a child about money is before they have any. This picture book wraps core financial "
            "literacy concepts inside a funny, fast-paced adventure so kids absorb them the same "
            "way they absorb everything else — through story.", s["Body"]),
        Paragraph(
            "The materials in this package are designed to meet you where you are. Whether you "
            "run an afterschool program, a library story hour, a credit union youth initiative, "
            "or a K–5 classroom, these resources require no financial expertise and no prep time.", s["Body"]),
        Paragraph(
            "Thank you for the work you do. This one's for you — and for every Clarence in your "
            "community who deserves a head start.", s["Body"]),
        Spacer(1, 0.15*inch),
        Paragraph("— Jonathan Bach, Author & Illustrator", s["Body"]),
        PageBreak(),
    ]

    # About the Book
    story += [
        Paragraph("About the Book", s["H1"]), hr(),
        Paragraph(
            "Clarence is on a mission. He wants the coolest toy at Barginville's biggest sale — "
            "but he only has so much money. What he discovers along the way turns him into "
            "the smartest shopper in the whole neighborhood.", s["Body"]),
        Spacer(1, 0.1*inch),
        Paragraph("Core Financial Concepts Covered", s["H2"]),
    ]
    concepts = [
        ("Needs vs. Wants", "Students distinguish essential purchases from desired ones."),
        ("Budgeting", "Clarence counts his money and decides how to allocate it."),
        ("Comparison Shopping", "He compares prices at multiple stalls to find the best deal."),
        ("Coupons & Sales", "He uses a coupon and times his purchase for maximum savings."),
        ("Opportunity Cost", "Choosing the toy means giving up something else — he weighs the trade-off."),
        ("Saving Goals", "A bonus scene shows Clarence deciding to save some change for next time."),
    ]
    for title, desc in concepts:
        story.append(Paragraph(f"<b>{title}.</b> {desc}", s["BulletItem"]))
    story.append(PageBreak())

    # Learning Objectives
    story += [
        Paragraph("Learning Objectives", s["H1"]), hr(),
        Paragraph("After completing the 4-week module, students will be able to:", s["Body"]),
    ]
    objectives = [
        "Define key vocabulary: budget, savings, price, coupon, trade-off, value.",
        "Distinguish between needs and wants with at least 80% accuracy.",
        "Create a simple personal budget using play money or a worksheet.",
        "Compare two prices and identify the better value.",
        "Explain what opportunity cost means in their own words.",
        "Describe at least one strategy a smart shopper uses.",
        "Complete a pre/post assessment demonstrating measurable financial literacy gains.",
    ]
    for o in objectives:
        story.append(Paragraph(f"• {o}", s["BulletItem"]))
    story.append(PageBreak())

    # Standards Mapping
    story += [
        Paragraph("Standards Alignment", s["H1"]), hr(),
        Paragraph("Clarence Gets a Bargain maps to the following national frameworks:", s["Body"]),
        Spacer(1, 0.1*inch),
    ]
    std_data = [
        ["Framework", "Standard / Strand", "Concepts Covered"],
        ["Jump$tart\nNational", "Spending (SPD 1–3)\nSaving (SVG 1–2)\nFinancial Responsibility (FM 1)", "Needs/Wants, Budgeting,\nSaving, Smart Choices"],
        ["CEE", "Standard 1 (Earning)\nStandard 2 (Buying)\nStandard 5 (Saving)", "Budgeting, Comparison\nShopping, Saving Goals"],
        ["CCSS Math", "K.CC, 1.OA, 2.MD.8\n(Counting & Measurement)", "Counting Money, Adding\n& Subtracting Amounts"],
        ["CCSS ELA", "RI.K-2.3, RF.K-2, SL.K-2\n(Informational Text)", "Key Ideas, Vocabulary,\nCollaborative Discussion"],
        ["FDIC\nMoney Smart", "Money Matters (K–2)\nSpend, Share & Save (3–5)", "All core unit concepts"],
    ]
    t = Table(std_data, colWidths=[1.05*inch, 2.3*inch, 2.95*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,0), 9.5),
        ("FONTSIZE",   (0,1), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LGRAY]),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ]))
    story += [t, PageBreak()]

    # Program Overview
    story += [
        Paragraph("4-Week Program Overview", s["H1"]), hr(),
        Paragraph(
            "The program is designed to be delivered in four weekly sessions of 45 minutes each. "
            "Each session uses the book as the anchor text and builds toward measurable outcomes.", s["Body"]),
        Spacer(1, 0.1*inch),
    ]
    weeks = [
        ("Week 1", "Needs vs. Wants + Introducing Budgets",
         "Students meet Clarence and explore the difference between needs and wants. They build a simple budget together."),
        ("Week 2", "Comparison Shopping + Coupons",
         "Students follow Clarence on his bargain hunt, learning to compare prices and evaluate deals."),
        ("Week 3", "Saving Goals + Opportunity Cost",
         "Students explore why Clarence saves some money and what he gives up to do so. Personal saving goals are set."),
        ("Week 4", "Smart Money Decisions + Celebration",
         "Students review all concepts, complete the post-assessment, and celebrate with a classroom 'bargain hunt' activity."),
    ]
    for week, title, desc in weeks:
        story += [
            Paragraph(f"<b>{week}: {title}</b>", s["H3"]),
            Paragraph(desc, s["Body"]),
        ]
    story.append(PageBreak())

    # Sample spread preview
    story += [
        Paragraph("Sample Spread Preview", s["H1"]), hr(),
        Paragraph("Pages 1–8: Clarence Wants Something Special", s["H2"]),
        Paragraph(
            "Clarence spots the ultimate toy at the Barginville sale. Bright, double-page spreads "
            "introduce his character and establish the central question: does he have enough money? "
            "The text introduces the words <i>budget</i>, <i>price tag</i>, and <i>bargain</i> naturally "
            "within the story.", s["Body"]),
        Paragraph("Pages 9–16: The Budget Challenge", s["H2"]),
        Paragraph(
            "Clarence counts his coins and discovers he's short. A two-page spread shows his "
            "coins laid out on a table — a natural counting/addition activity. He learns that "
            "having a plan (a budget) is the first step to getting what you want.", s["Body"]),
        Paragraph("Pages 17–24: Bargain Hunting Begins", s["H2"]),
        Paragraph(
            "Clarence visits three vendors, compares prices, and uses a coupon he found in the "
            "weekly flyer. Illustrations show price tags side-by-side, making comparison shopping "
            "visual and immediate for young readers.", s["Body"]),
        Paragraph("Pages 25–32: The Smart Choice", s["H2"]),
        Paragraph(
            "Clarence makes his decision, celebrates the savings, and puts a little away for next "
            "time. The final spread reveals what 'getting a bargain' really means: not just paying "
            "less, but making a smart choice you feel proud of.", s["Body"]),
        PageBreak(),
    ]

    # How to Order
    story += [
        Paragraph("How to Order", s["H1"]), hr(),
        Paragraph("Clarence Gets a Bargain is available through:", s["Body"]),
        Paragraph("• Amazon  (softcover & Kindle)", s["BulletItem"]),
        Paragraph("• Barnes & Noble  (softcover & Nook)", s["BulletItem"]),
        Paragraph("• IndieBound  (independent bookstores)", s["BulletItem"]),
        Spacer(1, 0.15*inch),
        Paragraph("<b>Bulk & institutional pricing available.</b> For orders of 10+ copies for "
                  "classrooms, credit union branches, or community programs, contact us at "
                  "educators@clarencegetsabargain.com", s["Body"]),
        Spacer(1, 0.3*inch),
        Paragraph("All educator PDFs are free to download, reproduce, and distribute "
                  "within your institution.", s["Small"]),
        Spacer(1, 0.4*inch),
        Paragraph("© 2026 Jonathan Bach. All rights reserved.", s["Small"]),
    ]

    d.build(story)
    print("✓ educator-preview.pdf")


# ──────────────────────────────────────────────────────────────
# 2. LESSON PLANS
# ──────────────────────────────────────────────────────────────
def make_lesson_plans():
    d = doc("lesson-plans.pdf", "Classroom Lesson Plans – Clarence Gets a Bargain")
    s = base_styles()
    story = []

    story += [
        Spacer(1, 0.8*inch),
        Paragraph("45-Minute Classroom Lesson Plans", s["Cover"]),
        Paragraph("Clarence Gets a Bargain", s["CoverSub"]),
        Spacer(1, 0.2*inch),
        Paragraph("Five ready-to-use modules  •  Grades K–5  •  No prep required", s["CoverMini"]),
        Spacer(1, 0.3*inch),
        Paragraph(
            "Each module is designed to stand alone or be used as part of the complete "
            "4-week program. Every lesson uses the book as an anchor text and aligns to "
            "Jump$tart, CEE, and Common Core standards.", s["CoverMini"]),
        PageBreak(),
    ]

    modules = [
        {
            "num": "Module 1", "title": "Meet Clarence: Needs vs. Wants",
            "week": "Week 1, Session 1", "grades": "K–5",
            "standards": "Jump$tart SPD-1; CEE Standard 2; CCSS ELA SL.K-2",
            "objectives": [
                "Define 'needs' and 'wants' in their own words.",
                "Sort a set of items into needs vs. wants categories.",
                "Connect needs vs. wants to Clarence's story.",
            ],
            "materials": [
                "Clarence Gets a Bargain (1 copy or projected)",
                "Needs vs. Wants sorting cards (printable from this packet)",
                "Whiteboard / chart paper",
                "Crayons or markers",
            ],
            "steps": [
                ("Warm-Up (5 min)", "Show 6 images on the board: food, a video game, shoes, a toy car, water, and a jacket. Ask students to give a thumbs up if it's something they NEED, thumbs down if it's something they WANT. Discuss any disagreements."),
                ("Read Aloud (15 min)", "Read pages 1–12 aloud. Pause on page 4 (Clarence sees the toy) and ask: 'Is this a need or a want for Clarence? How do you know?' Let 2–3 students respond."),
                ("Discussion (8 min)", "Use the anchor questions: (1) What does Clarence want? (2) Could he live without it? (3) Can you think of something YOU want that is also a want, not a need?"),
                ("Activity (12 min)", "Distribute sorting cards. Students work in pairs to sort 10 items into two columns: NEEDS and WANTS. Early finishers add their own items."),
                ("Closure (5 min)", "Exit ticket: each student writes or draws 1 need and 1 want. Collect as informal assessment."),
            ],
            "differentiation": "For K–1: use pictures only on sorting cards. For 4–5: add a 'It Depends' column and discuss how context changes classification.",
        },
        {
            "num": "Module 2", "title": "Budgeting Like Clarence",
            "week": "Week 1, Session 2", "grades": "K–5",
            "standards": "Jump$tart SPD-2, SVG-1; CEE Standard 2; CCSS Math K.CC, 1.OA",
            "objectives": [
                "Define 'budget' as a plan for spending.",
                "Count a set amount of money and determine what can be purchased.",
                "Understand that a budget means making choices.",
            ],
            "materials": [
                "Clarence Gets a Bargain",
                "Play money sets (one per student or pair)",
                "Budget worksheet (included in this packet)",
                "Pencils",
            ],
            "steps": [
                ("Warm-Up (5 min)", "Ask: 'If I gave you $5 to spend at a school book fair, how would you decide what to buy?' Take 3–4 answers. Introduce the word BUDGET: 'A budget is a plan that helps you decide how to spend your money.'"),
                ("Read Aloud (12 min)", "Read pages 9–16 (Clarence counts his money). Pause when Clarence lays out his coins. Ask: 'How much do you think he has? Let's count together.'"),
                ("Guided Practice (10 min)", "Give each student $1.00 in play money (4 quarters). Show three 'store items' on the board at $.25, $.50, and $.75. Model choosing items and counting change."),
                ("Independent Activity (13 min)", "Students complete the Budget Worksheet: they are given $2.50 and a menu of 8 items. They plan their spending without going over budget."),
                ("Closure (5 min)", "Pair-share: 'What was the hardest part of staying on budget?' Discuss as a group. Preview next session: comparison shopping."),
            ],
            "differentiation": "K–1: use coins only up to $1.00. Grades 3–5: add a 'savings' line — students must save $.50 and spend the rest.",
        },
        {
            "num": "Module 3", "title": "The Art of the Bargain: Comparison Shopping",
            "week": "Week 2", "grades": "K–5",
            "standards": "Jump$tart SPD-3; CEE Standard 2; CCSS Math 2.MD.8",
            "objectives": [
                "Define 'comparison shopping' and explain why it matters.",
                "Compare two prices and identify the lower-cost option.",
                "Understand how coupons and sales reduce price.",
            ],
            "materials": [
                "Clarence Gets a Bargain",
                "Classroom Store price cards (3 sets at different prices)",
                "Coupon cutouts (printable)",
                "Play money",
                "Comparison Shopping worksheet",
            ],
            "steps": [
                ("Warm-Up (7 min)", "Set up 3 'stores' at different tables with price cards for the same item (e.g., a pencil at $.30, $.25, and $.20). Ask: 'Where would you buy it? Why?' Introduce: 'This is called comparison shopping — checking prices before you buy.'"),
                ("Read Aloud (10 min)", "Read pages 17–24. Pause when Clarence visits each vendor. Ask: 'Is the price going up or down? Should he keep looking?'"),
                ("Coupon Activity (10 min)", "Distribute coupon cutouts (10% off, 25¢ off, buy-one-get-one). Show a price on the board ($1.00). Students calculate the price after each coupon. Which coupon saves the most?"),
                ("Classroom Store Game (13 min)", "Students use $3.00 in play money to 'shop' at the three classroom store tables, finding the best deal on 3 items. They record their choices and total savings."),
                ("Closure (5 min)", "Class discussion: 'What's the smartest move Clarence made in this section?' Write responses on the chart paper as a class anchor chart for the classroom wall."),
            ],
            "differentiation": "K–1: pre-calculate coupon prices; students just identify which is lowest. Grades 4–5: calculate percentage savings and rank stores by value.",
        },
        {
            "num": "Module 4", "title": "Save, Spend, or Share?",
            "week": "Week 3", "grades": "K–5",
            "standards": "Jump$tart SVG-1-2, FM-1; CEE Standard 5; FDIC Money Smart",
            "objectives": [
                "Distinguish between saving, spending, and sharing money.",
                "Define 'opportunity cost' in simple terms.",
                "Set a personal short-term savings goal.",
            ],
            "materials": [
                "Clarence Gets a Bargain",
                "Save/Spend/Share sorting scenarios (cards)",
                "My Savings Goal worksheet",
                "Pencils, crayons",
            ],
            "steps": [
                ("Warm-Up (5 min)", "Ask: 'If you had $10, what are three different things you could do with it?' Record student answers in three columns: SAVE / SPEND / SHARE."),
                ("Read Aloud (10 min)", "Read pages 25–32. Focus on the final scene where Clarence saves some of his change. Ask: 'Why does he save instead of spend it all?'"),
                ("Discussion: Opportunity Cost (8 min)", "Introduce opportunity cost with a simple scenario: 'Clarence could buy a second toy OR save the money. By saving, he gives up the second toy — but he gains something too. What does he gain?' Discuss short-term vs. long-term thinking."),
                ("Savings Goal Activity (12 min)", "Students complete 'My Savings Goal' worksheet: they name something they want to save for, estimate the cost, and calculate how many weeks of saving (at $1/week) it would take."),
                ("Closure (5 min)", "Share-out: students share their savings goal. Teacher records on a class 'Dream Board.' Optional: maintain a class savings tracker on the wall for the following week."),
            ],
            "differentiation": "K–1: limit to Save vs. Spend only; skip opportunity cost vocabulary. Grades 4–5: introduce the concept of interest — 'what if the bank gave you extra money for saving?'",
        },
        {
            "num": "Module 5", "title": "Clarence's Big Decision — Review & Celebrate",
            "week": "Week 4", "grades": "K–5",
            "standards": "All Jump$tart, CEE, and CCSS standards from Modules 1–4",
            "objectives": [
                "Demonstrate mastery of all 5 core financial literacy concepts.",
                "Complete post-assessment with measurable improvement over pre-assessment.",
                "Celebrate financial literacy achievement.",
            ],
            "materials": [
                "Clarence Gets a Bargain",
                "Post-Assessment Worksheet (from A/B packet)",
                "Certificate of Achievement (printable)",
                "Optional: prize bag with mini items for classroom bargain hunt",
            ],
            "steps": [
                ("Warm-Up / Book Recap (8 min)", "Full read-aloud of Clarence Gets a Bargain from cover to cover (or selected pages). Students raise their hand each time they hear a concept they learned: needs/wants, budget, comparison shopping, savings, opportunity cost."),
                ("Post-Assessment (12 min)", "Students complete the post-assessment independently. Collect and score using the answer key. Data tracking table is in the A/B Assessment packet."),
                ("Concept Review Game (15 min)", "Quick-fire team quiz: teacher reads scenarios ('Clarence sees a snack and a toy — he buys the snack because he's hungry. Is the snack a need or a want?'). Teams buzz in. 1 point per correct answer."),
                ("Certificates (5 min)", "Distribute Certificates of Financial Literacy Achievement. Allow students to write their own savings goal on the certificate."),
                ("Closure (5 min)", "Class reflection: 'What is one thing Clarence taught you about money that you'll remember?' Optional family letter sent home recapping what was learned."),
            ],
            "differentiation": "For K–1: use the picture-based post-assessment. For 4–5: add an open-response section to the post-assessment.",
        },
    ]

    for i, m in enumerate(modules):
        story += [
            Paragraph(f"{m['num']}: {m['title']}", s["H1"]),
            hr(),
            Paragraph(f"<b>Session:</b> {m['week']}  &nbsp;|&nbsp;  <b>Grades:</b> {m['grades']}", s["Small"]),
            Paragraph(f"<b>Standards:</b> {m['standards']}", s["Small"]),
            Spacer(1, 0.1*inch),
        ]

        story.append(Paragraph("Learning Objectives", s["H2"]))
        for o in m["objectives"]:
            story.append(Paragraph(f"• {o}", s["BulletItem"]))

        story.append(Paragraph("Materials Needed", s["H2"]))
        for mat in m["materials"]:
            story.append(Paragraph(f"• {mat}", s["BulletItem"]))

        story.append(Paragraph("Lesson Steps", s["H2"]))
        for step_title, step_desc in m["steps"]:
            story += [
                Paragraph(f"<b>{step_title}</b>", s["H3"]),
                Paragraph(step_desc, s["Body"]),
            ]

        story += [
            Paragraph("Differentiation", s["H2"]),
            Paragraph(m["differentiation"], s["Body"]),
        ]

        if i < len(modules) - 1:
            story.append(PageBreak())

    d.build(story)
    print("✓ lesson-plans.pdf")


# ──────────────────────────────────────────────────────────────
# 3. DISCUSSION GUIDE
# ──────────────────────────────────────────────────────────────
def make_discussion_guide():
    d = doc("discussion-guide.pdf", "Discussion Guide – Clarence Gets a Bargain")
    s = base_styles()
    story = []

    story += [
        Spacer(1, 0.8*inch),
        Paragraph("Discussion Guide", s["Cover"]),
        Paragraph("Clarence Gets a Bargain", s["CoverSub"]),
        Spacer(1, 0.2*inch),
        Paragraph("Chapter-by-Chapter Facilitation Guide  •  Mapped to CEE & Jump$tart", s["CoverMini"]),
        Spacer(1, 0.5*inch),
        Paragraph(
            "This guide is designed for educators, librarians, and community facilitators. "
            "It provides discussion prompts, vocabulary support, and critical thinking "
            "questions for each section of the book.", s["CoverMini"]),
        PageBreak(),
    ]

    story += [
        Paragraph("How to Use This Guide", s["H1"]), hr(),
        Paragraph(
            "Each section corresponds to approximately 8 pages of the book. "
            "Discussion questions are organized at three levels:", s["Body"]),
        Paragraph("<b>Literal (L):</b> Direct answers found in the text.", s["BulletItem"]),
        Paragraph("<b>Inferential (I):</b> Require students to read between the lines.", s["BulletItem"]),
        Paragraph("<b>Evaluative (E):</b> Personal connections, opinions, and real-world applications.", s["BulletItem"]),
        Spacer(1, 0.1*inch),
        Paragraph(
            "Vocabulary words are bolded in context. The full glossary appears at the end of this guide. "
            "CEE and Jump$tart alignments are noted at the end of each section.", s["Body"]),
        PageBreak(),
    ]

    sections = [
        {
            "title": "Section 1: Clarence Wants Something Special (Pages 1–8)",
            "summary": "We meet Clarence on the morning of Barginville's biggest sale of the year. "
                       "He spots the toy he's dreamed about — the Turbo-Zoom Racer 3000 — and immediately "
                       "wants it. His mom reminds him: 'You have your own money, Clarence. You decide.'",
            "vocab": [
                ("Budget", "A plan for how to spend your money."),
                ("Price tag", "A label showing how much something costs."),
                ("Bargain", "A good deal — getting something for less than it usually costs."),
                ("Want", "Something you'd like to have but don't need to survive."),
            ],
            "questions": [
                ("L", "What does Clarence want to buy? Where does he see it?"),
                ("L", "What does his mom say about the money?"),
                ("I", "Why do you think the author shows Clarence's face so closely when he sees the toy?"),
                ("I", "What do you predict will happen when Clarence checks his money?"),
                ("E", "Have you ever really wanted something at a store? How did it feel?"),
                ("E", "Is the Turbo-Zoom Racer a need or a want for Clarence? How do you know?"),
            ],
            "standards": "Jump$tart SPD-1 (Identifying wants); CEE Standard 2.1",
        },
        {
            "title": "Section 2: The Budget Challenge (Pages 9–16)",
            "summary": "Clarence opens his piggy bank and counts his money. He has $4.75. "
                       "The Turbo-Zoom Racer costs $6.00. He's short — but he doesn't give up. "
                       "He makes a list of everything he could buy with his money and circles the "
                       "things that are most important to him.",
            "vocab": [
                ("Savings", "Money you set aside to use later."),
                ("Trade-off", "Giving up one thing to get another."),
                ("Afford", "To have enough money to pay for something."),
                ("Priority", "What matters most to you."),
            ],
            "questions": [
                ("L", "How much money does Clarence have? How much does the toy cost?"),
                ("L", "What does Clarence do when he realizes he doesn't have enough?"),
                ("I", "Why do you think Clarence makes a list instead of giving up right away?"),
                ("I", "What does Clarence's list tell us about what he values?"),
                ("E", "Has something ever cost more than you had? What did you do?"),
                ("E", "What trade-offs would you make if you only had $4.75?"),
            ],
            "standards": "Jump$tart SPD-2, SVG-1 (Budgeting, Saving); CEE Standard 2.2, 5.1",
        },
        {
            "title": "Section 3: Bargain Hunting (Pages 17–24)",
            "summary": "Clarence visits three different vendors at the sale, each selling the "
                       "Turbo-Zoom Racer at a different price. He also finds a coupon in his "
                       "jacket pocket — 25¢ off any toy over $3.00. By comparing prices and "
                       "using the coupon, he gets the racer for exactly $4.75.",
            "vocab": [
                ("Comparison shopping", "Checking prices at more than one place before buying."),
                ("Coupon", "A ticket or paper that gives you a discount on an item."),
                ("Discount", "A reduction in the original price."),
                ("Value", "How much something is worth compared to its cost."),
            ],
            "questions": [
                ("L", "How many vendors does Clarence visit? What are the three prices?"),
                ("L", "Where does Clarence find the coupon? How much does it save him?"),
                ("I", "Why is it smart to check more than one price before buying?"),
                ("I", "How does the coupon help Clarence reach his goal? Could he have done it without it?"),
                ("E", "Do your parents use coupons? Have you ever found a deal that surprised you?"),
                ("E", "What would you do if you found a coupon for something you weren't planning to buy?"),
            ],
            "standards": "Jump$tart SPD-3 (Smart Purchasing); CEE Standard 2.3; FDIC Money Smart",
        },
        {
            "title": "Section 4: The Smart Choice (Pages 25–32)",
            "summary": "Clarence buys the Turbo-Zoom Racer and has 0¢ left — until he spots "
                       "a vendor selling lemonade for 25¢. He remembers he has change from the "
                       "coupon. He buys the lemonade and still has a dime left. On the way home, "
                       "he drops the dime in his piggy bank. 'That's how a bargain works,' he says.",
            "vocab": [
                ("Opportunity cost", "What you give up when you make a choice."),
                ("Change", "Money returned to you when you pay more than the price."),
                ("Smart shopper", "Someone who makes careful, informed purchasing decisions."),
                ("Financial literacy", "Understanding how money works and how to use it wisely."),
            ],
            "questions": [
                ("L", "What does Clarence buy with his remaining money? How much does he save?"),
                ("L", "What does Clarence say at the end of the book?"),
                ("I", "What does 'that's how a bargain works' mean to Clarence? What has he learned?"),
                ("I", "Why does Clarence put the dime back in his piggy bank instead of spending it?"),
                ("E", "What is the most important lesson YOU learned from Clarence's adventure?"),
                ("E", "What would you do differently than Clarence — or the same?"),
            ],
            "standards": "Jump$tart SVG-2, FM-1 (Saving, Financial Responsibility); CEE Standard 5.2",
        },
    ]

    for section in sections:
        story += [
            Paragraph(section["title"], s["H1"]), hr(),
            Paragraph("<b>Section Summary</b>", s["H2"]),
            Paragraph(section["summary"], s["Body"]),
            Paragraph("Vocabulary", s["H2"]),
        ]
        vdata = [["Word", "Definition"]] + [[w, d] for w, d in section["vocab"]]
        vt = Table(vdata, colWidths=[1.6*inch, 4.7*inch])
        vt.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), NAVY),
            ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTNAME",   (0,1), (0,-1), "Helvetica-Bold"),
            ("FONTSIZE",   (0,0), (-1,-1), 9.5),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LGRAY]),
            ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ]))
        story += [vt, Spacer(1, 0.15*inch)]

        story.append(Paragraph("Discussion Questions", s["H2"]))
        for level, q in section["questions"]:
            label = {"L": "Literal", "I": "Inferential", "E": "Evaluative"}[level]
            lcolor = {"L": "#3b82f6", "I": "#8b5cf6", "E": "#16a34a"}[level]
            story.append(Paragraph(
                f'<font color="{lcolor}"><b>[{label}]</b></font> {q}', s["BulletItem"]))

        story += [
            Spacer(1, 0.1*inch),
            Paragraph(f"<b>Standards:</b> {section['standards']}", s["Small"]),
            PageBreak(),
        ]

    # Vocabulary Glossary
    story += [
        Paragraph("Complete Vocabulary Glossary", s["H1"]), hr(),
    ]
    all_vocab = [
        ("Afford", "To have enough money to pay for something."),
        ("Bargain", "A good deal — getting something for less than it usually costs."),
        ("Budget", "A plan for how to spend your money."),
        ("Change", "Money returned to you when you pay more than the price."),
        ("Comparison shopping", "Checking prices at more than one place before buying."),
        ("Coupon", "A ticket or paper that gives you a discount on an item."),
        ("Discount", "A reduction in the original price."),
        ("Financial literacy", "Understanding how money works and how to use it wisely."),
        ("Needs", "Things you must have to live safely and healthily (food, water, shelter)."),
        ("Opportunity cost", "What you give up when you make a choice."),
        ("Price tag", "A label showing how much something costs."),
        ("Priority", "What matters most to you."),
        ("Savings", "Money you set aside to use later."),
        ("Smart shopper", "Someone who makes careful, informed purchasing decisions."),
        ("Trade-off", "Giving up one thing to get another."),
        ("Value", "How much something is worth compared to its cost."),
        ("Wants", "Things you'd like to have but don't need to survive."),
    ]
    gdata = [["Term", "Definition"]] + [[w, d] for w, d in all_vocab]
    gt = Table(gdata, colWidths=[1.8*inch, 4.5*inch])
    gt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME",   (0,1), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LGRAY]),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ]))
    story.append(gt)

    d.build(story)
    print("✓ discussion-guide.pdf")


# ──────────────────────────────────────────────────────────────
# 4. PRE/POST ASSESSMENT
# ──────────────────────────────────────────────────────────────
def make_assessment():
    d = doc("assessment-worksheet.pdf", "Pre/Post Assessment – Clarence Gets a Bargain")
    s = base_styles()
    story = []

    story += [
        Spacer(1, 0.6*inch),
        Paragraph("Pre/Post Assessment Worksheet", s["Cover"]),
        Paragraph("Clarence Gets a Bargain  •  Financial Literacy Module", s["CoverSub"]),
        Spacer(1, 0.15*inch),
        Paragraph("Grades K–5  •  Required for grant reporting  •  Answer key on page 3", s["CoverMini"]),
        PageBreak(),
    ]

    # Pre-Assessment
    story += [
        Paragraph("PRE-ASSESSMENT", s["H1"]),
        Paragraph("Complete BEFORE reading Clarence Gets a Bargain.", s["H3"]),
        hr(),
        Paragraph("Name: _______________________________  Date: _____________  Grade: ______", s["Body"]),
        Spacer(1, 0.15*inch),
        Paragraph(
            "Circle the best answer for each question. Do your best — there are no wrong answers right now. "
            "We just want to see what you already know!", s["Body"]),
        Spacer(1, 0.1*inch),
    ]
    pre_q = [
        ("Money that you keep to buy things later is called:", ["a) Spending", "b) Savings", "c) Coupon", "d) Price"]),
        ("Which of these is a NEED?", ["a) A video game", "b) A new toy", "c) Food to eat", "d) A movie ticket"]),
        ("A BUDGET is best described as:", ["a) A type of store", "b) A plan for spending money", "c) A kind of coupon", "d) A savings account"]),
        ("If one store sells juice for $1.00 and another sells it for $0.75, the BETTER DEAL is:", ["a) The $1.00 juice", "b) The $0.75 juice", "c) They cost the same", "d) I can't tell"]),
        ("A coupon is useful because it:", ["a) Makes you spend more money", "b) Lets you return items", "c) Reduces the price of something", "d) Is the same as a price tag"]),
        ("If you SAVE money, you are:", ["a) Spending it right away", "b) Giving it away", "c) Setting it aside for later", "d) Losing it"]),
        ("'Comparison shopping' means:", ["a) Comparing your money to someone else's", "b) Looking at prices in more than one place", "c) Buying two of the same thing", "d) Returning something you bought"]),
        ("An 'opportunity cost' is:", ["a) How much something costs at the store", "b) What you give up when you make a choice", "c) A type of sale price", "d) Free money"]),
        ("Which of these is a WANT?", ["a) A winter coat", "b) A dentist visit", "c) A new video game", "d) Dinner"]),
        ("A 'bargain' is:", ["a) A type of bank", "b) A good deal on something", "c) When something costs more than usual", "d) A store that only sells food"]),
    ]
    for i, (q, opts) in enumerate(pre_q):
        story.append(Paragraph(f"<b>{i+1}. {q}</b>", s["Body"]))
        for opt in opts:
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;{opt}", s["Body"]))
        story.append(Spacer(1, 0.05*inch))

    story.append(PageBreak())

    # Post-Assessment
    story += [
        Paragraph("POST-ASSESSMENT", s["H1"]),
        Paragraph("Complete AFTER completing the 4-week Clarence Gets a Bargain module.", s["H3"]),
        hr(),
        Paragraph("Name: _______________________________  Date: _____________  Grade: ______", s["Body"]),
        Spacer(1, 0.15*inch),
        Paragraph(
            "Circle the best answer. Think about what Clarence taught you!", s["Body"]),
        Spacer(1, 0.1*inch),
    ]
    post_q = [
        ("What do we call money you set aside for future use?", ["a) A trade-off", "b) A budget", "c) Savings", "d) A coupon"]),
        ("A bicycle to ride to school every day is most likely a:", ["a) Want", "b) Need", "c) Bargain", "d) Coupon"]),
        ("When Clarence made a plan for how to spend his $4.75, he was creating a:", ["a) Savings account", "b) Coupon", "c) Budget", "d) Trade-off"]),
        ("Clarence checked the price of the toy at three different vendors. This is called:", ["a) Comparison shopping", "b) Budgeting", "c) Discounting", "d) Saving"]),
        ("The 25¢ off coupon Clarence used is best described as a:", ["a) Price tag", "b) Budget", "c) Discount", "d) Trade-off"]),
        ("Putting your leftover money in a piggy bank instead of spending it is an example of:", ["a) Shopping", "b) Saving", "c) Bargaining", "d) Discounting"]),
        ("What is the MAIN reason comparison shopping is a smart habit?", ["a) It takes more time", "b) It helps you find the lowest price", "c) It means you buy more things", "d) It makes stores angry"]),
        ("When Clarence chose to buy the toy instead of two snacks, the snacks were his:", ["a) Budget", "b) Savings", "c) Opportunity cost", "d) Coupon"]),
        ("A new jacket to stay warm in winter is most likely a:", ["a) Want", "b) Bargain", "c) Need", "d) Discount"]),
        ("Getting a toy for $4.75 that usually costs $6.00 is an example of:", ["a) Overpaying", "b) Getting a bargain", "c) Wasting money", "d) Saving"]),
    ]
    for i, (q, opts) in enumerate(post_q):
        story.append(Paragraph(f"<b>{i+1}. {q}</b>", s["Body"]))
        for opt in opts:
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;{opt}", s["Body"]))
        story.append(Spacer(1, 0.05*inch))

    story.append(PageBreak())

    # Answer Key + Data Tracker
    story += [
        Paragraph("Answer Key & Data Tracking", s["H1"]), hr(),
        Spacer(1, 0.05*inch),
        Paragraph("<b>Pre-Assessment Answers:</b>  1-b  2-c  3-b  4-b  5-c  6-c  7-b  8-b  9-c  10-b", s["Body"]),
        Paragraph("<b>Post-Assessment Answers:</b>  1-c  2-b  3-c  4-a  5-c  6-b  7-b  8-c  9-c  10-b", s["Body"]),
        Spacer(1, 0.2*inch),
        Paragraph("Scoring:  10/10 = Exceeds  •  7–9/10 = Meets  •  4–6/10 = Approaching  •  0–3/10 = Beginning", s["Body"]),
        Spacer(1, 0.3*inch),
        Paragraph("Class Data Tracking Table", s["H2"]),
    ]
    tracker = [["Student Name", "Pre Score\n(out of 10)", "Post Score\n(out of 10)", "Gain", "Proficiency Level"]]
    for i in range(12):
        tracker.append(["", "", "", "", ""])
    tt = Table(tracker, colWidths=[2.1*inch, 1.1*inch, 1.1*inch, 0.7*inch, 1.3*inch])
    tt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LGRAY]),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(tt)
    story += [
        Spacer(1, 0.2*inch),
        Paragraph("Average class pre-score: ______  Average class post-score: ______  Average gain: ______", s["Small"]),
        Spacer(1, 0.15*inch),
        Paragraph(
            "This data tracking table satisfies documentation requirements for Gates Foundation, "
            "Kellogg Foundation, FDIC Money Smart, and Jump$tart grant reporting.", s["Small"]),
    ]

    d.build(story)
    print("✓ assessment-worksheet.pdf")


# ──────────────────────────────────────────────────────────────
# 5. FAMILY TAKE-HOME ACTIVITY
# ──────────────────────────────────────────────────────────────
def make_family_activity():
    d = doc("family-activity.pdf", "Family Take-Home Activity – Clarence Gets a Bargain")
    s = base_styles()
    story = []

    story += [
        Spacer(1, 0.8*inch),
        Paragraph("Family Take-Home Activity", s["Cover"]),
        Paragraph("Clarence Gets a Bargain", s["CoverSub"]),
        Spacer(1, 0.2*inch),
        Paragraph("Two-Generation Engagement  •  Parents & Kids Together", s["CoverMini"]),
        PageBreak(),
    ]

    # Family letter
    story += [
        Paragraph("Dear Families,", s["H1"]), hr(),
        Paragraph(
            "Your child recently read (or heard) <i>Clarence Gets a Bargain</i> — a picture book "
            "about a kid who learns to shop smart, budget his money, and get the best deal in town.", s["Body"]),
        Paragraph(
            "The activities in this packet are designed for you and your child to do TOGETHER. "
            "Research shows that when families talk about money at home, children develop stronger "
            "financial habits for life. These activities take about 15–20 minutes each and "
            "require no special materials.", s["Body"]),
        Paragraph(
            "We hope Clarence becomes a conversation starter in your household. Thank you for "
            "being your child's first and most important teacher.", s["Body"]),
        Spacer(1, 0.1*inch),
        Paragraph("— The Clarence Gets a Bargain Team", s["Body"]),
        PageBreak(),
    ]

    # Activity 1
    story += [
        Paragraph("Activity 1: Our Family Budget", s["H1"]), hr(),
        Paragraph("Best for: Ages 5–9  •  Time: 15 minutes", s["Small"]),
        Spacer(1, 0.1*inch),
        Paragraph(
            "In the book, Clarence made a plan for spending his $4.75. Now it's your family's turn! "
            "Work together to create a pretend weekly budget.", s["Body"]),
        Paragraph("<b>What You Need:</b> A pencil and this sheet.", s["Body"]),
        Spacer(1, 0.1*inch),
        Paragraph("Step 1: Choose a pretend weekly allowance together (try $10).", s["BulletItem"]),
        Paragraph("Step 2: List 3–4 things your child would like to spend it on.", s["BulletItem"]),
        Paragraph("Step 3: Fill in the budget together:", s["BulletItem"]),
        Spacer(1, 0.1*inch),
    ]
    budget_data = [
        ["I want to spend money on:", "How much?", "Is it a NEED or WANT?"],
        ["1.", "$", ""],
        ["2.", "$", ""],
        ["3.", "$", ""],
        ["4.", "$", ""],
        ["TOTAL:", "$", ""],
    ]
    bt = Table(budget_data, colWidths=[3.0*inch, 1.4*inch, 1.9*inch])
    bt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 9.5),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LGRAY]),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ]))
    story += [bt, Spacer(1, 0.1*inch),
              Paragraph("Talk About It: Did the total go over $10? What would you cut first?", s["H3"]),
              PageBreak()]

    # Activity 2
    story += [
        Paragraph("Activity 2: The Bargain Hunt Challenge", s["H1"]), hr(),
        Paragraph("Best for: Ages 6–12  •  Time: 20 minutes at the store", s["Small"]),
        Spacer(1, 0.1*inch),
        Paragraph(
            "Next time you go grocery shopping, give your child a Bargain Hunter mission!", s["Body"]),
        Paragraph("<b>Step 1:</b> Pick 3 items you need to buy.", s["BulletItem"]),
        Paragraph("<b>Step 2:</b> Before you grab them off the shelf, check: Is there a sale price? Is there a store brand that costs less? Is there a coupon on the app or in the flyer?", s["BulletItem"]),
        Paragraph("<b>Step 3:</b> Record your findings below:", s["BulletItem"]),
        Spacer(1, 0.1*inch),
    ]
    hunt_data = [
        ["Item", "Regular Price", "Sale/Coupon Price", "Money Saved"],
        ["1.", "$", "$", "$"],
        ["2.", "$", "$", "$"],
        ["3.", "$", "$", "$"],
        ["TOTAL SAVED:", "", "", "$"],
    ]
    ht = Table(hunt_data, colWidths=[2.0*inch, 1.3*inch, 1.5*inch, 1.5*inch])
    ht.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), ORANGE),
        ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 9.5),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LGRAY]),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ]))
    story += [ht, Spacer(1, 0.1*inch),
              Paragraph("Celebrate: When you get home, tell the story like Clarence — 'I found the BEST deal on...'", s["H3"]),
              PageBreak()]

    # Activity 3 + Dinner Table Prompts
    story += [
        Paragraph("Activity 3: Smart Shopper Journal", s["H1"]), hr(),
        Paragraph("Best for: Ages 7–12  •  Time: 10 minutes, 3× per week", s["Small"]),
        Spacer(1, 0.1*inch),
        Paragraph(
            "For one week, your child keeps a 'smart shopper journal.' Each day, they look for "
            "one money lesson — a sale sign, a price comparison, or a choice they made between "
            "two items. They write or draw it here.", s["Body"]),
        Spacer(1, 0.1*inch),
    ]
    for day in ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]:
        story += [
            Paragraph(f"<b>{day}:</b> What money thing did you notice today?", s["Body"]),
            Paragraph("_" * 80, s["Small"]),
            Spacer(1, 0.08*inch),
        ]
    story += [
        PageBreak(),
        Paragraph("Dinner Table Conversation Starters", s["H1"]), hr(),
        Paragraph("Use these prompts to keep the Clarence conversation going all week:", s["Body"]),
        Spacer(1, 0.1*inch),
    ]
    prompts = [
        "What's the difference between something you WANT and something you NEED? Name one of each.",
        "If you had $5, what three things could you buy and still have some left over?",
        "When you go to the store with me, how do I decide which brand to buy?",
        "What is a coupon and why do people use them?",
        "What is something we're saving up for as a family right now?",
        "If you HAD to choose between a new toy and a fun experience (like the movies), which would you pick? Why?",
        "What does the word 'bargain' mean to you now that you've read Clarence's story?",
    ]
    for p in prompts:
        story.append(Paragraph(f"• {p}", s["BulletItem"]))

    story += [
        Spacer(1, 0.3*inch),
        Paragraph(
            "This activity meets Gates Foundation and W.K. Kellogg Foundation two-generation "
            "program criteria by engaging both parent/caregiver and child in shared financial "
            "literacy activities.", s["Small"]),
    ]

    d.build(story)
    print("✓ family-activity.pdf")


# ──────────────────────────────────────────────────────────────
# 6. STANDARDS CORRELATION CHART
# ──────────────────────────────────────────────────────────────
def make_standards_chart():
    d = doc("standards-chart.pdf", "Standards Correlation Chart – Clarence Gets a Bargain")
    s = base_styles()
    story = []

    story += [
        Spacer(1, 0.6*inch),
        Paragraph("Standards Correlation Chart", s["Cover"]),
        Paragraph("Clarence Gets a Bargain", s["CoverSub"]),
        Spacer(1, 0.1*inch),
        Paragraph("One-page mapping of book concepts to national financial literacy standards", s["CoverMini"]),
        Spacer(1, 0.3*inch),
    ]

    intro = (
        "This chart maps every core financial literacy concept in <i>Clarence Gets a Bargain</i> "
        "and its accompanying educator materials to four major national frameworks. "
        "Use this document when writing grant proposals, curriculum submissions, or institutional adoption requests."
    )
    story += [Paragraph(intro, s["Body"]), Spacer(1, 0.2*inch)]

    headers = ["Book Concept\n& Scene", "Jump$tart\nNational Std.", "Common Core\nMath", "Common Core\nELA", "CEE\nStandard", "FDIC\nMoney Smart"]
    rows = [
        ["Needs vs. Wants\n(pp. 1–8)", "SPD 1:\nSpending\nDecisions", "K.CC.B.5\n(Count to 20)", "SL.K.1\nCollaborative\nDiscussion", "Standard 2:\nBuying Goods\n& Services", "Money Matters:\nUnit 1"],
        ["Budgeting &\nCounting Money\n(pp. 9–16)", "SPD 2:\nBudgeting;\nSVG 1: Saving", "1.OA.A.1\nAdd & Subtract;\n2.MD.C.8", "RI.1.3 Key\nDetails;\nSL.1.4", "Standard 2:\nBuying;\nStandard 5:\nSaving", "Money Matters:\nUnit 2"],
        ["Comparison\nShopping\n(pp. 17–24)", "SPD 3:\nConsumer\nDecisions", "2.NBT.B.5\nFluent Add/\nSubtract to 100", "RI.2.6\nAuthor Purpose;\nSL.2.1", "Standard 2:\nBuying Goods\n& Services", "Spend, Share\n& Save:\nUnit 1"],
        ["Coupons &\nDiscounts\n(pp. 17–24)", "SPD 3:\nConsumer\nDecisions", "3.OA.D.8\nMulti-step\nProblems", "RI.3.4\nVocabulary;\nL.3.4", "Standard 2:\nBuying", "Spend, Share\n& Save:\nUnit 2"],
        ["Saving Goals\n(pp. 25–32)", "SVG 1–2:\nSaving Goals", "3.NBT.A.2\nFluent Add/\nSubtract to 1000", "W.3.1\nOpinion\nWriting", "Standard 5:\nSaving", "Spend, Share\n& Save:\nUnit 3"],
        ["Opportunity\nCost\n(pp. 25–32)", "FM 1:\nFinancial\nResponsibility", "4.OA.A.3\nMulti-step\nWord Problems", "SL.4.1\nDiscussion;\nW.4.1", "Standard 2:\nTrade-offs", "Advanced:\nUnit 1"],
        ["Smart Shopper\nDecisions\n(all)", "SPD 1–3,\nSVG 1–2,\nFM 1 (all)", "K–5 Operations\n& Algebraic\nThinking", "K–5 Speaking\n& Listening;\nReading Info.", "Standards\n1, 2, 5 (all)", "All Units"],
    ]

    table_data = [headers] + rows
    col_widths = [1.35*inch, 1.05*inch, 1.05*inch, 1.05*inch, 1.05*inch, 1.05*inch]
    ct = Table(table_data, colWidths=col_widths)
    ct.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 8),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LGRAY]),
        ("GRID",       (0,0), (-1,-1), 0.4, colors.HexColor("#e2e8f0")),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("ALIGN",      (1,0), (-1,-1), "CENTER"),
        ("BACKGROUND", (0,-1), (-1,-1), colors.HexColor("#fff7ed")),
        ("FONTNAME",   (0,-1), (-1,-1), "Helvetica-Bold"),
    ]))
    story += [ct, Spacer(1, 0.25*inch)]

    story += [
        Paragraph("Framework Abbreviations & Links", s["H2"]),
        Paragraph("• <b>Jump$tart:</b> Jump$tart National Standards in K–12 Personal Finance Education (jumpstart.org)", s["BulletItem"]),
        Paragraph("• <b>CEE:</b> Council for Economic Education — Voluntary National Content Standards in Economics (councilforeconed.org)", s["BulletItem"]),
        Paragraph("• <b>CCSS Math / ELA:</b> Common Core State Standards Initiative (corestandards.org)", s["BulletItem"]),
        Paragraph("• <b>FDIC Money Smart:</b> Federal Deposit Insurance Corporation Money Smart for Young People curriculum (fdic.gov/moneysmart)", s["BulletItem"]),
        Spacer(1, 0.2*inch),
        Paragraph(
            "© 2026 Jonathan Bach. This standards chart may be freely reproduced and distributed "
            "for non-commercial educational purposes.", s["Small"]),
    ]

    d.build(story)
    print("✓ standards-chart.pdf")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    make_educator_preview()
    make_lesson_plans()
    make_discussion_guide()
    make_assessment()
    make_family_activity()
    make_standards_chart()
    print("\nAll 6 PDFs generated in ./downloads/")
