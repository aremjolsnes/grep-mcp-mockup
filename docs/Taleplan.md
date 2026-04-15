---
tags: [presentasjon, Grep, CASE, interoperabilitet]
creation-date: 2026-04-08
type: research
status: ua
topic: [Grep, CASE, RAG]
---

# Taleplan: Grep og CASE-interoperabilitet

## Fra programmet
### Day 2 – AI, Data, and Trust. (09.00 – 15.00)
To examine how AI can be integrated into education systems through interoperable data,
governed by trusted frameworks and aligned with national priorities.
#### 09:00 – 12:00 | AI, Data Access, and Trust in Education
**Audience:** All participants
**Focus:** To provide a view of how AI relies on interoperable data, and how trust, governance, and standards enable its responsible use in education. The session will look at
demonstrations and examples for standard based ways to access data from AI, Model Context Protocol, Learner Context and Generative AI.
Speakers
• 1EdTech (data standards, MCP, interoperability, AI integration)
• Udir / Sikt
  • Share any ongoing use-cases
  • implementation perspective, infrastructure and data access
Not final – suggestions welcome

Mitt bidrag blir da: Udir: "Share any ongoing use-cases" og "implementation perspective, infrastructure and data access", og innlegget kan holdes på norsk.

## Introduksjon (3–4 minutter)
**Hovedpoeng: Norge har allerede det andre land jobber mot. Grep er maskinlesbar realitet.**

### Et spørsmål fra en internasjonal ekspert

Colin Smyth, som jobber med CASE internasjonalt, stilte meg nylig et godt spørsmål:

> «Hva skal Norge med CASE – dere har jo Grep?»

Det er et ærlig spørsmål. Og svaret er at han har et poeng.
Norge har noe de fleste land bare drømmer om: ett sentralt, autoritativt, maskinlesbart læreplanregister.
I dag skal jeg vise hva vi kan gjøre med det – og så, til slutt, vise at vi kan oversette det til CASE også, bare fordi vi kan.

### Hvem er jeg og hva er min rolle?

- Udir, arbeid med Grep og semantisk teknologi
- Fokus på å gjøre læreplandata maskinlesbar og nyttig for AI-systemer

### Tre spor i dag:

1. Hva er Grep, og hvorfor er det bra utgangspunkt?
2. Hvordan bruker vi Grep til AI – konkret demo med MCP
3. Og ja – vi kan også CASE, fordi strukturerte data åpner for det

---

## Hva er Grep? (3–4 minutter)
**Hovedpoeng: Grep er ikke bare PDF. Det er maskinlesbar data.**

### Grep = nasjonalt læreplanregister

- Sentralisert, maskinlesbar database for alle norske læreplaner
- Eies og drives av Utdanningsdirektoratet
- Tilgjengelig som RDF/Linked Data via SPARQL og REST-API

### Hvorfor er dette viktig?

- Før Grep: læreplaner som PDF-dokumenter (ikke strukturert, vanskelig å søke i)
- Med Grep: strukturert, søkbar, koblet til andre kilder
- Gjør det mulig for både mennesker og maskiner å finne presise faglige data

### Grep i dag

- Allerede i produksjon og brukt av skoler, utdanningstilbydere og verktøyleverandører
- REST API for enkel tilgang
- SPARQL-endepunkt for komplekse spørringer

---

## Grep-datastrukturen (6–7 minutter)
**Hovedpoeng: En læreplan består av gjenkjennbare, kodifiserte deler.**

### Hovedelementene

- **Læreplan-kode** (f.eks. SAF01-04) – identifiserer faget
- **Læreplan** – ett fastsatt dokument per fag og program
- **Kompetansemål** – hva elever skal kunne (kodene: f.eks. KM1648)
- **Kjerneelement** – sentrale idéer og konsepter innenfor faget
- **Læringsressurser** – koblinger til fagmateriale

### Eksempel: En konkret norsk læreplan

- Læreplan-kode: SAF01-04 (Samfunnsfag, LK20)
- Læreplan-dokument: inneholder alle kompetansemål for dette faget og programmet
- Ett kompetansemål: KM1648
  - Har kode (KM1648), tekst, tilhørende kjerneelement, trinn
  - Eksempel: «Reflektere over kva for aktørar som har makt i samfunnet i dag, og korleis desse grunngir standpunkta sine»
  - Strukturen gjør det mulig å søke og kople data

### Hvordan får vi det ut?

- Via SPARQL: spørre etter alle kompetansemål i samfunnsfag for ungdomstrinnet
- Via REST API: hente full læreplan-dokument som JSON
- Dataene har URI-er som gjør dem permanente og referanserbare

---

## AI, RAG og strukturert data (7–8 minutter)
**Hovedpoeng: Modeller hallusinerer når de gjetter. Grep gir dem fakta.**

### Problemet med AI når data skal være faglig sikker

- LLM-er genererer tekst statistisk – de kan generere «halvveis rett» svar
- I utdanningskontekst: hallusinerte faglige råd kan skade elevlæringen
- Eksempel: «Hva inneholder den nye læreplanen i norsk?» → modellen gjetter halvt riktig

### RAG = Retrieval-Augmented Generation

- I stedet for reint model-svar: først hent riktige data, så la modellen formulere
- Flyt:
  1. Bruker spør: «Hva er kompetansemålene i matematikk for ungdomstrinnet?»
  2. System queryer Grep via SPARQL → får eksakte data
  3. LLM får faktaene som kontekst og genererer et godt svar

### Hvorfor Grep er perfekt for RAG

- Strukturert, autoritativ, kodifisert
- Ingen vektordatabase nødvendig – SPARQL er nok
- Data er allerede formalisert; usikkerhet minimeres
- Spesielt kritisk i utdanning, hvor feil kan få konsekvenser

### Konkret fordel

- En lærer eller student bruker AI til å forstå kompetansemål
- System sjekker Grep → vet den er aktuell → ingen gamle eller feilaktige læreplaner

---

## MCP og Learner Context: Fra generell data til personalisert svar (5–6 minutter)
**Hovedpoeng: Riktig data er ikke nok – systemet må også vite hvem som spør.**

### Model Context Protocol (MCP)

- MCP er en åpen protokoll (Anthropic, 2024) for å koble AI-modeller til eksterne datakilder på en standardisert måte
- Fungerer som et «stikkontakt-system»: AI-modellen trenger ikke å vite hvordan Grep fungerer – den bruker et MCP-verktøy som snakker med Grep på dens vegne
- Konkret flyt med MCP:
  ```
  Bruker spør AI → AI kaller MCP-verktøy «grep_hent_kompetansemaal» →
  MCP-server sender SPARQL mot Grep → returnerer strukturerte data →
  AI formulerer svar basert på faktiske kompetansemål
  ```
- **Koblingen til CASE:** En MCP-server kan eksponere Grep-data *som om det var CASE* – dvs. bruke ontologi-mappingen fra [[3-lags RAG-plan]] til å oversette Grep-strukturer til CASE CFItem/CFDocument i sanntid

### Learner Context

- Learner Context handler om at AI-systemet ikke bare kjenner fagdata – det kjenner også *brukeren*
- I 1EdTech-terminologi: informasjon om hvem læreren/eleven er, hvilket program de er på, hvilke kompetansemål de allerede har arbeidet med
- Uten Learner Context: RAG-svaret er generisk («Her er alle kompetansemålene i SAF1-04»)
- Med Learner Context: RAG-svaret er presist («Du er på 10. trinn, her er de tre kompetansemålene som er relevante for din nåværende enhet om demokrati»)

### Hvordan vi ivaretar dette i vår mockup

Demonstrasjonen viser tre lag i kombinasjon:

| Lag                | Teknologi                  | Hva det gjør                                               |
| ------------------ | -------------------------- | ---------------------------------------------------------- |
| 1 – Fagdata        | Grep via SPARQL            | Henter eksakte kompetansemål for SAF01-04, 10. trinn       |
| 2 – Protokoll      | MCP-server                 | Eksponerer Grep som et AI-verktøy; kan oversette til CASE  |
| 3 – Brukerkontekst | Learner Context (simulert) | Filtrerer og tilpasser svar til konkret elev/trinn/program |

**Konkret demo-scenario – tre steg:**

> En lærer på 10. trinn spør: «Hvilke kompetansemål i samfunnsfag er relevante for et prosjekt om demokrati og valg?»

**Steg 1 – Uten Learner Context:**
AI kaller `grep_hent_kompetansemaal("SAF01-04", "10")` og får alle 19 KM.
Svaret er korrekt, men generisk – AI vet ikke hva klassen har jobbet med.

**Steg 2 – Med Learner Context:**
Læreren legger inn brukerprofil i prompten:
```json
{ "rolle": "lærer", "trinn": "10", "fag": "SAF01-04",
  "gjennomgaatt": ["KM1638", "KM1640", "KM1643"] }
```
AI kaller samme verktøy, men tilpasser svaret: peker direkte på
**KM1648** (makt i samfunnet) og **KM1652** (politisk system) som neste relevante steg.

**Steg 3 – CASE-format:**
AI kaller `grep_hent_cfitems("SAF01-04", "10")` og returnerer samme data
strukturert som CASE CFDocument med CFItems – klar for interoperabilitet med
internasjonale systemer. Ingen endringer i Grep.

---

## CASE – fordi vi kan (6–7 minutter)
**Hovedpoeng: Grep er godt nok. Men siden vi har strukturerte data, kan vi også snakke CASE.**

### Hva er CASE?

- Competency and Academic Standards Exchange – internasjonal standard for å beskrive læringsrammer
- Brukt i USA, Europa, internasjonale edtech-plattformer
- Lik Grep i konsept (struktur, koder, hierarki), men internasjonal konvensjon

### Grep er ikke problemet – det er løsningen

- Norge har ikke et problem med læreplandata. Vi har Grep.
- CASE er ikke noe vi *må* ha – det er noe vi *kan* bruke fordi Grep allerede er strukturert
- Siden data er formalisert, kan vi mappe Grep til CASE uten å endre Grep selv
- Det er dette som er styrken med strukturerte data: de er oversettbare

### Konkret eksempel: Nevada vs. Norge

- Nevada, USA: «Social Studies, Grade 9–12, Civics, Standard 1: Understand the U.S. Constitution» (SS.9-12.CE.1)
- Norge: «Samfunnsfag, ungdomstrinnet, SAF01-04/KM1652: Beskrive trekk ved det politiske systemet og velferdssamfunnet i Noreg i dag og reflektere over sentrale utfordringar»
- CASE gjør det mulig å si: «Disse to kompetansemålene dekker lignende forståelse av demokratiske institusjoner og styresett»
- Gir grunnlag for:
  - Internasjonal kartlegging av kompetanser
  - Godkjenning av utenlandsk utdanning
  - Globale læringsplattformer som skal forstå både norsk og utenlandsk kurs

### Mapping: Fra Grep til CASE

- Grep-kompetansemål → CASE CFItem
- Grep-læreplan → CASE CFDocument
- Grep-fagkoder → CASE kompetanseklasser
- Via en adapter eller crosswalk blir dataene oversettbare

---

## Konkretisering: Nevada-eksempelet (2–3 minutter)
**Hovedpoeng: Se konkret hvordan samme ambisjon ser ut i to systemer.**

### Scenario

- En norsk elev skal studere i USA, eller omvendt
- Sammenligningsorganer må vite: er disse kompetansemålene likeverdige?

### Uten CASE

- Nevada: engelsk dokumentasjon i deres system
- Norge: norsk dokumentasjon i Grep
- Ingen direkte sammenheng; må gjøres manuelt av mennesker

### Med CASE

- Begge systemer, hvis koblet til CASE, kan sees på samme «språk»
- System kan automatisk sjekke: «Matcher Nevada SS.9-12.CE.1 norske SAF01-04/KM1652?»
- Gir grunnlag for raskere godkjenning og samarbeid

---

## Konklusjon og diskusjon (2–3 minutter)
**Hovedpoeng: Vi er ikke bak. Vi er foran.**

### Vi svarer på Colins spørsmål

Colin spurte: «Hva skal Norge med CASE?»
Svaret er: vi trenger det ikke – men vi *kan* bruke det, og det er nettopp poenget.
Grep gir oss friheten til å velge.

### Vi har det norske på plass

- Grep er maskinlesbar, strukturert og driftet – det er ikke alle land som kan si det
- Perfekt grunnlag for AI (RAG), søk og automatisering
- Og nå har vi vist: kan brukes som kilde for CASE-kompatible systemer uten å endre noe

### Neste steg – hvis vi vil

- En enkel adapter mellom Grep og CASE kan åpne for internasjonale plattformer
- Gjøre norske læreplandata synlige globalt – på Norges premisser
- Utgangspunktet er godt. Spørsmålet er hva vi vil bruke det til.

### Diskusjonsspørsmål for gruppa

1. Hvordan kan vi bruke Grep som CASE-tilpasset ressurs uten å endre selve Grep-registeret?
2. Hvordan håndterer vi versjonering og oppdateringer?
3. Hvilke brukstilfeller ser vi først for en Grep→CASE-adapter?
   - Internasjonale plattformer? Utdanningsinstitusjonell godkjenning?
4. Hvordan sikrer vi at norske data blir brukt og ikke ignorert i globale standarder?
5. Hvem eier mappingen? Hvem vedlikeholder den?

### Invitasjon til videre arbeid

- Dette ligger rikt potensial for interoperabilitet
- Vi ser gjerne innspill fra dere om prioritet og brukstilfeller

---

## Vedlegg: Nyttige referanser

- Grep REST API dokumentasjon
- CASE-spesifikasjonen (www.case-network.com)
- Research-notat i vaulten: [[Research - Grep og CASE interoperabilitet]]
- Eksempler på SPARQL-spørringer mot Grep
