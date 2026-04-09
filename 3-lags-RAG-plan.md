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
SPARQL-spørring mot Grep → returnerer KM1637, kjerneelementer, tilhørende læreplan
       ↓
LLM får: [spørsmål] + [Grep-data som kontekst]
       ↓
Svar basert på faktisk læreplandata – ikke hallusinert
```

**Nøkkelpoeng:** Grep er allerede maskinlesbart. Det *er* grunnlaget for en RAG, uten at man trenger å skrape PDFer eller bygge vektordatabase fra scratch.

### Demo-todo
- [ ] SPARQL-spørring som henter KM1637 med alle metadata (tittel, kode, trinn, kjerneelementer, læreplan)
- [ ] Prompt-konstruert kontekst sendt til LLM – vise svar vs. hallusinasjon

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
# Grep: alle 62 KM via REST
GET https://data.udir.no/kl06/v201906/kompetansemaal-lk20/{kode}
# → tittel (nob), kode, aarstrinn, kjerneelementer

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

I stedet for å bygge en adapter med hardkodet konverteringslogikk, uttrykkes mappingen **deklarativt i ontologien** – som RDF-tripler. Da er det ontologien som gjør jobben, ikke kode.

```turtle
PREFIX grep: <http://psi.udir.no/ontologi/kl06/>
PREFIX case: <https://purl.imsglobal.org/spec/case/v1p1/schema/context/>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

# Klasse-mapping
grep:Kompetansemaal  owl:equivalentClass  case:CFItem .
grep:Laereplan       owl:equivalentClass  case:CFDocument .

# Egenskap-mapping
grep:tittel          skos:closeMatch          case:fullStatement .
grep:kode            owl:equivalentProperty   case:humanCodingScheme .
grep:aarstrinn       owl:equivalentProperty   case:educationLevel .
grep:id              owl:equivalentProperty   case:identifier .
```

### Valg av mapping-styrke

| Konstrukt | Betydning | Eksempel |
|---|---|---|
| `owl:equivalentProperty` | Identisk semantikk | `grep:kode` ↔ `case:humanCodingScheme` |
| `owl:equivalentClass` | Identisk klasse | `grep:Kompetansemaal` ↔ `case:CFItem` |
| `skos:closeMatch` | Nær, men ikke identisk | `grep:tittel` ↔ `case:fullStatement` – Greps tittel er kortere og mer normativ |

### Konsekvens: Grep→CASE-adapter

En ekstern tjeneste bruker disse triplene til automatisk å eksponere Grep-data som gyldige CASE-strukturer:

```
Grep REST/SPARQL
      ↓
Grep→CASE-adapter (bruker ontologi-mappingen)
      ↓  eksponerer:  /ims/case/v1p1/CFDocuments
      ↓               /ims/case/v1p1/CFItems
      ↓               /ims/case/v1p1/CFPackages
CASE Network / Google Classroom
```

**Effekt:** Norske kompetansemål blir søkbare og tagbare i Google Classroom på linje med amerikanske standarder – uten at Grep selv endres.

### Demo-todo
- [ ] Skriv ontologi-triplene som en egen Turtle-fil
- [ ] Vurder om dette kan inngå i Greps eksisterende OWL-ontologi
- [ ] Skisser adapter-arkitektur (OpenSALT-instans eller enkel Flask-tjeneste)

---

## Relaterte notater
- [[Research - Grep og CASE interoperabilitet]]
- [[Grep]]
- [[SPARQL]]
