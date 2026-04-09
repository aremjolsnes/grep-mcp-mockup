# Demo-scenario: Demokrati og valg på 10. trinn

## Bakgrunn

Dette scenariet demonstrerer tre lag i kombinasjon:

| Lag | Teknologi | Rolle |
|---|---|---|
| **1. Grep via SPARQL** | GraphDB + MCP-server | Henter eksakte kompetansemål fra Greps triplestore |
| **2. MCP-server** | FastMCP + Python | Eksponerer Grep som AI-verktøy – i Grep-format og CASE-format |
| **3. Learner Context** | Simulert brukerprofil | Tilpasser AI-svaret til klassens konkrete situasjon |

---

## Spørsmål fra lærer

> «Hvilke kompetansemål i samfunnsfag er relevante for et prosjekt om demokrati og valg?»

---

## Steg 1 – Grep via MCP, uten Learner Context

AI-en bruker MCP-verktøyet `grep_hent_kompetansemaal("SAF01-04", "10")` og henter alle
19 kompetansemål for 10. trinn direkte fra Greps triplestore.

**Eksempel på AI-svar:**

> Her er kompetansemålene i samfunnsfag (SAF01-04) for 10. trinn som er relevante for
> et prosjekt om demokrati og valg:
>
> - **KM1648** – reflektere over kva for aktørar som har makt i samfunnet i dag, og korleis
>   desse grunngir standpunkta sine
> - **KM1652** – beskrive trekk ved det politiske systemet og velferdssamfunnet i Noreg i dag
>   og reflektere over sentrale utfordringar
> - **KM1650** – reflektere over korleis menneske har kjempa og kjempar for endringar i
>   samfunnet og samstundes har vore og er påverka av geografiske forhold og historisk kontekst
> - **KM1651** – beskrive sentrale lover, reglar og normer og drøfte kva konsekvensar brot på
>   desse kan ha for den enkelte og for samfunnet
> - *(+ 15 øvrige KM for 10. trinn)*

Svaret er korrekt, men generisk – AI-en vet ikke hva klassen allerede har gjennomgått.

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

AI-en bruker fortsatt `grep_hent_kompetansemaal` via MCP, men tilpasser svaret til profilen.

**Eksempel på AI-svar:**

> Basert på klassens progresjon anbefaler jeg å prioritere disse kompetansemålene:
>
> **Neste steg – direkte relevante for prosjektet:**
> - **KM1648** – makt i samfunnet (hvem bestemmer, og hvordan begrunnes det?)
> - **KM1652** – det politiske systemet og velferdssamfunnet i Norge
>
> **Støttende – kan trekkes inn som forkunnskaper:**
> - KM1643 (mangfold og identitet, allerede gjennomgått) – nyttig som inngang til
>   diskusjon om demokratiske verdier
>
> KM1638 (teknologi) og KM1640 (geografi/levekår) er gjennomgått og trenger ikke
> prioriteres, men kan nevnes som kontekst ved behov.

Svaret er presist og handlingsrettet – AI-en peker direkte på neste relevante steg.

---

## Steg 3 – CASE-format via MCP

For systemer som kommuniserer via CASE-standarden kan AI-en bruke
`grep_hent_cfitems("SAF01-04", "10")` i stedet. Dette returnerer nøyaktig samme
Grep-data, men strukturert som CASE CFDocument med CFItems.

**Utdrag fra responsen:**

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

Samme MCP-server – to formater. Grep-strukturen er uendret.

---

## Sammenligning

| | Steg 1 | Steg 2 | Steg 3 |
|---|---|---|---|
| **Verktøy** | `grep_hent_kompetansemaal` | `grep_hent_kompetansemaal` | `grep_hent_cfitems` |
| **Grep-data** | Alle 19 KM for 10. trinn | Samme 19 KM | Samme 19 KM |
| **Format** | Grep-format | Grep-format | CASE CFItem |
| **Learner Context** | Nei | Ja (simulert) | Valgfritt |
| **AI-svar** | Generisk liste | Tilpasset progresjon | Maskinlesbar standard |
| **Verdi** | Korrekt, men lite handlingsrettet | Direkte nyttig for læreren | Interoperabelt med andre systemer |

---

## Hva er simulert?

**Learner Context:** I en reell LTI-integrasjon ville brukerprofilen blitt sendt automatisk
via en **LTI Launch Message** når læreren åpner AI-verktøyet fra Canvas eller tilsvarende.
I denne mockupen limes den inn manuelt i prompten for å illustrere konseptet.
Dette er det «manglende leddet» som et ekte LTI-oppsett ville fylt inn automatisk.

**Grep-data:** Hentet live fra Greps triplestore via SPARQL – ikke mocket.

**CASE-format:** Generert i MCP-serveren ved hjelp av ontologi-mappingen i
`ontologi/grep_case_mapping.ttl`. Ingen endringer i Grep.
