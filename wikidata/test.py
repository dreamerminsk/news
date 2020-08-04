from qwikidata.sparql  import return_sparql_query_results
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api


query_string = """SELECT ?book ?title ?illustratorLabel ?publisherLabel ?published
WHERE
{
  ?book wdt:P50 wd:Q35610;
        wdt:P1476 ?title;
        wdt:P110 ?illustrator;
        wdt:P123 ?publisher;
        wdt:P577 ?published.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
}"""

res = return_sparql_query_results(query_string)
print(res)
for row in res["results"]["bindings"]:
   print(row)