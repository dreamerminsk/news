from qwikidata.sparql  import return_sparql_query_results

query_string = """
        SELECT ?child ?childLabel
WHERE
{
# ?child  father   Bach
  ?child wdt:P22 wd:Q1339.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
}"""

res = return_sparql_query_results(query_string)
print(res)
for row in res["results"]["bindings"]:
   print(row)