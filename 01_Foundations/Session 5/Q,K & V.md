# Q, K & V Metrices

Imagine you go to Google.

- **Query (Q):** You type something into the search bar. "Best Italian restaurants near me." The Query is what you want to know.
- **Key (K):** Google looks at millions of websites. Every website has "Tags" or "Meta descriptions" (e.g., Italian, Pizza, New York, Plumbing).
  The Key is what the website claims to be about.
- **Value (V):** You click on a website. The actual text, pictures, and menus on the page are the Value. The Value is the actual content you
  consume.
- **The Math behind the scenes:** Google takes your Query and compares it against millions of Keys.
    - Query("Italian") x Key("Italian Restaurant") = High Score (90%)
    - Query("Italian") × Key("Plumbing") = Low Score (2%)

- Google then takes those percentages (using Softmax) and uses them to rank the Values (the actual websites). You get Italian websites, not
  plumbing websites.
