# Ontology

This directory contains ontology files for grep-mcp-mockup. The files are loaded
into the GraphDB repository `grep-mcp-mockup` in the order specified below.

## Files

| File | Contents |
|---|---|
| `grep_ontologi.ttl` | Normative ontology: classes and properties in the Grep model (LK20) |
| `grep_case_mapping.ttl` | CASE bridge axioms: mappings from Grep to CASE/CFItem |

## Graph structure in GraphDB

| Graph | Contents |
|---|---|
| Default graph | Grep JSON-LD dump (already loaded) |
| `urn:graph:grep-ontologi` | `grep_ontologi.ttl` |
| `urn:graph:grep-case-mapping` | `grep_case_mapping.ttl` |

Grep data resides in the default graph and is not modified. Ontology files are loaded
as named graphs so they can be updated independently of the data.
Existing SPARQL queries against the default graph continue to work unchanged, since
GraphDB includes all named graphs in the default graph as a union.

## Load order in GraphDB Workbench

1. Load `grep_ontologi.ttl` with target graph `urn:graph:grep-ontologi`
2. Load `grep_case_mapping.ttl` with target graph `urn:graph:grep-case-mapping`

The Grep JSON-LD dump is already loaded in the default graph — no changes needed there.

## Scope

The ontology is intentionally scoped to the classes and properties relevant
to this project:

**Classes:** `Kompetansemaal`, `kompetansemaal_lk20`, `Laereplan`,
`Kompetansemaalsett`, `Aarstrinn`

**Properties:** `kode`, `tittel`, `kortform`, `tilhoerer-laereplan`,
`tilhoerer-kompetansemaalsett`, `etter-aarstrinn`

## The CASE standard

CASE (Competencies & Academic Standards Exchange) is a standard from
1EdTech (formerly IMS Global) for machine-readable exchange of curricula
and competency standards across systems.

- Specification: https://www.imsglobal.org/activity/case
- Namespace used here: `https://purl.imsglobal.org/spec/case/v1p0/vocab#`
