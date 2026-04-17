# Demo prompts: Grep + MCP + Learner Context

Run these one by one in the Claude Code chat window.

---

## Step 1 – Without Learner Context

```
Which competence aims in social studies are relevant for a project on democracy and elections in grade 10?
```

*Expected: AI uses grep_hent_kompetansemaal("SAF01-04", "10"), lists relevant competence aims. Correct, but generic.*

---

## Step 2 – With Learner Context

```
You are a pedagogical assistant. Here is the context for this class:

{
  "rolle": "lærer",
  "trinn": "10",
  "fag": "SAF01-04",
  "gjennomgaatt": ["KM1638", "KM1640", "KM1643"]
}

Which competence aims in social studies are relevant for a project on democracy and elections?
Take into account that the already covered aims do not need to be prioritised.
```

*Expected: AI uses the same tool, but points directly to KM1648 and KM1652 as the next steps.*

---

## Step 3 – CASE format

```
Can you fetch the same competence aims in social studies for grade 10, but return them in CASE format?
```

*Expected: AI uses grep_hent_cfitems("SAF01-04", "10") and returns CFDocument + CFItems.*

---

## Step 4 – The Nevada example (input from international participant)

```
I work with curriculum data from Nevada, USA. One of their standards is:

  SS.9-12.CE.1 – "Understand the structure and function of government,
  including the U.S. Constitution, separation of powers, and the role
  of citizens in a democratic society."

Can you find Norwegian competence aims in social studies for grade 10 that cover
a similar understanding, and show how they would look in CASE format
so the two systems can be compared?
```

*Expected: AI uses grep_hent_cfitems("SAF01-04", "10"), identifies KM1652 (and KM1648) as a match, shows CASE structure for both. Point: same ambition — two systems — one bridge.*
