# grep-mcp-mockup

Teknisk demonstrasjon av tre lag i kombinasjon:

1. **Grep via SPARQL** – henter eksakte kompetansemål fra Greps triplestore
2. **MCP-server** – eksponerer Grep som et AI-verktøy
3. **Learner Context (simulert)** – tilpasser svar til konkret elev/trinn/fag

## Prosjektstruktur

```
grep-mcp-mockup/
├── README.md
├── requirements.txt
├── .mcp.json                   # MCP-konfigurasjon for Claude Code
├── docs/
│   ├── PLAN.md                 # Hovedplan for mockupen
│   ├── 3-lags-RAG-plan.md      # Teknisk RAG-plan
│   └── Taleplan.md             # Presentasjonsplan
├── server/
│   ├── main.py                 # MCP-server (FastMCP)
│   └── sparql.py               # SPARQL-klient mot GraphDB
├── demo/                       # Demo-scenarioer (kommer)
└── ontologi/                   # Ontologi-mappinger (kommer)
```

## SPARQL-endepunkt

Repoet bruker GraphDB-repoet `grep-mcp-mockup` eksponert via:

```
https://sparql-beta-data.udir.no/repositories/grep-mcp-mockup
```

## Oppsett

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python server/sparql.py   # Test SPARQL-tilkobling
python server/main.py     # Start MCP-server
```

## Claude Code-oppsett

Repoet inkluderer `.mcp.json` som registrerer MCP-serveren automatisk når du åpner prosjektet i Claude Code.

I tillegg trenger du en lokal tillatelseskonfig som **ikke** er inkludert i repoet (siden den er maskinspesifikk). Opprett filen manuelt:

```bash
mkdir -p .claude
```

`.claude/settings.local.json`:
```json
{
  "permissions": {
    "allow": [
      "mcp__grep__grep_hent_kompetansemaal",
      "mcp__grep__grep_hent_cfitems",
      "mcp__grep__grep_sok_kompetansemaal"
    ]
  }
}
```

Uten denne filen vil Claude Code be om tillatelse ved hvert verktøykall under demoen.

## MCP-verktøy

Serveren eksponerer to verktøy:

| Verktøy | Beskrivelse |
|---|---|
| `grep_hent_kompetansemaal(laereplan_kode, trinn)` | Henter KM for gitt læreplan og trinn |
| `grep_sok_kompetansemaal(fritekst, maks_treff)` | Fritekstsøk på tvers av alle KM |

## Learner Context

### Hva er Learner Context?

"Learner Context" er ikke én formell standardterm, men et konsept som springer ut av **1EdTech**-økosystemet – primært fra to standarder:

- **LTI (Learning Tools Interoperability):** Leverer kontekst om *hvem* og *hvor* – rolle, kurs og institusjon – via en Launch Message når en ekstern app åpnes fra f.eks. Canvas. Appen vet da om brukeren er `Learner` eller `Instructor` i den gitte situasjonen.

- **CASE (Competencies & Academic Standards Exchange):** Leverer kontekst om *hva* – hvilke kompetansemål som gjelder for eleven, trinnet og faget. Dette kobler elevens arbeid tett mot faglige krav.

Målet i 1EdTech-verdenen er **dataportabilitet**: elevens behov, preferanser og oppnådde kompetanse skal følge eleven på tvers av verktøy, i stedet for å være låst inne i ett enkelt system.

### I denne mockupen

Learner Context er **simulert** – brukerprofilen hardkodes i prompten i stedet for å hentes fra et reelt LTI-system. Dette er det "manglende leddet" som et ekte LTI-oppsett ville fylt inn automatisk ved oppstart.

```json
{
  "rolle": "lærer",
  "trinn": "10",
  "fag": "SAF01-04",
  "gjennomgaatt": ["KM7815", "KM7816"]
}
```

Dette kommuniseres tydelig i presentasjonen.
