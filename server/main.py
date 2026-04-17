#!/usr/bin/env python3
"""
MCP server exposing Grep curriculum data as tools.

Tools:
  - grep_hent_kompetansemaal: Fetch competence aims for a curriculum and grade
  - grep_sok_kompetansemaal:  Full-text search across competence aims
  - grep_hent_cfitems:        Fetch competence aims in CASE CFItem format

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
    Fetches competence aims from Grep for a given curriculum and grade.

    Args:
        laereplan_kode: Curriculum code, e.g. 'SAF01-04'. Empty string returns all curricula.
        trinn: Grade, e.g. '10' or '7'. Empty string returns all grades.

    Returns:
        List of competence aims. Each element contains:
        - kmCode: Competence aim code (e.g. KM7817)
        - title: Competence aim text in the official language
        - kmsTitle: Name of the competence aim set
        - gradeLabel: Grade description (e.g. '10. trinn')
        - currTitle: Curriculum title
    """
    raw = hent_kompetansemaal(laereplan_kode, trinn)
    return [
        {
            "kmCode":     r.get("kmCode", {}).get("value", ""),
            "title":      r.get("title", {}).get("value", ""),
            "kmsTitle":   r.get("kmsTitle", {}).get("value", ""),
            "gradeLabel": r.get("gradeLabel", {}).get("value", ""),
            "currTitle":  r.get("currTitle", {}).get("value", ""),
            "keCodes":    r.get("keCodes", {}).get("value", ""),
            "keTitles":   r.get("keTitles", {}).get("value", ""),
        }
        for r in raw
    ]


@mcp.tool()
def grep_sok_kompetansemaal(fritekst: str, maks_treff: int = 10) -> list[dict]:
    """
    Searches for competence aims in Grep using free text.

    Args:
        fritekst: Search text, e.g. 'demokrati' or 'kildekritikk'.
        maks_treff: Maximum number of results (default 10).

    Returns:
        List of matching competence aims (km_code, title, description).
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
    Fetches competence aims from Grep and returns them in CASE CFItem format.

    Args:
        laereplan_kode: Curriculum code, e.g. 'SAF01-04'. Empty string returns all curricula.
        trinn: Grade, e.g. '10' or '7'. Empty string returns all grades.

    Returns:
        A CASE CFDocument with associated CFItems. The structure follows
        the 1EdTech CASE standard (Competencies & Academic Standards Exchange).
        Each CFItem contains:
        - identifier: URI of the competence aim
        - humanCodingScheme: Competence aim code (e.g. KM1638)
        - fullStatement: Competence aim text
        - educationLevel: List with grade description
        - CFDocumentURI: Reference to the curriculum (identifier + title)
    """
    raw = hent_kompetansemaal(laereplan_kode, trinn)
    cfitems = [to_cfitem(r) for r in raw]

    tittel = raw[0].get("currTitle", {}).get("value", laereplan_kode) if raw else laereplan_kode
    return to_cfdocument(laereplan_kode, tittel, cfitems)


if __name__ == "__main__":
    mcp.run(transport="stdio")
