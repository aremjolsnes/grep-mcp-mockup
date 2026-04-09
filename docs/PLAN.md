---
tags: [plan, mockup, MCP, Grep, CASE, RAG]
creation-date: 2026-04-09
type: prosjekt
status: ua
topic: [Grep, CASE, MCP, RAG, interoperabilitet]
---

# Mockup-plan: Grep + MCP + Learner Context

> Denne planen gjelder bygging av en teknisk demonstrasjon utenfor Obsidian-hvelvet.
> Koden plasseres i en egen GitHub-repo (opprettes av Are).
> Relatert: [[Taleplan]] | [[3-lags RAG-plan]]

---

## Mål

Demonstrere tre lag i kombinasjon for presentasjonen:

1. **Grep via SPARQL** – henter eksakte kompetansemål
2. **MCP-server** – eksponerer Grep som et AI-verktøy (og kan oversette til CASE)
3. **Learner Context (simulert)** – tilpasser svar til konkret elev/trinn/program

> **Merk:** Learner Context er simulert i mockupen – brukerprofilen hardkodes i prompten, ikke hentet fra et reelt LTI-system. Dette kommuniseres tydelig i presentasjonen.

---

## GraphDB-oppsett

Før kode-utvikling starter, må følgende være på plass i GraphDB Workbench:

1. **Opprett repo:** `grep-mcp-mockup`
2. **Last inn data:** Grep JSON-LD-dump fra `https://data.udir.no/kl06/v201906/dump/jsonld`
3. **Bygg ontologier:** Lag mappinger for CASE/CFItem-konvertering
4. **Eksponér via SPARQL:** Gjør repoet tilgjengelig på `https://sparql-beta-data.udir.no/repositories/grep-mcp-mockup`

> Dette håndteres av Are via Workbench – koden trenger bare å snakke mot det ferdige SPARQL-endpointet.

---

## Steg 1 – MCP-server for Grep

### Hva den skal gjøre
- Ta imot spørringer fra en AI-modell via MCP-protokollen
- Oversette disse til SPARQL-spørringer mot Greps endepunkt
- Returnere strukturerte kompetansemål-data som kontekst til AI-en
- (Valgfritt) Eksponere data i CASE-format ved hjelp av ontologi-mappingen fra [[3-lags RAG-plan]]

### Teknisk stack
- **Python** (FastMCP eller mcp-python SDK)
- **SPARQL** mot GraphDB-repo `grep-mcp-mockup` på `https://sparql-beta-data.udir.no/repositories/grep-mcp-mockup`
- **MCP-verktøy som eksponeres:**
  - `grep_hent_kompetansemaal(fagkode, trinn)` – henter KM for gitt fag og trinn
  - `grep_hent_laereplan(fagkode)` – henter full læreplan
  - `grep_sok(fritekst)` – fritekstsøk mot Grep
  - (Valgfritt) `case_hent_cfitems(fagkode)` – returnerer data i CASE CFItem-format

### Avhengigheter
- [ ] GraphDB-repo `grep-mcp-mockup` opprettet i Workbench
- [ ] Grep JSON-LD-dump lastet inn: `https://data.udir.no/kl06/v201906/dump/jsonld`
- [ ] Ontologi-mappinger for CASE/CFItem laget og bakt inn i repoet
- [ ] MCP Python SDK installert (`pip install mcp`)
- [ ] Test at SPARQL-spørringer returnerer forventet data for SAF1-04

---

## Steg 2 – Learner Context (simulert)

### Hva det skal gjøre
- Legge til brukerprofil som kontekst i prompten til AI-en
- Filtrere Grep-data basert på profilen (trinn, fag, allerede gjennomgåtte KM)

### Demo-scenario
En lærer på 10. trinn spør: *«Hvilke kompetansemål i samfunnsfag er relevante for et prosjekt om demokrati og valg?»*

**Simulert brukerprofil (hardkodet i prompt):**
```json
{
  "rolle": "lærer",
  "trinn": "10",
  "fag": "SAF1-04",
  "gjennomgaatt": ["KM7815", "KM7816"]
}
```

**Forventet oppførsel:**
- Uten Learner Context: AI lister alle 19 KM for 10. trinn
- Med Learner Context: AI peker direkte på KM7817 og KM7819 som neste relevante steg

---

## Steg 3 – CASE-eksponering (valgfritt / avansert)

- Bruk ontologi-mappingen fra [[3-lags RAG-plan]] til å oversette Grep-output til CASE CFItem/CFDocument
- Vis at samme MCP-server kan svare både «norsk Grep-format» og «CASE-format»
- Demonstrerer interoperabilitet uten å endre Grep

---

## Repo-struktur (forslag)

```
grep-mcp-mockup/
├── README.md
├── server/
│   ├── main.py          ← MCP-server
│   ├── sparql.py        ← SPARQL-klient mot Grep
│   └── case_adapter.py  ← (valgfritt) Grep→CASE-oversetter
├── demo/
│   ├── scenario.md      ← Beskrivelse av demo-scenariet
│   └── learner_context.json ← Simulert brukerprofil
└── ontologi/
    └── grep_case_mapping.ttl ← Turtle-fil med OWL/SKOS-mapping
```

---

## Arbeidsrekkefølge

1. Are oppretter GitHub-repo (`grep-mcp-mockup` eller tilsvarende)
2. Sett opp Python-miljø og verifiser SPARQL-tilgang mot Grep
3. Bygg MCP-server med `grep_hent_kompetansemaal`-verktøyet
4. Test med Claude Desktop / Claude Code som MCP-klient
5. Legg til Learner Context-simulering i demo-scenariet
6. (Valgfritt) Bygg CASE-adapteren
7. Dokumenter demo-scenariet i `demo/scenario.md`

---

## Beslutninger

| Spørsmål | Beslutning |
|---|---|
| MCP-klient | Ikke avklart – egen økt på dette |
| Deployment | Deployet – GitHub-repo + Vercel e.l. |
| Grep-data | Egen Grep-triplestore med ny ontologi og bro til CASE (ikke live Grep, ikke ren mock) |
| Kode-lokasjon | `C:\Users\AMJ\git\grep-sandkasse\grep-case-rag` (eget VS Code-prosjekt) |

### MCP-klient – åpent spørsmål
Krever en dedikert gjennomgang. Alternativene som bør vurderes:
- **Claude Desktop** – enklest å demonstrere, innebygd MCP-støtte
- **Claude Code** – bra for teknisk publikum, terminal-basert
- **Egen klient** – mest fleksibel, men mer å bygge

### Triplestore-strategi
Vi bygger en egen Grep-triplestore med:
- Utvalgte data fra Grep (SAF1-04, relevante trinn)
- Ny ontologi tilpasset dette formålet
- Eksplisitt bro til CASE-ontologien (OWL/SKOS-mapping fra [[3-lags RAG-plan]])
- Hostet slik at MCP-serveren kan nå den fra Vercel
