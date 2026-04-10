# Ontologi

Denne mappen inneholder ontologi-filer for grep-mcp-mockup. Filene lastes inn
i GraphDB-repoet `grep-mcp-mockup` i rekkefølgen angitt nedenfor.

## Filer

| Fil | Innhold |
|---|---|
| `grep_ontologi.ttl` | Normativ ontologi: klasser og egenskaper i Grep-modellen (LK20) |
| `grep_case_mapping.ttl` | CASE-broaksiomer: kobling fra Grep til CASE/CFItem |

## Graf-struktur i GraphDB

| Graf | Innhold |
|---|---|
| Default graph | Grep JSON-LD-dump (allerede lastet) |
| `urn:graph:grep-ontologi` | `grep_ontologi.ttl` |
| `urn:graph:grep-case-mapping` | `grep_case_mapping.ttl` |

Grep-dataene ligger i default graph og røres ikke. Ontologi-filene lastes
inn som named graphs slik at de kan oppdateres uavhengig av dataene.
Eksisterende SPARQL-spørringer mot default graph fungerer uendret, siden
GraphDB inkluderer alle named graphs i default graph som union.

## Laste-rekkefølge i GraphDB Workbench

1. Last inn `grep_ontologi.ttl` med target graph `urn:graph:grep-ontologi`
2. Last inn `grep_case_mapping.ttl` med target graph `urn:graph:grep-case-mapping`

Grep JSON-LD-dump er allerede lastet i default graph – ingen endringer der.

## Omfang

Ontologien er bevisst avgrenset til klasser og egenskaper som er relevante
for dette prosjektet:

**Klasser:** `Kompetansemaal`, `kompetansemaal_lk20`, `Laereplan`,
`Kompetansemaalsett`, `Aarstrinn`

**Egenskaper:** `kode`, `tittel`, `kortform`, `tilhoerer-laereplan`,
`tilhoerer-kompetansemaalsett`, `etter-aarstrinn`

## CASE-standarden

CASE (Competencies & Academic Standards Exchange) er en standard fra
1EdTech (tidligere IMS Global) for maskinlesbar utveksling av læreplaner
og kompetansestandarder på tvers av systemer.

- Spesifikasjon: https://www.imsglobal.org/activity/case
- Namespace brukt her: `https://purl.imsglobal.org/spec/case/v1p0/vocab#`
