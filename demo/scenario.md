# Demo scenario: Democracy and elections in grade 10

## Background

This scenario demonstrates three layers working in combination:

| Layer | Technology | Role |
|---|---|---|
| **1. Grep via SPARQL** | GraphDB + MCP server | Retrieves exact competence aims from Grep's triplestore |
| **2. MCP server** | FastMCP + Python | Exposes Grep as an AI tool — in Grep format and CASE format |
| **3. Learner Context** | Simulated user profile | Tailors the AI response to the class's specific situation |

---

## Teacher's question

> "Which competence aims in social studies are relevant for a project on democracy and elections?"

---

## Step 1 – Grep via MCP, without Learner Context

The AI uses the MCP tool `grep_hent_kompetansemaal("SAF01-04", "10")` and retrieves all
19 competence aims for grade 10 directly from Grep's triplestore.

**Example AI response:**

> Here are the competence aims in social studies (SAF01-04) for grade 10 that are relevant for
> a project on democracy and elections:
>
> - **KM1648** – reflektere over kva for aktørar som har makt i samfunnet i dag, og korleis
>   desse grunngir standpunkta sine
> - **KM1652** – beskrive trekk ved det politiske systemet og velferdssamfunnet i Noreg i dag
>   og reflektere over sentrale utfordringar
> - **KM1650** – reflektere over korleis menneske har kjempa og kjempar for endringar i
>   samfunnet og samstundes har vore og er påverka av geografiske forhold og historisk kontekst
> - **KM1651** – beskrive sentrale lover, reglar og normer og drøfte kva konsekvensar brot på
>   desse kan ha for den enkelte og for samfunnet
> - *(+ 15 remaining competence aims for grade 10)*

The response is correct, but generic — the AI does not know what the class has already covered.

---

## Step 2 – With Learner Context

The teacher adds the user profile from `learner_context.json` at the top of the prompt:

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

The AI still uses `grep_hent_kompetansemaal` via MCP, but tailors the response to the profile.

**Example AI response:**

> Based on the class's progress, I recommend prioritising these competence aims:
>
> **Next steps — directly relevant for the project:**
> - **KM1648** – power in society (who decides, and how is it justified?)
> - **KM1652** – the political system and the welfare state in Norway
>
> **Supporting — can be drawn in as prior knowledge:**
> - KM1643 (diversity and identity, already covered) — useful as an entry point for
>   discussion of democratic values
>
> KM1638 (technology) and KM1640 (geography/living conditions) have been covered and do not
> need prioritising, but can be mentioned as context if needed.

The response is precise and actionable — the AI points directly to the next relevant step.

---

## Step 3 – CASE format via MCP

For systems that communicate via the CASE standard, the AI can use
`grep_hent_cfitems("SAF01-04", "10")` instead. This returns exactly the same
Grep data, but structured as a CASE CFDocument with CFItems.

**Excerpt from the response:**

```json
{
  "CFDocument": {
    "identifier": "http://psi.udir.no/kl06/SAF01-04",
    "humanCodingScheme": "SAF01-04",
    "title": "Læreplan i samfunnsfag"
  },
  "CFItems": [
    {
      "identifier": "http://psi.udir.no/kl06/KM1648",
      "humanCodingScheme": "KM1648",
      "fullStatement": "reflektere over kva for aktørar som har makt i samfunnet i dag, og korleis desse grunngir standpunkta sine",
      "educationLevel": ["Tiende årstrinn"],
      "CFDocumentURI": {
        "identifier": "http://psi.udir.no/kl06/SAF01-04",
        "title": "Læreplan i samfunnsfag"
      }
    }
  ]
}
```

Same MCP server — two formats. The Grep structure is unchanged.

---

## Comparison

| | Step 1 | Step 2 | Step 3 |
|---|---|---|---|
| **Tool** | `grep_hent_kompetansemaal` | `grep_hent_kompetansemaal` | `grep_hent_cfitems` |
| **Grep data** | All 19 competence aims for grade 10 | Same 19 aims | Same 19 aims |
| **Format** | Grep format | Grep format | CASE CFItem |
| **Learner Context** | No | Yes (simulated) | Optional |
| **AI response** | Generic list | Tailored to progress | Machine-readable standard |
| **Value** | Correct, but not actionable | Directly useful for the teacher | Interoperable with other systems |

---

## What is simulated?

**Learner Context:** In a real LTI integration, the user profile would be sent automatically
via an **LTI Launch Message** when the teacher opens the AI tool from Canvas or similar.
In this mockup, it is pasted manually into the prompt to illustrate the concept.
This is the "missing link" that a real LTI setup would fill in automatically at launch.

**Grep data:** Fetched live from Grep's triplestore via SPARQL — not mocked.

**CASE format:** Generated in the MCP server using the ontology mapping in
`ontologi/grep_case_mapping.ttl`. No changes to Grep.
