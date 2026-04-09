#!/usr/bin/env python3
"""
CASE adapter: oversetter Grep-bindings til CASE CFItem-format.
CASE adapter: translates Grep bindings to CASE CFItem format.

CASE (Competencies & Academic Standards Exchange) er en standard fra
1EdTech for maskinlesbar utveksling av kompetansestandarder.

CASE (Competencies & Academic Standards Exchange) is a standard from
1EdTech for machine-readable exchange of competency standards.

Ref: https://www.imsglobal.org/activity/case
"""

from typing import Any, Dict, List


def to_cfitem(binding: Dict[str, Any]) -> Dict[str, Any]:
    """
    Oversetter én Grep SPARQL-binding til et CASE CFItem.
    Translates a single Grep SPARQL binding to a CASE CFItem.

    Args:
        binding: SPARQL-binding fra hent_kompetansemaal, med feltene:
                 km, kmCode, title, gradeLabel, curriculum, currTitle.

    Returns:
        Dict strukturert som et CASE CFItem.
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
    Pakker en liste med CFItem-er inn i et CASE CFDocument.
    Wraps a list of CFItems into a CASE CFDocument.

    Args:
        laereplan_kode: Læreplan-kode, f.eks. 'SAF01-04'.
        tittel: Læreplan-tittel.
        cfitems: Liste med CFItem-dicts.

    Returns:
        Dict strukturert som et CASE CFDocument med innebygde CFItem-er.
    """
    return {
        "CFDocument": {
            "identifier":        f"http://psi.udir.no/kl06/{laereplan_kode}",
            "humanCodingScheme": laereplan_kode,
            "title":             tittel,
        },
        "CFItems": cfitems,
    }
