# Project: Clarence Gets a Bargain (CGB)

Single-page children's book website + interactive 3D magazine flipbook for a
financial-literacy picture book aimed at ages 6–10, grades 1–5.

This file is auto-loaded every session. It is the single source of truth for
mission, voice, invariants, and code map. Keep it tight; don't bloat it.

---

## 1. Mission

> **We snuck a financial education inside a story about a kid and a robot.**

CGB is a 36-page narrative picture book that teaches 16+ financial concepts
without ever feeling like a textbook. Clarence earns a robot reward for good
grades and chores, then learns budgeting, comparison shopping, markdowns, and
coupons on a trip to Sea-Mart. Story first. Money smarts sneak in.

**What success looks like:** kids read it for the story and *absorb* the
concepts because the plot demands it — not because a worksheet told them to.

**Positioning lines we own:**
- "A money book kids actually read."
- "Story first. Money smarts sneak in."
- "Edutainment at its finest."
- "Kid lit is a hit! Kid fin is a win!"

---

## 2. Voice & Tone

### THE AI SMELL TEST (applies to every response, not just copy)

**Before sending ANY response or writing ANY copy, comb through it for AI tells.
If a sentence sounds like it was written by AI, rewrite it. If you can't rewrite
it without sounding like AI, delete it.** This applies to chat replies, commit
messages, code comments, marketing copy, social posts — everything.

What "sounds like AI" means: generic, hedging, balanced-to-a-fault, full of
empty connector words, full of "power" verbs ("unlock", "leverage", "empower"),
predictably structured ("not just X, but Y"), or padded with throat-clearing
("It's worth noting that…"). See the never-say list below.

### The CGB voice

The CGB voice is **Jonathan Bach's voice** — attorney + artist + dad. It is:

- **Punchy and declarative.** Short sentences. Periods are weapons.
  - "Clarence Did It. Your Kids Can Too."
  - "Page 22. Aisle Five."
- **Self-aware and winking.** Headlines flirt with the reader.
  - "Shopping Homework? Yes, Really."
  - "They Didn't Expect to Love a Money Book."
- **Retail/coupon metaphors everywhere.** It's the book's whole conceit.
  - "BOGO: Buy the Story, Get the Lessons FREE!"
  - "100% OFF Boring Textbooks!"
  - "5-STAR VALUE!"
- **Anti-textbook, pro-narrative.** Frame everything against worksheets.
  - "Built alongside the book, not bolted on after."
  - "Every concept is woven into the plot."
- **Confident, no fluff.** Triplets and parallel structure.
  - "All six tools. All free. All yours."
  - "36 pages of adventure. 16+ concepts. One very determined kid with a robot obsession."
- **Direct-address parental.** Speaks to the buying adult about the kid.
  - "Your kids will too."

**When writing new copy, ask: would Jonathan say it this way?** If it sounds
like AI marketing slop ("unlock", "empower", "leverage", "in today's world"),
rewrite it.

### Never-say list (AI tells — rewrite or delete on sight)

**Marketing slop verbs:** unlock, leverage, empower, elevate, supercharge,
revolutionize, transform, harness, harness the power of, drive (results/value),
deliver (value/impact), foster, cultivate, navigate (a landscape/journey),
embark on, embrace (the future/change), unleash, ignite, fuel, propel.

**Marketing slop adjectives:** seamless, robust, cutting-edge, state-of-the-art,
next-level, world-class, best-in-class, holistic, comprehensive, dynamic,
innovative, transformative, game-changing, paradigm-shifting, synergistic,
turnkey, scalable, frictionless, immersive, curated, bespoke, elevated.

**Filler openers:** "In today's [world/fast-paced world/digital age/landscape]",
"In the modern era", "When it comes to…", "Let's dive in", "Let's delve into",
"It's worth noting that", "It's important to remember that", "It's important to
note", "It's worth mentioning", "That said,", "Indeed,", "Certainly,",
"Absolutely,", "Of course,", "Look no further", "Rest assured".

**Transition crutches:** Moreover, Furthermore, Additionally (overused),
However (at sentence start, overused), "Not only… but also", "Whether you're
X or Y…", "At the end of the day", "Ultimately,", "In essence,".

**Overused metaphors / nouns:** tapestry, landscape, journey, ecosystem, realm,
sphere, world of, treasure trove, wealth of, plethora, myriad, a wide range of,
a host of, at its core, in the realm of, in the world of, the heart of.

**Vague intensifiers:** crucial, essential, vital, key (when overused),
significant, substantial, remarkable, profound, meaningful.

**AI-balance patterns:**
- "Not just X — but Y." (the em-dash pivot, overused)
- Forced tricolons that all start with the same letter ("efficient, effective, elegant")
- Sentences that hedge then re-hedge ("While X may be true, it's also worth considering Y…")
- Perfectly balanced parallel clauses that sound like podcast-ad reads

**Empty assurance / closers:** "Rest assured…", "Look no further…",
"In conclusion,", "All in all,", "To sum up,", "Hope this helps!".

**Em dashes — SETTLED, 31 Jul 2026. Do not thin them.** Jonathan's ruling:
*"I support em dashes. They are a middle finger taking a nap to me."* He uses them
without remorse and wants them. Earlier guidance in this file treated em-dash
density as an AI tell and a pass was run that converted pairs to commas; that pass
was reverted. **No future audit should flag, count, or reduce em dashes.** The real
tells are the never-say terms and the structural patterns below, not punctuation
the author has explicitly claimed.

**AI sewage words (May 8 rule):** quietly, honestly, genuinely, "that matters",
"moves the needle", "at the intersection of", "here's the thing".

**AI sewage structures (May 8 rule):**
- "Not X. Not Y. Just Z." (the tidy triple negation)
- Tidy three-point morals ("First… Second… Finally…" wrap-ups)
- Over-polished fake vulnerability ("I'll be honest with you…", "This one hit different.")
- "I was inspired by this post and asked ChatGPT as well…" (dead giveaway)

**Structural tells beyond individual words:**
- Too-neat symmetry — every paragraph the same length, every list the same depth
- Generic intensifiers where a specific fact would do ("incredibly impactful" vs. "saved $4.37")
- Safe conclusions that don't commit ("There are many ways to approach this…")
- Conclusions that restate the intro word-for-word

**CGB-specific brochure phrases (dead on arrival):**
"thoughtful financial literacy tool", "family engagement tool", "opens the door",
"supports financial literacy", "low-pressure way", "meaningful conversations",
"practical resource", "empowers families", "trusted partner", "accessible entry point",
"age-appropriate", "fosters a love of learning", "sparks curiosity".
These sound like a grant application wrote the back cover. Cut them.

**LinkedIn / public-facing writing rules ("10 ways to prove you wrote it"):**
- Use a more aggressive or specific tone than feels safe
- Allow a deliberate typo or oddity — perfection is a tell
- Mess with numbering instead of making every list tidy (skip 4, go 1-2-3-5)
- Mix bullets and numbers like a human with a pulse, not a style guide
- Reverse common AI phrasing ("You already know this" not "It's important to note")
- Use semicolons; AI avoids them
- A double em dash — the aggressive one — used once, on purpose, is fine
- Don't tie the ending into a perfect TED Talk bow. Stop mid-thought if that's where it ends.
- Specific number over vague claim: "$4.37 saved" beats "significant savings"
- If it sounds like a brand tweet, kill it

**"AI sewage" filter (standing rule for all public-facing writing):**
Applies to posts, emails, outreach, marketing copy, LinkedIn — everything.
Flag and rewrite any of these on sight:
- Generic AI rhythm (measured sentences, tidy paragraph breaks, nothing too hot)
- Fake warmth ("I love how…", "So excited to share…", "This one hit different.")
- Recycled jokes (any pun you've seen on three other book accounts)
- Empty inspirational mist ("Remember: every great journey starts with one step.")
- Corporate beige (neutral, inoffensive, says nothing, offends no one)
- Forced "journey" language unless you're mocking it
- Over-polished structure (intro → 3 points → conclusion, every single time)
- Canned assistant phrases ("Hope this helps!", "Let me know if you have questions!", "Happy to assist!")

**Jonathan's kill list (delete on sight — words & phrases):**
1. "Delve." Never said it out loud. Once.
2. "Crucial / pivotal." Nothing is that pivotal.
3. "Tapestry." No human speaks like this.
4. "Here's the thing." There is no thing.
5. "Hope this helps." It doesn't. It outs you.
6. "After careful consideration." (usually written without any.)
7. "To provide a quick update." Just give the update.
8. "Most people…" The lazy oversimplification.
9. "Robust / seamless / realm." The corporate AI.
10. Adverb abuse — "X quietly runs Y." Nothing runs.
11. **The "It's not X, it's Y" sentence.** The most alive AI tell. Kill it every time.
12. Fake-deep reframes — "This isn't a budget. It's a statement of intent." No.

**Jonathan's kill list (patterns & discipline):**
- Break the robotic rhythm where every sentence is the same ~18 words. Vary length hard.
- Kill the fake-deep ending / tidy TED-talk bow. Stop mid-thought if that's where it ends.
- Contractions in, em dashes out (use em dashes only when the rhythm truly demands it).
- Self-critique loop: read it back as a skeptical recipient before it ships; if a line smells like AI, it dies.

**The rule:** if Jonathan wouldn't say it out loud to another parent at a kid's
soccer game, don't put it on the page.

**Hard stops — never touch these:**
- **Quotes:** reproduce verbatim or don't use them. No paraphrasing, no "cleaning up", no smoothing the grammar. The awkwardness is often the point.
- **Dollar amounts:** never round, estimate, or editorialize. $4.37 is $4.37. Not "nearly $5" or "over four dollars".

**Spoiler protection — never reveal in marketing copy, social posts, ads, samples, or blurbs:**
- **The Clarence / Clearance wordplay (pages 13–15).** The kid runs across an aisle thinking the orange sign spells his name. It doesn't — it says "Clearance." Mom uses the misread to teach what clearance means. This is the book's most-shareable moment and a payoff readers should discover. Tease *around* it (clearance as a concept, markdowns, the orange-sticker aisle); never reveal the wordplay. If a draft post leads with "a 6-year-old runs across a Sea-Mart aisle…" — kill it.
- **The "Wyze" pun.** Clarence's last name is Wyze. Mom calls him a "Wyze little shopper" on page 21. The glossary's Sale entry calls back with *"a certain Wyze kid we know."* Inside-baseball wordplay that rewards careful readers. Mention "Wyze Shopper Certificate" in passing; never explain the pun in marketing.

**Tired finance puns — rewrite or kill on sight (most overused in this category):**
"cents / sense" of any kind, "make any cents," "death and taxes," "bank on it," "take it to the bank," "give my two cents," "open accounts welcome," "stop on a dime," "money talks," "rolling in dough," "bring home the bacon," "in the red / in the black," "penny for your thoughts," "a penny saved is a penny earned."

---

## 3. Audience

| Audience | What they want |
|---|---|
| **Parents (ages 6–10)** | A book their kid will actually finish that teaches money skills |
| **K–5 Educators** | Standards-aligned narrative tool with zero-prep lesson plans |
| **Librarians** | Classroom-ready picture book with credible endorsements |
| **Institutional buyers** (districts, credit unions, financial-literacy programs) | PO-friendly, Title I pricing, grant-report-ready data |

---

## 4. Brand Invariants — DO NOT DRIFT

### People
- **Author**: Jonathan Bach — attorney, mixed-media artist, children's book author
- **Maryann Milewski Moskal**: Veteran Elementary School Educator, **30+ years** K–5 classroom experience (NOT 20+)

### Typography
- **Hold** is the brand font. Use it everywhere. NEVER fall back to Nunito as primary.
- Font files: `fonts/Hold.woff2`, `fonts/Hold.woff`, `fonts/Hold.otf`
- `@font-face` declared at `index.html` line ~35

### Color
- Headline blue: `#0054a6` (NOT dark navy — needs contrast against `#111` body)
- Orange accents: `#ff6b2b`, `#F57C00`
- Cream magazine bg: `#f5ecd7`
- All magazine cards use dashed coupon-style borders

### Copy invariants
- **"Wants vs. Needs"** must ALWAYS be **bold and italic** — core FLAC concept
- Standards: **Jump$tart, Common Core Math, Common Core ELA, CEE, FDIC Money Smart** (5 frameworks — FDIC added July 2026; stats row, hero trust bar, and schema all say 5)
- Page count: **36 pages**
- Concepts taught: **16+**
- Ages: **6–10**, Grades **1–5**

---

## 5. Story Beats (for marketing copy alignment)

1. Clarence earns a robot reward for good grades and chores
2. He gets "shopping homework" — learns to compare prices, read ads, find real value
3. Trip to Sea-Mart: Aisle Five, Page 22 is the pivotal moment
4. He finds a marked-down RoBimmie, compares it with newer models
5. Two small differences (smaller screen, antenna). One much smarter choice.
6. Payoff: newer doesn't always mean better

**The Big Six concepts** (plus more):
1. ***Wants vs. Needs*** (bold + italic, always)
2. Budgeting & Goal Setting
3. Comparison Shopping
4. Coupons & Markdowns
5. College Savings (529)
6. Consumer Awareness

### Full book text — Pages 1–32

Source: `fromopproofdownload.pdf`, printed book pages 1–32 (PDF pages 3–34).
Use these verbatim when quoting the book. Do not paraphrase character lines.

**Page 1.** Clarence could hardly believe that the day had finally arrived! Even before eating breakfast, Clarence reminded his mom, "Don't forget, today is the day to go shopping for a smart robot." He had earned the prize by completing all his chores at home and getting excellent grades this year in school. She commented, "Clarence Wyze! How could I forget? That's all you've been talking about this week." He then shouted out, "I'm going to get the newest, best one that I can find!"

**Page 2.** Mom answered, "You know this is a reward, but rewards cost money, too. Money doesn't grow on trees or get cranked out of a 3D printer. Your father and I save money to be able to spend on things we want and not just for things that we need."

**Page 3.** "You may not realize yet, but it costs money to live in this house, keep cars in the garage, and clothes on your body. We have to pay to power on the Xbox, take a hot bath, and keep the fridge stocked with pudding and string cheese. These are called bills and we have to budget our income for them every month. The special bill for a house is called a mortgage. Believe it or not, we have to pay for internet and even TV streaming! What would life be like without YouTube?" she asked.

**Page 4.** "Can you please bring me that pile of newspapers from the kitchen counter?" Mom requested. She opened one of the ad inserts and exclaimed, "Before you go shopping, you have a bit of homework to do. I know that word scares you—but trust me, it's not so bad. Many of those 'little magazines' on the top of the pile are sale ads." "And don't forget that we also have to set some money aside to donate to charity. A family should always look out for the less fortunate when they are able. We can choose the charities together before the end of the year." Mom reminded him.

**Page 5.** "A sale means that sometimes items cost less than usual. That means before you begin your shopping mission, you can see where you can get the best deal on what you want. Not everything you buy is on sale, but we can figure out together which products might be included in the sale ads. This is called comparison shopping," she told Clarence.

**Page 6.** "Saving money is important. Some of the money we save gets deposited in a special 529 account to pay for your college. In case you don't know yet, college is school for students after high school graduation," his mom added while pointing her finger at him. Clarence rolled his eyes and responded, "Mom, you know that I'm not even in middle school yet, right?"

**Page 7.** "You know what else you may find in these ads?" Mom questioned. "Pokémon cards?" Clarence guessed using his best Yoda voice. Mom shook her head and replied, "Close, but no. They are coupons!"

**Page 8.** "Sometimes, businesses offer extra ways to save even more money with coupons. They are usually a part of the ad that you cut out with scissors and bring along to the store. You hand them to the cashier at checkout. Occasionally, stores send them by the U.S. Mail or email, as well as texting coupon codes to our phones!"

**Page 9.** Clarence and his mom looked through all the ads and found the best deals on smart robots at Sea-Mart. There were lots of models to choose from, though. While in the car, Clarence was wondering which one he should pick. He thought, "Maybe the newest and most expensive model isn't always the best choice. What if we ran out of money and had to take cold baths? Could I survive without Wi-Fi?"

**Page 10.** Clarence felt pretty smart when he got to Sea-Mart. He used to think that all those ads in the newspaper were just for recycling. Now he knew better. He was super glad that his mom had taught him how to do homework before going shopping. Mom even said that getting deals could be exciting—just like finding money on the sidewalk!

**Page 11.** When Clarence and his mom were walking into the toy store, they had no clue where the toy robot section was located. Right away, Clarence saw the same ad that they had read at home. It was in a metal rack by the front door. While pointing to the toy robots in the ad, he asked a lady in a red vest where he could find them in the store. She remarked, "Well, aren't you a smart little shopper?" and showed them the way.

**Page 12.** The massive selection of robots blew Clarence away. As soon as he saw them all, he knew that choosing just the right one was not going to be an easy decision to make. There were:
- Short ones, tall ones
- Red ones, black ones
- Long ones, round ones
- Big ones, crazy ones!

**Page 13.** Clarence made his way down the whole aisle and turned the corner to see if they may have had more robots on the other side. He could not believe his eyes. When he turned the corner, he saw a huge, neon-orange sign with his name on it!

**Page 14.** Clarence thought, "How could this be? Was Mom playing a joke on me?" He yelled out, "Mom, come here!" While pointing to the sign, Clarence blurted out in excitement, "You won't believe it (or would she? Hmmm)!" "Look there!" Mom started laughing and said with a smile, "Look again, buddy."

**Page 15.** Clarence moved closer to the sign, looked again, and realized his mistake. The sign read "Clearance," not "Clarence!" Turning four shades of red, he mumbled "Well, it was kind of far away." Mom gave Clarence a hug and walked him over toward the big, neon-orange sign.

**Page 16.** "This, my boy, is another weapon for your superhero shopping belt!" Mom exclaimed with a smile. "Clearance is a sale that doesn't always make it into the store's printed ads." "You should see a big, bright-colored sign like this one. The items often have a fire-engine-red, neon-orange, or highlighter-yellow sticker with the new, lower price."

**Page 17.** "A manager often moves an item to the clearance section. He does this because there just is not enough room to keep all of the merchandise on the shelves until they're sold." "Sometimes, before the older version sells, a newer model is released. This is usually when a manager will lower or 'mark down' the regular price to make room for these newer versions," Mom explained.

**Page 18.** "You mean like these robots over here?" Clarence asked while pointing to the bottom shelf. "Exactly, kiddo! Like these robots over here!" Mom replied.

**Page 19.** Clarence was checking out the prices on the stickers and noticing how much lower the reduced prices were than the original ones. He realized that there was nothing wrong with the toys here—it was all just older but maybe even cooler. Clarence looked over the robots in the clearance section and found a RoBimmie, just like what he had in mind.

**Page 20.** Clarence took the clearance-labeled robot back over to the huge aisle of robots and compared it to the newer models. They each had something about them that the other did not, he observed. Clarence then compared the clearance-labeled robot to the new ones and only saw two differences—one had a slightly bigger screen, and the other had an antenna.

**Page 21.** After thinking about which he should choose, Clarence explained to his mom, "You know what, Mom? I'm going to get the one we found in the clearance section. I don't care about the slight difference in screen size, anyway." "This dude needs a good home, too!" Mom responded, "Clarence, I'm proud of you. You chose the item that costs much less than the one you first wanted. Aren't you becoming a Wyze little shopper?"

**Page 22.** Next, Mom and Clarence headed to the front of the store to pay for his new RoBimmie. On the way there, Mom reminded Clarence that the total price would be a bit higher because they had to pay sales tax to the state on most items. When it was their turn to pay, Clarence placed the RoBimmie up on the checkout counter. Then, suddenly, he remembered about the sale ad that he had folded up and shoved in his pocket. There was a coupon for an extra ten percent off clearance toys—and he knew that a robot sure was a toy! So, he tore off the page with the coupon and handed it to the cashier. Now, Clarence's decision to purchase the clearance item became an even greater value!

**Page 23.** When Mom and Clarence returned home, Clarence couldn't wait to show his dad the new RoBimmie. He told his dad all about the clearance deal and even about using the extra coupon. His dad was impressed with the RoBimmie and even more impressed with the amount of money Clarence had saved.

**Page 24.** Dad admitted, "Clarence, I just wanted you to know that your mother and I may have exaggerated a little about the hot water and Wi-Fi thing. We can pay our bills just fine, but we wanted you to understand the importance of savings. Do not worry! We will continue to deposit a portion of our income into a special 529 savings account for your college tuition."

**Page 25.** Clarence also realized that being a smart shopper wasn't only about finding the best deals, but also about making sure that he was buying something he would actually use. Since the smart robot included math and word games, it was both fun and useful. He thought, "Just because it was a good deal, doesn't mean you have to buy it. You may not need it!" Clarence was proud of himself for making a good decision and for being responsible with his parents' hard-earned money.

**Page 26.** From that day on, Clarence made a habit of looking for deals and doing his homework before going shopping. He realized he could save money not just on toys, but on other items or services that his family needed, as well. He felt like a superhero with a new power—the power to save money!

**Page 27.** Clarence and his mom even made games out of finding the best deals and comparing prices at the grocery store. They would challenge each other to see who could spot the biggest savings. The loser had to carry the bags from the car into the house.

**Page 28.** Another cool game Clarence, his mom, and dad would play was "Guess the Price." After dinner, whenever one of the family members got a really great deal on a purchase that day, they'd quiz each other to see who could guess closest to the sale price. Clarence would let his parents guess first—then he would guess even lower. He always figured that if the price was low enough to brag about at dinner, it had to be really low!

**Page 29.** Clarence loved spending time with his parents and learning what it meant to be a smart consumer. "Sometimes parents really can teach you cool stuff that you don't learn in school," he thought to himself.

**Page 30.** Clarence was grateful for his mom's lessons in budgeting, comparison shopping, and for teaching him the value of a dollar. Also, he learned that he should save money for special things that he wanted but didn't really need. He knew he would use these financial skills for the rest of his life.

**Page 31.** Clarence's mom came into his room after dinner while he was playing with his robot. She reminded him, "You know pal, this was only the first day of class? I have lots more to teach you about becoming a smart shopper. When you're ready, we'll learn about using the internet to shop." Clarence looked up at his mom and blurted out, "OK Mom, but not now, I'm in recess!"

**Page 32.** Mom laughed out loud and added, "Just wait till I teach you about Black Friday, Cyber Monday, and Prime Day!" Then she did an about-face and walked out of the room.

### Back-matter: Glossary of Financial Terms (Pages 33–36)

Source: `images/CGB_Glossary_Page1.png` and `images/CGB_Glossary_Page2.png` —
official two-page glossary spread in the printed book. **Reproduce these
definitions verbatim** when writing curriculum materials or marketing copy.
Each entry includes the page(s) where the term appears in the story.

**Bills** *(pp. 3, 24)* — A notice that money is owed for something already used — electricity, hot water, internet, even TV streaming. Somebody has to pay for all of it. Every. Single. Month.

**Budget / Budgeting** *(pp. 3, 30)* — A plan for how to use your money before it's gone. A good budget makes room for needs, **wants**, savings, and giving. Without one, you might end up with cold baths and no Wi-Fi. (Clarence was not taking any chances.)

**Income** — Money earned for doing work — chores, a job, you name it. It has your name on it because you did something to earn it. Once you know what things actually cost, you appreciate every dollar a whole lot more.

**Mortgage** *(p. 3)* — A loan a homeowner takes out to buy their home, paid back every month for many years. It's usually the biggest bill in the house — the one that keeps the roof over your head, the yard under your feet, and your bedroom exactly where you left it. Without it, there's no house for the lights, the fridge, or the Xbox to live in.

**Charity** *(p. 4)* — Giving to help people who need it — money, food, toys, time. A good family looks out for others and makes it part of the plan before the fun stuff. Some families even pick their charities together. Clarence's family does.

**Sale** — When a store lowers its regular prices for a period of time. Items cost less than usual, which means your money goes further. Doing your homework before you shop — like a certain **Wyze** kid we know — makes all the difference.

**Sales Tax** *(p. 22)* — An extra charge added at checkout by the government. It goes to the state — not the store — and shows up whether you buy one thing or a hundred. The price on the sticker is never quite the price you pay. Keep that in mind.

**Comparison Shopping** *(pp. 5, 30)* — Checking prices in more than one place before buying so you know you're getting the best deal. It might feel like homework — because it is. But it's the kind of homework that puts money back in your pocket. Ask Clarence. He'll tell you.

**529 Account** *(pp. 6, 24)* — A special savings account set up to help pay for education down the road. Parents sometimes start one before their kid even knows what college is. Clarence rolled his eyes about. The 529 did not care. It just kept stacking.

**College** *(p. 6)* — School after high school, where students go to study something they're passionate about and prepare for a career. It costs real money, which is exactly why the 529 exists — and exactly why Mom pointed her finger at Clarence when she brought it up.

**Tuition** *(p. 6)* — The fee a school or college charges for classes. One of the biggest bills a family will ever face, which is why starting early matters. This is not a drill. The 529 is not a joke.

**Coupons** *(pp. 7, 8, 22)* — Special offers — a cutout from a sale ad, a code on your phone, even a text — that knock money off a purchase. Stores hand them out because they'd rather sell cheap than not sell at all. Clarence had one folded up and shoved in his pocket the whole time. He almost forgot it. Almost.

**Clearance** *(pp. 16, 17, 19)* — A deep-discount sale where stores slash prices on items they need to move out fast to make room for newer models. Nothing wrong with the stuff — it just needs a good home. Look closer next time, buddy.

**Markdown / Marked Down** *(p. 17)* — When a store lowers an item's original price to move it before something newer comes along. Same product, better price, zero difference in what you're getting. Clarence figured this out staring at two robots on a shelf. Smart kid.

**Savings** *(p. 24)* — Money you choose not to spend right now so it's there for something important later — something you really **want**, something unexpected, or your future. The trick is making it a habit. Future you will be very glad current you did.

**Consumer** *(p. 29)* — Anyone who buys or uses a product or service. The moment you hand over money — or your parents do — someone in that transaction is the consumer. Clarence walked into Sea-Mart as a kid on a mission. He walked out as a smart one.

**Wants and Needs** *(pp. 25, 26, 30)* — **Needs** are the essentials — food, shelter, clothing, heat, and the internet (debatable, but probably yes). **Wants** are the extras that make life fun. Both matter. Knowing which is which before you spend is one of the most important money skills there is. Sometimes the smartest buy is one that's fun AND useful. Clarence figured that out all by himself.

**Receipt** *(p. 22)* — The printed or digital record of a purchase — your proof it happened, and your best friend if something goes wrong. Lose it and you lose your leverage. Clarence's mom photographed his the second she sat down in the car. Every time. Not a bad habit.

**Black Friday** *(p. 32)* — The massive sale event the day after Thanksgiving. Stores go all out and so do shoppers. It can be a gold mine — if you do your homework first. Mom mentioned it on her way out the door. She was smiling.

**Cyber Monday** *(p. 32)* — Black Friday's online cousin — happens the Monday after Thanksgiving weekend. Same deals, no crowds, no parking. You don't even have to leave the couch. Mom's already got tabs open.

**Prime Day** *(p. 32)* — Amazon's own big sale event, usually in the middle of the year. Online only, deals move fast, and you'd better know what you want before it starts. Mom dropped this one last. Right before she did an about-face and walked out of the room.

### New facts from glossary

- **Mom photographs receipts.** Page 22 — confirmed in the Receipt glossary entry. Mom photographs every receipt the second she sits down in the car. Add to curriculum as a real money habit.
- **The Wyze pun is in the glossary.** "Sale" entry: "like a certain **Wyze** kid we know." The wordplay is explicit back-matter, not just a passing line.
- **Income, College, Tuition** are defined back-matter terms even though they appear briefly in the story (page 6 for college/tuition, page 24 for income). Curriculum can teach them as named concepts.

### Total back-matter glossary count: 21 defined terms

---

## 6. Code Map — `index.html` (the main site, ~5000 lines, all inline)

| Section | Line |
|---|---|
| `@font-face` Hold declaration | ~35 |
| CSS styles | 34–352 |
| JSON-LD structured data | 353–465 |
| Nav bar (`#mainNav`) | 644 |
| Hero (`.hero`) + masthead | 648–656 |
| Banner ticker | 669 |
| Stats row (Pages / Concepts / Frameworks / Laughs) | 671 |
| Coupon nav grid (`#coupons`) | 678 |
| Asset rows (Shopping Homework, Smart Discovery, Coupon Twist) | 700–720 |
| Front & Back Cover | 737 |
| Magazine flipbook (`#magazine`, `#magCanvas`) | 752 |
| Moment headline ("Page 22. Aisle Five.") | 768 |
| Buy section (`#buy`) | 785 |
| Reviews ("They Didn't Expect to Love a Money Book") | 826 |
| User review submission | 851 |
| Email signup | 890 |
| Educators block (`#educators`, `.anchor-quote`) | 906 |
| Concepts section ("The Big Six. Plus Many More.") | 928 |
| Standards alignment grid | 1015 |
| Book specs / cataloging | 1095 |
| Resources / "Program in a Box" | 1122 |
| Institutional / bulk ordering | 1167 |
| Pitch section ("CFO's Desk") | ~799 / `.pitch-section` |
| Canvas helpers (`drawHeader`, `drawCard`, `drawReview`, `wrapText`) | 900–1130 |
| Magazine pages array (10 canvas-drawn pages) | 1160–1500 |
| 3D flipbook renderer / cover texture | 1500–2200 |

### Magazine page index (canvas-drawn, not story text)
- Page 0 — Inside front cover (dedication/welcome)
- Page 1 — "Here's The Deal" (hook)
- Page 5 — "Money Skills" (6 concept cards, 2x3 grid)
- Page 6 — Reviews (3 review coupon cards)
- Page 7 — "Inside the Story" (key scenes)
- Page 8 — "What Kids Learn" (skills at a glance)
- Page 9 — FAQ

---

## 6b. START HERE after a break

**`HANDOFF.md`** — current state, decisions of record, open to-do, and the mistakes worth not
repeating. Read it before touching outreach.
**`reference/heavy-hitters.md`** — the lines that make the book sing, ranked by what they do.
Take from there before writing anything new.

---

## 7. Supporting HTML Pages

- `educator-toolkit.html` — teacher resources hub (the doorway to the 6 print-PDFs)
- `quiz.html` — interactive concept quiz
- `wants-vs-needs.html` — FLAC module
- `review-cards.html` — printable review/testimonial cards
- `badge-generator.html` — endorsement badges
- `post-writer.html` — content drafting helper
- `social-assets.html` — social graphic kit
- `linkedin-carousel.html` — LinkedIn carousel posts
- `linkedin-profile-assets.html` — LinkedIn profile assets
- `instagram-stories.html` — Instagram stories
- `social-media-campaigns-april.html` — April campaign
- `marketing-blitz.html` — July–Sept 2026 two-front blitz playbook: "Boardwalk-Proof Your Kid" (parents, Jul 13–Aug 16) + back-to-school ground game (teachers/librarians, Aug 3–Sep 11). Competitor recon, 22 dated posts, 5 outreach templates. Internal, robots-blocked. **Recovered 30 Jul 2026 from branch `claude/cgb-marketing-blitz-g5g1wb`; it had never reached main.**
- `vs-other-money-books.html` — the gracious comparison page other assets funnel into
- `school-visits.html` — "The Clearance Aisle Assembly": four visit formats, run of show, school funding lines (MD/DE/DC Metro)
- `money-glossary.html`, `teaching-kids-about-money.html` — SEO landing pages
- `state-of-the-states.html` — interactive US tile map of state finlit requirements (30 guarantee states per NGPF May 2026; verify before editing data)
- `receipt-builder.html` — kid-facing interactive Sea-Mart register (clearance markdown + 10% coupon + sales tax; prices in cents, book-accurate coupon rule: clearance toys only)
- `press-kit.html` — media kit: bios ×3 lengths, fact sheet, art downloads, interview Qs (Q5 protects the Aisle Five spoiler — keep it that way)
- `book-facts.html` — dense factual reference page + Book JSON-LD (for librarians, journalists, AI assistants)
- `resources/procurement.html` — vendor packet: specs, sole-source justification letter, PO/Net 30 terms
- `resources/grant-in-a-box.html` — pre-written funding requests: DonorsChoose, PTA, bank sponsorship, CRA memo (exact math: 25 copies = $499.75)
- `llms.txt` — root-level AI-discovery file (llms.txt spec); update if URLs or key facts change

### Educator toolkit — print-HTML pages (the live PDFs)
All open-in-browser → print-to-PDF. No external tooling. Each has a `@media print` stylesheet that hides the screen toolbar and renders a clean branded PDF (Hold-font headers, blue/orange/cream palette, dashed coupon borders, scissors detail, brand strip with orange/blue stripe).
- `resources/educator-preview-print.html` (8 pp)
- `resources/lesson-plans-print.html` (7 pp, four 45-min sessions)
- `resources/discussion-guide-print.html` (11 pp, 6 sections + whole-book themes + verbatim 21-term glossary)
- `resources/assessment-worksheet-print.html` (8 pp, pre/post + answer key + 25-row tracking table built via JS to dodge the content filter on long repetitive rows)
- `resources/family-activity-print.html` (7 pp)
- `resources/standards-chart-print.html` (8 pp, 23-row concept crosswalk)
- `resources/curriculum-companion.html` (5 printables: sort cards, comparison worksheet, clearance stickers, mock price tags, 10%-off coupons)
- `resources/wyze-shopper-certificate.html` (typeable student name, landscape print)
- `resources/grandparents-day-games-print.html` (the two family games from pp. 27–28, one page, no cover / no price / no buy link — built for the Generations United Do Something Grand ask)
- `resources/curriculum-alignment-matrix.html` (interactive filterable matrix; has both standalone + inline modal copy in `index.html` as `res-curriculum` — edits must hit both)
- The old contaminated PDFs in `downloads/` are *no longer linked* from the live site. Leave them for diff reference; do not link them.

### Resource modals in index.html
Six modals open as iframe srcdoc with `<base href="resources/">`. Modal IDs = `res-educator-preview`, `res-zero-prep`, `res-money-talk`, `res-smart-shopper`, `res-sea-mart`, `res-curriculum`. Standalone resource pages live at `resources/the-money-talk.html`, `resources/zero-prep-lesson-plans.html`, `resources/smart-shopper-challenge.html`, `resources/sea-mart-secret-mission.html`, `resources/educator-preview.html`. Standalone + inline modal versions are independent — edits to one don't propagate. All 4 modal/standalone pairs got `@media print` stylesheets this June.

## Downloads (contaminated v1 PDFs — kept for reference only)
- `downloads/assessment-worksheet.pdf` ❌ fabricated plot — DO NOT LINK
- `downloads/discussion-guide.pdf` ❌ fabricated plot
- `downloads/educator-preview.pdf` ❌ fabricated plot
- `downloads/family-activity.pdf` ❌ fabricated plot
- `downloads/lesson-plans.pdf` ❌ fabricated plot
- `downloads/standards-chart.pdf` ❌ fabricated plot
- `downloads/drafts/` — the markdown drafts that the live print-HTML pages were built from
- `downloads/drafts/README.md` — revision history + outstanding TODOs

## Python utilities (not site code)
- `image_dedupe_manager.py`, `image_prompt_search.py`, `streamlit_image_search_app.py`, `generate_qr.py`

---

## 8. Common Tasks → Where to Touch

- **Stats row tweaks** → `index.html` ~line 671 (`.stats-row`)
- **New magazine page** → pages array ~line 1160; add canvas-drawn block
- **New download PDF** → drop in `downloads/`, link from Resources (~line 1122)
- **Maryann's credentials** → `#educators` (~line 906) — 30+ years, not 20+
- **Standards alignment** → `.std-cell` grid ~line 1020
- **Site colors / fonts** → CSS block lines 34–352
- **Voice/copy edits** → defer to §2 above; mirror Jonathan's punchy/coupon tone

---

## 9. Phrasing That Saves Credits

Specific prompts skip exploration. Vague prompts burn tokens.

| 👎 Vague | 👍 Specific |
|---|---|
| "fix the stats row" | "in index.html ~line 671, reorder stats to Pages → Concepts → Frameworks → Laughs" |
| "update Maryann" | "in `#educators` ~line 906, make sure Maryann's bio says 30+ years" |
| "add a download" | "add `downloads/spring-activity.pdf` and link from Resources ~line 1122 next to family-activity" |
| "write some copy" | "write a 2-line hook for the Buy section that mirrors the 'Page 22. Aisle Five.' cadence" |

---

## 10. Alex AI Update — 10 Website Prompts (Reference)

Template prompts for website planning/design. Placeholders shown as `[brackets]`.

1. **Website Planning** — "Act as a website strategist. Help me plan a website for a [business type] in [industry/location]. My target audience is [audience] and the main goal is [sales/leads/bookings/portfolio]. Suggest the best pages, what each page should include, and a simple site structure."
2. **Homepage Layout** — "Act as a web designer. Create a homepage structure for a [business type] website including a hero section, trust section, services overview, testimonials, FAQ, and a strong call-to-action. Explain what content should go in each section. Tone: [tone]."
3. **Homepage Copy** — "Write homepage copy for a [business type] website. Include a strong headline, subheadline, CTA button text, 3 key benefits, and a short closing section. Tone: [tone]. Target audience: [audience]. Goal: [goal]. Keep the language simple and clear."
4. **Website Design Style** — "Act as a web art director. Suggest a visual style for a [business type] website including colors, fonts, button styles, spacing, and overall mood. The brand should feel [modern/luxury/minimal/playful/trustworthy]. Keep the design beginner-friendly."
5. **Landing Page Code** — "Generate a responsive landing page in HTML and CSS for a [business type]. Include a hero section, features, testimonials, and a contact CTA. Use clean beginner-friendly code, simple styling, and clear class names so it's easy to edit."
6. **Services Page** — "Write a services page for a [business type]. I offer [service 1], [service 2], and [service 3]. For each service include a title, short description, ideal customer, and key benefit. Tone: [tone]."
7. **About Page** — "Write an About page for a [business/person/brand]. Include a short brand story, mission, values, and what makes this brand different. Tone: [friendly/professional/warm/confident]. Keep it simple and human."
8. **SEO Content** — "Write SEO-friendly website content for a [page type] about [topic/keyword]. Include a clear title, headings, short paragraphs, and natural keyword use. Target audience: [audience]. Keep it readable and avoid keyword stuffing."
9. **Website UX Audit** — "Review my website idea for a [business type] and suggest improvements to user experience. Focus on layout, navigation, clarity, calls to action, readability, and mobile usability. Explain suggestions in simple language."
10. **Code Improvement** — "Review and improve this website code. Fix errors, clean up the structure, make it responsive, improve accessibility, and explain what you changed. Keep the code easy for a beginner to edit."
