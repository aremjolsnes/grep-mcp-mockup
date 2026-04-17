# Three-layer RAG plan

Plan for how Grep and CASE can be combined in a RAG architecture for AI-assisted comparative curriculum analysis.

---

## Three angles — overview

Three distinct angles that are connected but can be presented independently:

| # | Angle | Point | Audience |
|---|---|---|---|
| 1 | **Grep as RAG foundation** | AI using Grep does not hallucinate curricula | Broad — everyone |
| 2 | **AI-generated crosswalk: Grep ↔ Nevada** | Structured data enables comparative analysis across countries | Educators, policy people |
| 3 | **Ontology mapping as bridge** | An adapter can expose Grep as CASE without modifying Grep | Tim Couper, technical audience |

### How they connect

```
Ontology mapping (3)
      ↓ enables
Grep→CASE adapter
      ↓ provides data to
RAG (1) + Crosswalk (2)
      ↓ used by
AI that answers precisely about Norwegian and international curricula
```

---

## Angle 1: Grep as RAG foundation

A RAG needs a **retriever** and a **generator**. For Grep the natural choice is:

- **Retriever:** The SPARQL endpoint *is* the retriever. Instead of a vector database, structured RDF data is fetched directly. This gives *precise* retrieval — not fuzzy embedding search.
- **Generator:** An LLM (GPT-4, Claude, etc.) that receives Grep data as context in the prompt.

Flow:
```
User asks: "What does the Norwegian curriculum say about source criticism in grade 10?"
       ↓
SPARQL query against Grep → returns competence aim code, title, competence aim set,
grade, curriculum title, and associated core elements (code + title)
       ↓
LLM receives: [question] + [Grep data as context]
       ↓
Answer based on actual curriculum data — not hallucinated
```

**Key point:** Grep is already machine-readable. It *is* the foundation for a RAG, without needing to scrape PDFs or build a vector database from scratch.

### Status: implemented

- [x] SPARQL query against Grep via `sparql.py` (`hent_kompetansemaal`, `sok_kompetansemaal`)
- [x] Returned fields: competence aim code, title, competence aim set, grade, curriculum title, and associated core elements (code + title, pipe-separated via `GROUP_CONCAT`)
- [x] MCP server (`server/main.py`) exposes Grep data as AI tools (`grep_hent_kompetansemaal`, `grep_sok_kompetansemaal`)
- [x] Three-step live demo run with Claude as AI — see `demo/scenario.md`

---

## Angle 2: AI-generated crosswalk: Grep ↔ Nevada

### Anchor example

| Grep | Title (nb) | CASE | fullStatement |
|---|---|---|---|
| KM1637 | "vurdere på hvilke måter ulike kilder gir informasjon om et samfunnsfaglig tema..." | SS.9-12.CE.1 | "When constructing compelling questions, reference points of agreement and disagreement..." |

Both deal with source awareness, disciplinary thinking, and perspective diversity. Nevada is high school (9–12), Grep is grade 10 — nearly the same age, nearly the same ambition.

### Volume

| | Count |
|---|---|
| Grep SAF01-04 competence aims | **62** (13 + 13 + 17 + 19 across grades 2, 4, 7, 10) |
| Nevada Social Studies — grade structure | KG–12, organised in 9 top nodes |
| Most relevant to compare | Grep grade 10 ↔ Nevada 9–12 / Grep grade 7 ↔ Nevada 6–8 |

Nevada data fetched from `opensalt.net/uri/{uuid}.json` (mirrors satchelcommons.com).

### Step 1 – Fetch data

```python
# Grep: all 62 competence aims via SPARQL or REST API
# The SPARQL repo builds on the REST API — everything in REST is also in SPARQL
# Via SPARQL (as in sparql.py): hent_kompetansemaal("SAF01-04", "")
# Via REST: GET https://data.udir.no/kl06/v201906/kompetansemaal-lk20/{code}
# → code, title, grade, core elements

# Nevada: all CFItems of type "Disciplinary Skills Standard"
GET https://opensalt.net/uri/{uuid}.json
# → fullStatement, humanCodingScheme, educationLevel, CFItemType
```

### Step 2 – Build prompt

Send both lists to the LLM with prompt:

> "Here are all Norwegian competence aims in social studies (Grep SAF01-04) and all Nevada Social Studies standards. For each Norwegian competence aim, find the Nevada element that matches best semantically. Indicate match quality (high / medium / low) and a brief justification."

Run step by step:
- Grep grade 10 (19 aims) ↔ Nevada 9–12
- Grep grade 7 (17 aims) ↔ Nevada 6–8
- etc.

### Step 3 – Output

| Grep code | Grep title (shortened) | Nevada code | Nevada fullStatement (shortened) | Match |
|---|---|---|---|---|
| KM1637 | "vurdere på hvilke måter ulike kilder..." | SS.9-12.CE.1 | "When constructing compelling questions..." | High |
| ... | ... | ... | ... | ... |

### Demo todo
- [ ] Fetch all Nevada CFItems of type `Disciplinary Skills Standard` for 6–8 and 9–12 and save as JSON
- [ ] Fetch all 62 Grep SAF competence aims and save as JSON
- [ ] Run AI mapping step by step and build crosswalk table
- [ ] Consider whether output is suitable as `skos:closeMatch` triples in Turtle

---

## Angle 3: Ontology mapping as bridge

The mapping is expressed **declaratively in the ontology** — as RDF triples. This provides a normative, machine-readable description of the connection between Grep and CASE. In the mockup this is realised in two layers: the ontology as declaration, and `case_adapter.py` as runtime translator.

```turtle
@prefix u:    <http://psi.udir.no/ontologi/kl06/> .
@prefix case: <https://purl.imsglobal.org/spec/case/v1p0/vocab#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

# Class mappings
u:Kompetansemaal     owl:equivalentClass  case:CFItem .
u:Laereplan          owl:equivalentClass  case:CFDocument .
u:Kompetansemaalsett skos:closeMatch      case:CFPackage .

# Property mappings
u:kode               skos:exactMatch      case:humanCodingScheme .
u:tittel             skos:exactMatch      case:fullStatement .
```

### Choice of mapping strength

| Construct | Meaning | Example |
|---|---|---|
| `owl:equivalentClass` | Identical class | `u:Kompetansemaal` ↔ `case:CFItem`, `u:Laereplan` ↔ `case:CFDocument` |
| `skos:exactMatch` | Semantically identical across vocabularies | `u:kode` ↔ `case:humanCodingScheme`, `u:tittel` ↔ `case:fullStatement` |
| `skos:closeMatch` | Close, but not identical | `u:Kompetansemaalsett` ↔ `case:CFPackage` — the grade dimension has no direct CASE equivalent |

### Consequence: Grep→CASE adapter

The ontology mapping is realised in two layers:

**Layer 1 — declarative ontology** (`ontologi/grep_case_mapping.ttl`): Defines the mappings as RDF triples, loaded into GraphDB.

**Layer 2 — MCP tool** (`server/case_adapter.py` + `server/main.py`): Translates Grep SPARQL bindings to CASE CFDocument/CFItem structures at runtime.

```
Grep SPARQL endpoint (GraphDB)
      ↓
MCP server → grep_hent_cfitems() → case_adapter.py
      ↓  returns:  CASE CFDocument
      ↓            CASE CFItems
AI model (Claude via MCP client)
```

**Effect:** Norwegian competence aims are exposed in CASE format to the AI model — without modifying Grep itself. A future REST adapter (OpenSALT instance etc.) could use the same ontology mapping to expose `/ims/case/v1p0/CFDocuments` for Google Classroom and other CASE-compatible systems.

### Status: implemented

- [x] Ontology triples written as two Turtle files: `ontologi/grep_ontologi.ttl` (normative OWL) and `ontologi/grep_case_mapping.ttl` (bridge axioms)
- [x] Both files loaded into GraphDB (default graph)
- [x] MCP tool `grep_hent_cfitems` implemented with `case_adapter.py`
- [x] Live demo run — CASE CFDocument with CFItems returned for SAF01-04, grade 10
- [ ] Consider whether the ontology can be incorporated into Grep's existing OWL ontology (future step)
- [ ] REST adapter for exposure to CASE Network / Google Classroom (future step)
