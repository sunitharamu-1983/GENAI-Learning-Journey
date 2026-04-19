# Q, K & V Metrices

Imagine you go to Google.

- **Query (Q):** You type something into the search bar. "Best Italian restaurants near me." The Query is what you want to know.
- **Key (K):** Google looks at millions of websites. Every website has "Tags" or "Meta descriptions" (e.g., Italian, Pizza, New York, Plumbing).
  The Key is what the website claims to be about.
- **Value (V):** You click on a website. The actual text, pictures, and menus on the page are the Value. The Value is the actual content you
  consume.
- **The Math behind the scenes:** Google takes your Query and compares it against millions of Keys.
    - Query("Italian") x Key("Italian Restaurant") = High Score (90%)
    - Query("Italian") x Key("Plumbing") = Low Score (2%)

- Google then takes those percentages (using Softmax) and uses them to rank the Values (the actual websites). You get Italian websites, not
  plumbing websites.

---

### How this works INSIDE a Sentence (The Cocktail Party)
In a Transformer, we aren't searching Google. We are doing Self-Attention—words in a sentence are searching for context within the same sentence.

Imagine the words in a sentence are people at a loud cocktail party. They can't hear the whole sentence at once; they have to figure out what's going on by looking at the other people in the room.

Let's use the sentence your instructor used:

```
"I bought an apple to eat."
```

Let's focus purely on the word "**apple**" trying to figure out its own identity.

- **Step 1:** The Query (What am I looking for?)
  The word "apple" is confused. Am I a fruit? Am I a tech company?
  So, "apple" generates a Query.

  Think of the Query as "apple" holding up a sign that says: "Hey room! Is anyone here talking about food?"

- **Step 2:** The Keys (What do you claim to be?)
  Every other word in the sentence generates a Key.

  "I" holds up a sign: "I am a pronoun."
  "bought" holds up a sign: "I am a transaction."
  "eat" holds up a sign: "I am an action related to food."

- **Step 3:** The Dot Product (Matching signs)
  The system takes Apple's Query ("Anyone talking about food?") and multiplies it by everyone's Key.

  Apple's Query × "I's" Key = Low Score (0%)
  Apple's Query × "bought's" Key = Medium Score (20%)
  Apple's Query × "eat's" Key = High Score (80%)

- **Step 4:** The Value (The actual influence)
  This is where the magic happens.
  "eat" doesn't just have a Key (a sign saying "I am food"). "eat" has a Value—which is its actual mathematical vector containing deep, rich
  information about consuming food.

  ***The system takes Apple's score for "eat" (80%) and says: "Okay Apple, take 80% of 'eat's mathematical Value and absorb it into yourself."***

  ### Text Infographic - The Apple Transformation
  ```
  SENTENCE: "I bought an [APPLE] to eat."

   [APPLE] needs to know: "What am I?"
      │
      ├─> APPLE creates a QUERY: "Looking for Food context"
      │
      ├─> OTHER WORDS create KEYS:
      │      "I"       -> Key: "Pronoun"
      │      "bought"  -> Key: "Commerce"
      │      "eat"     -> Key: "FOOD"  <-- BINGO!
      │
      ├─> SCORING (Query × Key):
      │      Apple × "I"       = 5% relevance
      │      Apple × "bought"  = 15% relevance
      │      Apple × "eat"     = 80% relevance
      │
      └─> EXTRACT VALUE:
             Take 80% of "eat's" VALUE (its raw math data about food)
             Take 15% of "bought's" VALUE
             Mix them together.
             │
             ▼
RESULT: A brand new, transformed vector for APPLE. It is no longer generic. It is mathematically "weighted" towards food.
