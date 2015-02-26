#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml.etree import parse
import sys
import redis

r = redis.StrictRedis()

filename = sys.argv[1]
tree = parse(filename)

ns = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "nsogi": "http://prefix.cc/nsogi"
}

#
#  redis model: normalized_label:{"label": LABEL, "identifier": IDENTIFIER}
# 
def model(label, identifier):
    return '{}:{{"label":"{}", "id":"{}"}}'.format(
            label.lower().encode('utf-8'), label.encode('utf-8'), identifier)


print "indexing: {}".format(filename)

for concept in tree.xpath('//rdf:Description', namespaces=ns):
    
    rdftype =  concept.xpath("rdf:type/@rdf:resource", namespaces=ns)[0]
   
    if rdftype.endswith("Concept"):
        # term id url
        term_id = concept.xpath("./@rdf:about", namespaces=ns)[0]
        
        # prefLabel
        preflabel = concept.xpath("skos:prefLabel", namespaces=ns)[0].text
        r.zadd("autocomplete", 0, model(preflabel, term_id))

        # altLabels
        altlabels = concept.xpath("skos:altLabel", namespaces=ns)
        for altlabel in altlabels:
            r.zadd("autocomplete", 0, model(altlabel.text, term_id))
