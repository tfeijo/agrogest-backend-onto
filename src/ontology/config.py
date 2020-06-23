from owlready2 import *

onto_path.append("src/ontology/")
onto = get_ontology("bd.owl").load()

infered = get_ontology("bd_infered.owl").load()
