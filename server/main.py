#!/usr/bin/env python3
"""
MCP server exposing Grep curriculum data as tools.

Exposes:
  - hent_kompetansemaal: Fetch competence aims for a curriculum and grade
  - sok_kompetansemaal:  Full-text search across competence aims

Run with:
    python server/main.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from mcp.server.fastmcp import FastMCP
from sparql import hent_kompetansemaal, sok_kompetansemaal
from case_adapter import to_cfitem, to_cfdocument

mcp = FastMCP("grep-mcp")


@mcp.tool()
def grep_hent_kompetansemaal(laereplan_kode: str, trinn: str) -> list[dict]:
    """
    Henter kompetansemål fra Grep for en gitt læreplan og trinn.

    Args:
        laereplan_kode: Læreplan-kode, f.eks. 'SAF01-04'. Tom streng gir alle læreplaner.
        trinn: Trinn, f.eks. '10' eller '7'. Tom streng gir alle trinn.

    Returns:
        Liste med kompetansemål. Hvert element inneholder:
        - kmCode: Kompetansemålkode (f.eks. KM7817)
        - title: Kompetansemålstekst på fastsettingsspråket
        - kmsTitle: Navn på kompetansemålsettet
        - gradeLabel: Trinnbeskrivelse (f.eks. '10. trinn')
        - currTitle: Læreplan-tittel
    """
    raw = hent_kompetansemaal(laereplan_kode, trinn)
    return [
        {
            "kmCode":    r.get("kmCode", {}).get("value", ""),
            "title":     r.get("title", {}).get("value", ""),
            "kmsTitle":  r.get("kmsTitle", {}).get("value", ""),
            "gradeLabel": r.get("gradeLabel", {}).get("value", ""),
            "currTitle": r.get("currTitle", {}).get("value", ""),
        }
        for r in raw
    ]


@mcp.tool()
def grep_sok_kompetansemaal(fritekst: str, maks_treff: int = 10) -> list[dict]:
    """
    Søker etter kompetansemål i Grep med fritekst.

    Args:
        fritekst: Søketekst, f.eks. 'demokrati' eller 'kildekritikk'.
        maks_treff: Maks antall treff (standard 10).

    Returns:
        Liste med matchende kompetansemål (km_code, title, description).
    """
    raw = sok_kompetansemaal(fritekst, maks_treff)
    return [
        {
            "km_code":     r.get("km_code", {}).get("value", ""),
            "title":       r.get("title", {}).get("value", ""),
            "description": r.get("description", {}).get("value", ""),
        }
        for r in raw
    ]


@mcp.tool()
def grep_hent_cfitems(laereplan_kode: str, trinn: str) -> dict:
    """
    Henter kompetansemål fra Grep og returnerer dem i CASE CFItem-format.

    Args:
        laereplan_kode: Læreplan-kode, f.eks. 'SAF01-04'. Tom streng gir alle læreplaner.
        trinn: Trinn, f.eks. '10' eller '7'. Tom streng gir alle trinn.

    Returns:
        Et CASE CFDocument med tilhørende CFItem-er. Strukturen følger
        1EdTech CASE-standarden (Competencies & Academic Standards Exchange).
        Hvert CFItem inneholder:
        - identifier: URI til kompetansemålet
        - humanCodingScheme: Kompetansemålkode (f.eks. KM1638)
        - fullStatement: Kompetansemålstekst
        - educationLevel: Liste med trinnbeskrivelse
        - CFDocumentURI: Referanse til læreplan (identifier + title)
    """
    raw = hent_kompetansemaal(laereplan_kode, trinn)
    cfitems = [to_cfitem(r) for r in raw]

    tittel = raw[0].get("currTitle", {}).get("value", laereplan_kode) if raw else laereplan_kode
    return to_cfdocument(laereplan_kode, tittel, cfitems)


if __name__ == "__main__":
    mcp.run(transport="stdio")
