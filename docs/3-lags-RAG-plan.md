---
tags: [research]
creation-date: 2026-04-07 09:00
type: prosjekt
status: ua
topic:
  - Grep
  - CASE
  - RAG
  - AI
  - interoperabilitet
---

# 3-lags RAG-plan

Relatert: [[Research - Grep og CASE interoperabilitet/]] | [[2026-03-30-Møte-Interoperabilitet-Grep-CASE]]

Plan for hvordan Grep og CASE kan kombineres i en RAG-arkitektur for AI-assistert komparativ læreplananalyse.

---

## Tre innfallsvinkler – oversikt

Vi har tre distinkte innfallsvinkler som henger sammen, men kan presenteres uavhengig:

| # | Innfallsvinkel | Poeng | Publikum |
|---|---|---|---|
| 1 | **Grep som RAG-grunnlag** | AI som bruker Grep hallusinerer ikke læreplaner | Bredt – alle |
| 2 | **AI-generert crosswalk: Grep ↔ Nevada** | Strukturerte data gjør komparativ analyse mulig på tvers av land | Pedagoger, policyfolk |
| 3 | **Ontologi-mapping som bro** | En adapter kan eksponere Grep som CASE uten å endre Grep | Tim Couper, teknisk publikum |

### Sammenheng

```
Ontologi-mapping (3)
      ↓ gjør mulig
Grep→CASE-adapter
      ↓ gir data til
RAG (1) + Crosswalk (2)
      ↓ brukes av
AI som svarer presist om norske og internasjonale læreplaner
```

---

## Innfallsvinkel 1: Grep som RAG-grunnlag

En RAG trenger en **retriever** og en **generator**. For Grep er det naturlige valget:

- **Retriever:** SPARQL-endepunktet *er* retrieveren. I stedet for vektordatabase henter man strukturerte RDF-data direkte. Det gir *presis* gjenfinning – ikke fuzzy embedding-søk.
- **Generator:** En LLM (GPT-4, Claude osv.) som får Grep-data som kontekst i prompten.

Flyten:
```
Bruker spør: "Hva sier norsk læreplan om kildekritikk i 10. klasse?"
       ↓
SPARQL-spørring mot Grep → returnerer KM-kode, tittel, kompetansemålsett,
trinn, læreplan-tittel, og tilknyttede kjerneelementer (kode + tittel)
       ↓
LLM får: [spørsmål] + [Grep-data som kontekst]
       ↓
Svar basert på faktisk læreplandata – ikke hallusinert
```

**Nøkkelpoeng:** Grep er allerede maskinlesbart. Det *er* grunnlaget for en RAG, uten at man trenger å skrape PDFer eller bygge vektordatabase fra scratch.

### Status: implementert

- [x] SPARQL-spørring mot Grep via `sparql.py` (`hent_kompetansemaal`, `sok_kompetansemaal`)
- [x] Returnerte felt: KM-kode, tittel, kompetansemålsett, trinn, læreplan-tittel, og tilknyttede kjerneelementer (kode + tittel, pipe-separert via `GROUP_CONCAT`)
- [x] MCP-server (`server/main.py`) eksponerer Grep-data som AI-verktøy (`grep_hent_kompetansemaal`, `grep_sok_kompetansemaal`)
- [x] Tre-stegs live demo kjørt med Claude som AI – se `demo/scenario.md`

---

## Innfallsvinkel 2: AI-generert crosswalk: Grep ↔ Nevada

### Anker-eksempel

| Grep | Tittel (nb) | CASE | fullStatement |
|---|---|---|---|
| KM1637 | "vurdere på hvilke måter ulike kilder gir informasjon om et samfunnsfaglig tema..." | SS.9-12.CE.1 | "When constructing compelling questions, reference points of agreement and disagreement..." |

Begge handler om kildebevissthet, faglig tenking og perspektivmangfold. Nevada er videregående (9–12), Grep er 10. trinn – nesten samme alder, nesten samme ambisjon.

### Volum

| | Antall |
|---|---|
| Grep SAF01-04 kompetansemål | **62** (13 + 13 + 17 + 19 fordelt på 2., 4., 7., 10. trinn) |
| Nevada Social Studies – trinnstruktur | KG–12, organisert i 9 toppnoder |
| Mest relevant å sammenligne | Grep 10. trinn ↔ Nevada 9–12 / Grep 7. trinn ↔ Nevada 6–8 |

Nevada-data hentes fra `opensalt.net/uri/{uuid}.json` (speiler satchelcommons.com).

### Steg 1 – Hent data

```python
# Grep: alle 62 KM via SPARQL eller REST API
# SPARQL-repoet bygger på REST-APIet – alt som finnes i REST, finnes også i SPARQL
# Via SPARQL (som i sparql.py): hent_kompetansemaal("SAF01-04", "")
# Via REST: GET https://data.udir.no/kl06/v201906/kompetansemaal-lk20/{kode}
# → kode, tittel, aarstrinn, kjerneelementer

# Nevada: alle CFItems av type "Disciplinary Skills Standard"
GET https://opensalt.net/uri/{uuid}.json
# → fullStatement, humanCodingScheme, educationLevel, CFItemType
```

### Steg 2 – Bygg prompt

Send begge lister til LLM med prompt:

> "Her er alle norske kompetansemål i samfunnsfag (Grep SAF01-04) og alle Nevada Social Studies standards. For hvert norske kompetansemål, finn det Nevada-elementet som matcher best semantisk. Angi matchkvalitet (høy / middels / lav) og en kort begrunnelse."

Kjøres gjerne trinnvis:
- Grep 10. trinn (19 KM) ↔ Nevada 9–12
- Grep 7. trinn (17 KM) ↔ Nevada 6–8
- osv.

### Steg 3 – Output

| Grep-kode | Grep-tittel (forkortet) | Nevada-kode | Nevada-fullStatement (forkortet) | Match |
|---|---|---|---|---|
| KM1637 | "vurdere på hvilke måter ulike kilder..." | SS.9-12.CE.1 | "When constructing compelling questions..." | Høy |
| ... | ... | ... | ... | ... |

### Demo-todo
- [ ] Hent alle Nevada CFItems av type `Disciplinary Skills Standard` for 6–8 og 9–12 og lagre som JSON
- [ ] Hent alle 62 Grep SAF-kompetansemål og lagre som JSON
- [ ] Kjør AI-mapping trinnvis og bygg crosswalk-tabell
- [ ] Vurder om output egner seg som `skos:closeMatch`-tripler i Turtle

---

## Innfallsvinkel 3: Ontologi-mapping som bro

Mappingen uttrykkes **deklarativt i ontologien** – som RDF-tripler. Dette gir en normativ, maskinlesbar beskrivelse av koblingen mellom Grep og CASE. I mockupen er dette realisert i to lag: ontologien som deklarasjon, og `case_adapter.py` som oversetter Grep SPARQL-bindings til CASE-strukturer i kjøretid.

```turtle
@prefix u:    <http://psi.udir.no/ontologi/kl06/> .
@prefix case: <https://purl.imsglobal.org/spec/case/v1p0/vocab#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

# Klasse-mapping
u:Kompetansemaal     owl:equivalentClass  case:CFItem .
u:Laereplan          owl:equivalentClass  case:CFDocument .
u:Kompetansemaalsett skos:closeMatch      case:CFPackage .

# Egenskap-mapping
u:kode               skos:exactMatch      case:humanCodingScheme .
u:tittel             skos:exactMatch      case:fullStatement .
```

### Valg av mapping-styrke

| Konstrukt | Betydning | Eksempel |
|---|---|---|
| `owl:equivalentClass` | Identisk klasse | `u:Kompetansemaal` ↔ `case:CFItem`, `u:Laereplan` ↔ `case:CFDocument` |
| `skos:exactMatch` | Semantisk identisk på tvers av vokabularer | `u:kode` ↔ `case:humanCodingScheme`, `u:tittel` ↔ `case:fullStatement` |
| `skos:closeMatch` | Nær, men ikke identisk | `u:Kompetansemaalsett` ↔ `case:CFPackage` – trinn-dimensjonen har ingen direkte CASE-ekvivalent |

### Konsekvens: Grep→CASE-adapter

Ontologi-mappingen er realisert i to lag:

**Lag 1 – deklarativ ontologi** (`ontologi/grep_case_mapping.ttl`): Definerer koblingene som RDF-tripler, lastet inn i GraphDB.

**Lag 2 – MCP-verktøy** (`server/case_adapter.py` + `server/main.py`): Oversetter Grep SPARQL-bindings til CASE CFDocument/CFItem-struktur i kjøretid.

```
Grep SPARQL-endepunkt (GraphDB)
      ↓
MCP-server → grep_hent_cfitems() → case_adapter.py
      ↓  returnerer:  CASE CFDocument
      ↓               CASE CFItems
AI-modell (Claude via MCP-klient)
```

**Effekt:** Norske kompetansemål eksponeres i CASE-format til AI-modellen – uten at Grep selv endres. En fremtidig REST-adapter (OpenSALT-instans e.l.) kan bruke samme ontologi-mapping til å eksponere `/ims/case/v1p0/CFDocuments` for Google Classroom og andre CASE-kompatible systemer.

### Status: implementert

- [x] Ontologi-tripler skrevet som to Turtle-filer: `ontologi/grep_ontologi.ttl` (normativ OWL) og `ontologi/grep_case_mapping.ttl` (broaksiomer)
- [x] Begge filer lastet inn i GraphDB (default graph)
- [x] MCP-verktøy `grep_hent_cfitems` implementert med `case_adapter.py`
- [x] Live demo kjørt – CASE CFDocument med CFItems returnert for SAF01-04, 10. trinn
- [ ] Vurder om ontologien kan inngå i Greps eksisterende OWL-ontologi (fremtidig steg)
- [ ] REST-adapter for eksponering mot CASE Network / Google Classroom (fremtidig steg)

---

## Relaterte notater
- [[Research - Grep og CASE interoperabilitet]]
- [[Grep]]
- [[SPARQL]]
