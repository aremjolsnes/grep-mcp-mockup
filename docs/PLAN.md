# Project plan: Grep + MCP + Learner Context

Technical demonstration of three layers working in combination.

---

## Goals

Demonstrate three layers in combination:

1. **Grep via SPARQL** – retrieves exact competence aims
2. **MCP server** – exposes Grep as an AI tool (and can translate to CASE)
3. **Learner Context (simulated)** – tailors responses to a specific student/grade/subject

> **Note:** Learner Context is simulated in the mockup — the user profile is hardcoded in the prompt, not retrieved from a real LTI system. This is made explicit in the demo.

---

## GraphDB setup

Before code development begins, the following must be in place in GraphDB Workbench:

1. **Create repo:** `grep-mcp-mockup`
2. **Load data:** Grep JSON-LD dump from `https://data.udir.no/kl06/v201906/dump/jsonld`
3. **Build ontologies:** Create mappings for CASE/CFItem conversion
4. **Expose via SPARQL:** Make the repo available at `https://sparql-beta-data.udir.no/repositories/grep-mcp-mockup`

> This is handled by Are via Workbench — the code only needs to talk to the finished SPARQL endpoint.

---

## Step 1 – MCP server for Grep

### What it should do
- Accept queries from an AI model via the MCP protocol
- Translate these into SPARQL queries against Grep's endpoint
- Return structured competence aim data as context to the AI
- (Optional) Expose data in CASE format using the ontology mapping

### Technical stack
- **Python** (FastMCP or mcp-python SDK)
- **SPARQL** against GraphDB repo `grep-mcp-mockup` at `https://sparql-beta-data.udir.no/repositories/grep-mcp-mockup`
- **MCP tools exposed:**
  - `grep_hent_kompetansemaal(fagkode, trinn)` – fetches competence aims for a given subject and grade
  - `grep_hent_laereplan(fagkode)` – fetches full curriculum
  - `grep_sok_kompetansemaal(fritekst)` – full-text search against Grep
  - (Optional) `grep_hent_cfitems(fagkode, trinn)` – returns data in CASE CFItem format

### Dependencies
- [ ] GraphDB repo `grep-mcp-mockup` created in Workbench
- [ ] Grep JSON-LD dump loaded: `https://data.udir.no/kl06/v201906/dump/jsonld`
- [ ] Ontology mappings for CASE/CFItem created and loaded into the repo
- [ ] MCP Python SDK installed (`pip install mcp`)
- [ ] Verify that SPARQL queries return expected data for SAF01-04

---

## Step 2 – Learner Context (simulated)

### What it should do
- Add a user profile as context in the prompt to the AI
- Filter Grep data based on the profile (grade, subject, already covered competence aims)

### Demo scenario
A teacher in grade 10 asks: *"Which competence aims in social studies are relevant for a project on democracy and elections?"*

**Simulated user profile (hardcoded in prompt):**
```json
{
  "rolle": "lærer",
  "trinn": "10",
  "fag": "SAF01-04",
  "gjennomgaatt": ["KM7815", "KM7816"]
}
```

**Expected behaviour:**
- Without Learner Context: AI lists all 19 competence aims for grade 10
- With Learner Context: AI points directly to KM7817 and KM7819 as the next relevant steps

---

## Step 3 – CASE exposure (optional / advanced)

- Use the ontology mapping to translate Grep output to CASE CFItem/CFDocument
- Show that the same MCP server can respond in both "Norwegian Grep format" and "CASE format"
- Demonstrates interoperability without modifying Grep

---

## Repository structure

```
grep-mcp-mockup/
├── README.md
├── server/
│   ├── main.py          ← MCP server
│   ├── sparql.py        ← SPARQL client for Grep
│   └── case_adapter.py  ← Grep→CASE translator
├── demo/
│   ├── scenario.md      ← Demo scenario description
│   └── learner_context.json ← Simulated user profile
└── ontologi/
    └── grep_case_mapping.ttl ← Turtle file with OWL/SKOS mapping
```

---

## Work order

1. Are creates GitHub repo (`grep-mcp-mockup`)
2. Set up Python environment and verify SPARQL access to Grep
3. Build MCP server with `grep_hent_kompetansemaal` tool
4. Test with Claude Code as MCP client
5. Add Learner Context simulation to the demo scenario
6. (Optional) Build CASE adapter
7. Document demo scenario in `demo/scenario.md`

---

## Decisions

| Question | Decision |
|---|---|
| MCP client | Claude Code |
| Deployment | GitHub repo + GraphDB at sparql-beta-data.udir.no |
| Grep data | Dedicated Grep triplestore with new ontology and bridge to CASE (not live Grep, not pure mock) |

### Triplestore strategy
We build a dedicated Grep triplestore with:
- Selected data from Grep (SAF01-04, relevant grades)
- New ontology tailored to this purpose
- Explicit bridge to the CASE ontology (OWL/SKOS mapping)
- Hosted so the MCP server can reach it
