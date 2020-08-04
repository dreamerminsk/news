from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api


query_string = """SELECT ?book ?title ?illustratorLabel ?publisherLabel ?published
WHERE
{
  ?book wdt:P50 wd:Q35610.
  OPTIONAL { ?book wdt:P1476 ?title. }
  OPTIONAL { ?book wdt:P110 ?illustrator. }
  OPTIONAL { ?book wdt:P123 ?publisher. }
  OPTIONAL { ?book wdt:P577 ?published. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
}"""

res = return_sparql_query_results(query_string)
print(res)
for row in res["results"]["bindings"]:
   print(row)
   
Q_RIVER = "Q4022"
subclasses_of_river = get_subclasses_of_item(Q_RIVER)
print(subclasses_of_river)