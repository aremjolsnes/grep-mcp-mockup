# grep-mcp-mockup

Mockup for MCP + Grep + Learner Context.

## Prosjektstruktur

```
grep-mcp-mockup/
├── README.md
├── requirements.txt
├── docs/                    # Planleggingsdokumenter
│   ├── PLAN.md             # Hovedplan for mockupen
│   ├── 3-lags-RAG-plan.md  # Teknisk RAG-plan
│   └── Taleplan.md         # Presentasjonsplan
├── server/                 # MCP-server kode
│   └── sparql.py           # SPARQL-klient mot GraphDB
├── demo/                   # Demo-scenarioer (kommer)
└── ontologi/               # Ontologi-mappinger (kommer)
```

## SPARQL endpoint

Denne repoen bruker GraphDB-repoet `grep-mcp-mockup` eksponert via:

`https://sparql-beta-data.udir.no/repositories/grep-mcp-mockup`

## Oppsett

1. **GraphDB-repo:** Opprett `grep-mcp-mockup` i Workbench
2. **Last inn data:** Grep JSON-LD fra `https://data.udir.no/kl06/v201906/dump/jsonld`
3. **Bygg ontologier:** Legg til CASE-mappinger
4. **Kjør kode:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   python server/sparql.py  # Test SPARQL-tilkobling
   ```

## Neste steg

1. Bygg GraphDB-repoet med Grep-data og ontologier
2. Lag `server/main.py` – MCP-server som eksponerer Grep-funksjoner
3. Lag `demo/learner_context.json` – simulert brukerprofil
4. Lag `demo/scenario.md` – demo-scenario beskrivelse
