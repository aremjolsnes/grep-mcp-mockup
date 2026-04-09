#!/usr/bin/env python3
"""
Test script to verify access to Grep SPARQL endpoint
"""

from SPARQLWrapper import SPARQLWrapper, JSON

def test_grep_endpoint():
    """Test basic connectivity to Grep SPARQL endpoint"""

    sparql = SPARQLWrapper("https://sparql-beta-data.udir.no/repositories/grep-mcp-mockup")
    sparql.setReturnFormat(JSON)

    # Simple query to get some basic info
    query = """
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?subject ?label
    WHERE {
        ?subject a skos:Concept ;
                 skos:prefLabel ?label .
    }
    LIMIT 5
    """

    sparql.setQuery(query)

    try:
        results = sparql.query().convert()
        print("✅ Successfully connected to Grep SPARQL endpoint!")
        print(f"Retrieved {len(results['results']['bindings'])} results:")
        for result in results['results']['bindings']:
            print(f"  - {result['label']['value']}")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Grep SPARQL endpoint: {e}")
        return False

if __name__ == "__main__":
    test_grep_endpoint()