# Demo-scenario: Demokrati og valg på 10. trinn

## Spørsmål fra lærer

> «Hvilke kompetansemål i samfunnsfag er relevante for et prosjekt om demokrati og valg?»

---

## Steg 1 – Uten Learner Context

AI-en bruker MCP-verktøyet `grep_hent_kompetansemaal("SAF01-04", "10")` og får alle 19 KM
for 10. trinn. Den lister dem opp uten å skille mellom hva klassen allerede har jobbet med
og hva som er nytt.

---

## Steg 2 – Med Learner Context

Læreren legger inn brukerprofilen fra `learner_context.json` øverst i prompten:

```
Du er en pedagogisk assistent. Her er konteksten for denne klassen:

{
  "rolle": "lærer",
  "trinn": "10",
  "fag": "SAF01-04",
  "gjennomgaatt": ["KM1638", "KM1640", "KM1643"]
}

Hvilke kompetansemål i samfunnsfag er relevante for et prosjekt om demokrati og valg?
Ta hensyn til at de allerede gjennomgåtte målene ikke trenger å prioriteres.
```

AI-en bruker fortsatt `grep_hent_kompetansemaal` via MCP, men filtrerer nå svaret:
- Peker direkte på **KM1648** (makt i samfunnet) og **KM1652** (politisk system og velferdsstat)
  som de mest relevante neste målene
- Nevner gjennomgåtte KM kun dersom de er direkte relevante som forkunnskaper

---

## Hva demonstrerer dette?

| | Uten Learner Context | Med Learner Context |
|---|---|---|
| **Grep-data** | Alle 19 KM for 10. trinn | Samme 19 KM |
| **AI-svar** | Generisk liste | Tilpasset klassens progresjon |
| **Verdi** | Korrekt, men lite handlingsrettet | Direkte nyttig for læreren |

---

## Hva er simulert?

I en reell LTI-integrasjon ville brukerprofilen blitt sendt automatisk via en **LTI Launch
Message** når læreren åpner AI-verktøyet fra Canvas eller tilsvarende. I denne mockupen
limes den inn manuelt i prompten for å illustrere konseptet.
