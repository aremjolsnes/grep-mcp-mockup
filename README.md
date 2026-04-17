# grep-mcp-mockup

Technical demonstration of three layers working in combination:

1. **Grep via SPARQL** – retrieves exact competence aims from Grep's triplestore
2. **MCP server** – exposes Grep as an AI tool
3. **Learner Context (simulated)** – tailors responses to a specific student/grade/subject

## Project structure

```
grep-mcp-mockup/
├── README.md
├── requirements.txt
├── .mcp.json                   # MCP configuration for Claude Code
├── docs/
│   ├── PLAN.md                 # Main project plan
│   ├── 3-lags-RAG-plan.md      # Technical RAG plan
├── server/
│   ├── main.py                 # MCP server (FastMCP)
│   ├── sparql.py               # SPARQL client for GraphDB
│   └── case_adapter.py         # Grep → CASE format adapter
├── demo/                       # Demo scenarios and prompts
└── ontologi/                   # Ontology files and mappings
```

## SPARQL endpoint

The repo uses the GraphDB repository `grep-mcp-mockup` exposed via:

```
https://sparql-beta-data.udir.no/repositories/grep-mcp-mockup
```

## Setup

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python server/sparql.py   # Test SPARQL connectivity
python server/main.py     # Start MCP server
```

## Claude Code setup

The repo includes `.mcp.json` which registers the MCP server automatically when you open the project in Claude Code.

You also need a local permissions config that is **not** included in the repo (it is machine-specific). Create it manually:

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

Without this file, Claude Code will prompt for permission on every tool call during the demo.

## MCP tools

The server exposes three tools:

| Tool | Description |
|---|---|
| `grep_hent_kompetansemaal(laereplan_kode, trinn)` | Fetch competence aims for a given curriculum and grade |
| `grep_sok_kompetansemaal(fritekst, maks_treff)` | Full-text search across all competence aims |
| `grep_hent_cfitems(laereplan_kode, trinn)` | Fetch competence aims in CASE CFItem format |

## Learner Context

### What is Learner Context?

"Learner Context" is not a single formal standard term, but a concept rooted in the **1EdTech** ecosystem — primarily from two standards:

- **LTI (Learning Tools Interoperability):** Delivers context about *who* and *where* — role, course, and institution — via a Launch Message when an external app is opened from e.g. Canvas. The app then knows whether the user is a `Learner` or `Instructor` in that situation.

- **CASE (Competencies & Academic Standards Exchange):** Delivers context about *what* — which competence aims apply to the student, grade, and subject. This ties the student's work closely to curriculum requirements.

The goal in the 1EdTech world is **data portability**: the student's needs, preferences, and achieved competencies should follow the student across tools, rather than being locked into a single system.

### In this mockup

Learner Context is **simulated** — the user profile is hardcoded in the prompt rather than retrieved from a real LTI system. This is the "missing link" that a real LTI setup would fill in automatically at launch.

```json
{
  "rolle": "lærer",
  "trinn": "10",
  "fag": "SAF01-04",
  "gjennomgaatt": ["KM7815", "KM7816"]
}
```

This is made explicit in the demo.
