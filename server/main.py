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


if __name__ == "__main__":
    mcp.run(transport="stdio")
