# Ontologi

Denne mappen inneholder ontologi-filer for grep-mcp-mockup. Filene lastes inn
i GraphDB-repoet `grep-mcp-mockup` i rekkefølgen angitt nedenfor.

## Filer

| Fil | Innhold |
|---|---|
| `grep_ontologi.ttl` | Normativ ontologi: klasser og egenskaper i Grep-modellen (LK20) |
| `grep_case_mapping.ttl` | CASE-broaksiomer: kobling fra Grep til CASE/CFItem |

## Laste-rekkefølge i GraphDB Workbench

1. Last inn Grep JSON-LD-dump (i eget named graph, f.eks. `<urn:graph:grep-data>`)
2. Last inn `grep_ontologi.ttl`
3. Last inn `grep_case_mapping.ttl`

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
