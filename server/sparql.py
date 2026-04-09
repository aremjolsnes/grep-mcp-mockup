#!/usr/bin/env python3
"""
SPARQL client for Grep data in GraphDB repository.

This module provides functions to query the Grep curriculum data
via the GraphDB SPARQL endpoint at:
https://sparql-beta-data.udir.no/repositories/grep-mcp-mockup
"""

import json
import logging
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GrepSparqlClient:
    """Client for querying Grep data via SPARQL"""

    def __init__(self, repository_url: str = "https://sparql-beta-data.udir.no/repositories/grep-mcp-mockup"):
        """
        Initialize the SPARQL client.

        Args:
            repository_url: URL to the GraphDB repository
        """
        self.repository_url = repository_url
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'grep-mcp-mockup/1.0'
        }

    def query(self, sparql_query: str) -> Dict[str, Any]:
        """
        Execute a SPARQL query and return results as JSON.

        Args:
            sparql_query: The SPARQL query string

        Returns:
            Query results as JSON dictionary

        Raises:
            Exception: If query fails
        """
        try:
            logger.info(f"Querying SPARQL endpoint")
# URL encode the query
            params = {'query': sparql_query}
            url = f"{self.repository_url}?{urlencode(params)}"

            logger.info(f"Querying: {url}")

            # Create request
            req = Request(url, headers=self.headers)

            # Execute request
            with urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))

            logger.info(f"Query returned {len(data.get('results', {}).get('bindings', []))} results")
            return data

        except HTTPError as e:
            logger.error(f"HTTP Error: {e.code} - {e.reason}")
            raise Exception(f"SPARQL query failed: {e.code} {e.reason}")
        except URLError as e:
            logger.error(f"URL Error: {e.reason}")
            raise Exception(f"Failed to connect to SPARQL endpoint: {e.reason}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise Exception(f"Invalid JSON response from SPARQL endpoint: {e}")

    def get_competence_aims(self, curriculum_code: str, grade: str) -> List[Dict[str, Any]]:
        """
        Get competence aims for a specific curriculum and grade.

        Args:
            curriculum_code: Curriculum code used as URI suffix, e.g. 'SAF01-04'.
                             Resolves to <http://psi.udir.no/kl06/SAF01-04>.
                             Pass empty string for no curriculum filtering.
            grade: Grade short form (e.g. '10') or label (e.g. '10. trinn').
                   Pass empty string for no grade filtering.

        Returns:
            List of competence aims with their details
        """
        curriculum_filter = (
            f"FILTER (?curriculum = d:{curriculum_code})"
            if curriculum_code
            else ""
        )
        grade_filter = (
            f"""FILTER (
                CONTAINS(str(?gradeShort), "{grade}") ||
                CONTAINS(str(?gradeLabel), "{grade}")
            )"""
            if grade
            else ""
        )

        query = f"""
        PREFIX u: <http://psi.udir.no/ontologi/kl06/>
        PREFIX d: <http://psi.udir.no/kl06/>

        SELECT ?km ?kmCode ?title ?kms ?kmsTitle ?grade ?gradeLabel ?gradeShort ?curriculum ?currTitle
        WHERE {{
            ?km a u:kompetansemaal_lk20 ;
                u:kode ?kmCode ;
                u:tittel ?title ;
                u:tilhoerer-kompetansemaalsett ?kms ;
                u:tilhoerer-laereplan ?curriculum .

            {curriculum_filter}

            ?curriculum u:tittel ?currTitle .

            ?kms u:etter-aarstrinn ?grade ;
                 u:tittel ?kmsTitle .

            ?grade u:tittel ?gradeLabel ;
                   u:kortform ?gradeShort .

            FILTER (
                LANG(?title) = "default" &&
                LANG(?kmsTitle) = "default" &&
                LANG(?gradeLabel) = "default" &&
                LANG(?gradeShort) = "default" &&
                LANG(?currTitle) = "default"
            )
            {grade_filter}
        }}
        ORDER BY ?kmCode
        LIMIT 200
        """

        results = self.query(query)
        return results.get('results', {}).get('bindings', [])

    def get_curriculum(self, subject_code: str) -> Dict[str, Any]:
        """
        Get full curriculum information for a subject.

        Args:
            subject_code: Subject code (e.g., 'SAF1-04')

        Returns:
            Curriculum information
        """
        query = f"""
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX grep: <http://psi.udir.no/ontologi/kl06/>

        SELECT ?lp_code ?title ?description
        WHERE {{
            ?lp a grep:Laereplan ;
                grep:harKode ?lp_code ;
                skos:prefLabel ?title ;
                dct:description ?description .
            FILTER(?lp_code = "{subject_code}")
        }}
        """

        results = self.query(query)
        bindings = results.get('results', {}).get('bindings', [])

        if bindings:
            return bindings[0]
        else:
            return {}

    def search_competence_aims(self, search_term: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for competence aims containing the search term.

        Args:
            search_term: Text to search for
            limit: Maximum number of results

        Returns:
            List of matching competence aims
        """
        query = f"""
        PREFIX u: <http://psi.udir.no/ontologi/kl06/>

        SELECT ?km_code ?title
        WHERE {{
            ?km a u:kompetansemaal_lk20 ;
                u:kode ?km_code ;
                u:tittel ?searchTitle ;
                u:tittel ?title .

            FILTER (CONTAINS(LCASE(str(?searchTitle)), LCASE("{search_term}")))
            FILTER (LANG(?title) = "default")
        }}
        ORDER BY ?km_code
        LIMIT {limit}
        """

        results = self.query(query)
        return results.get('results', {}).get('bindings', [])

# Global client instance
client = GrepSparqlClient()

# Convenience functions for easy access
def hent_kompetansemaal(laereplan_kode: str, trinn: str) -> List[Dict[str, Any]]:
    """Hent kompetansemål for gitt læreplan-kode (f.eks. 'SAF01-04') og trinn"""
    return client.get_competence_aims(laereplan_kode, trinn)

def hent_laereplan(fagkode: str) -> Dict[str, Any]:
    """Hent lærerplan for gitt fagkode"""
    return client.get_curriculum(fagkode)

def sok_kompetansemaal(fritekst: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Søk etter kompetansemål med fritekst"""
    return client.search_competence_aims(fritekst, limit)

if __name__ == "__main__":
    # Test the client
    try:
        # Test basic connectivity
        results = client.query("SELECT ?s WHERE { ?s ?p ?o } LIMIT 1")
        print("✅ SPARQL endpoint is accessible")

        # Test competence aims query
        try:
            aims = hent_kompetansemaal("SAF01-04", "10")
            print(f"Found {len(aims)} competence aims for SAF01-04 grade 10")
        except Exception as e:
            print(f"Query executed but no data found (expected if GraphDB not loaded yet): {e}")

    except Exception as e:
        print(f"❌ Failed to connect: {e}")