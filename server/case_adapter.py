#!/usr/bin/env python3
"""
CASE adapter: translates Grep SPARQL bindings to CASE CFItem format.

CASE (Competencies & Academic Standards Exchange) is a standard from
1EdTech for machine-readable exchange of competency standards.

Ref: https://www.imsglobal.org/activity/case
"""

from typing import Any, Dict, List


def to_cfitem(binding: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translates a single Grep SPARQL binding to a CASE CFItem.

    Args:
        binding: SPARQL binding from hent_kompetansemaal, with fields:
                 km, kmCode, title, gradeLabel, curriculum, currTitle.

    Returns:
        Dict structured as a CASE CFItem.
    """
    return {
        "identifier":        binding.get("km",         {}).get("value", ""),
        "humanCodingScheme": binding.get("kmCode",     {}).get("value", ""),
        "fullStatement":     binding.get("title",      {}).get("value", ""),
        "educationLevel":   [binding.get("gradeLabel", {}).get("value", "")],
        "CFDocumentURI": {
            "identifier": binding.get("curriculum", {}).get("value", ""),
            "title":      binding.get("currTitle",  {}).get("value", ""),
        },
    }


def to_cfdocument(laereplan_kode: str, tittel: str, cfitems: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Wraps a list of CFItems into a CASE CFDocument.

    Args:
        laereplan_kode: Curriculum code, e.g. 'SAF01-04'.
        tittel: Curriculum title.
        cfitems: List of CFItem dicts.

    Returns:
        Dict structured as a CASE CFDocument with embedded CFItems.
    """
    return {
        "CFDocument": {
            "identifier":        f"http://psi.udir.no/kl06/{laereplan_kode}",
            "humanCodingScheme": laereplan_kode,
            "title":             tittel,
        },
        "CFItems": cfitems,
    }
