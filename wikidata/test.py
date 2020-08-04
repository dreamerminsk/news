from qwikidata.sparql  import return_sparql_query_results

query_string = """
        SELECT $WDid
         WHERE {
          ?WDid (wdt:P279)* wd:Q4022
        }"""

res = return_sparql_query_results(query_string)

for row in res["results"]["bindings"]:
   print(row)