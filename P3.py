
# coding: utf-8

# In[2]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re
import codecs
import json


# In[3]:

sample = 'sample.osm'


# In[17]:

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)



expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Highway"]


mapping = { "St": "Street",
            "st": "Street",
            "Ct": "Court",
            "E": "East",
            "N": "North",
            "Cir": "Circle",
            "road": "Road",
            "S.": "South",
            "Ave": "Avenue",
            "Ln": "Lane",
            "Ave.": "Avenue",
            "ave": "Avenue",
            "Pkwy": "Parkway",
            "Blvd": "Boulevard",
            "Pl": "Place",
            "Trl": "Trail",
            "Hwy": "Highway",
            "Dr": "Drive",
            "Dr.": "Drive",
            "W.": "West",
            "W": "West",
            "Rd": "Road"
            }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    """
    Takes the street abbreviation attribute as 'name' to return the full name using the mapping dictionary.
    """
    m = street_type_re.search(name)
    other_street_types = []
    if m:
        street_type = m.group()
        if street_type in mapping.keys():
            name = re.sub(street_type_re,mapping[street_type],name)
        else:
            other_street_types.append(street_type)

    return name

def update_postcode(postcode):
    """
    Takes in a postcode and produces a 5 digit code without hyphens or abbreviations.
    """
    match = re.match(r'^\D*(\d{5}).*', postcode)
    clean_postcode = match.group(1)
    return clean_postcode


def test():
    st_types = audit(sample)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
        print better_name

#audit(sample)


# In[23]:

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]



def shape_element(element):
    
    node = {}
    address = {}
    amenity = {}
    cuisine = {}
    landuse = {}
    bicycle = {}
    religion = {}
    sport = {}
    pos = []
    node_refs = []
    
    if element.tag == "node" or element.tag == "way" :
        node['id'] = element.attrib['id']
        node['type'] = element.tag
        node['visible'] = element.get('visible')
        created = {}
        created["version"] = element.attrib["version"]
        created["changeset"] = element.attrib["changeset"]
        created["timestamp"] = element.attrib["timestamp"]
        created["user"] = element.attrib["user"]
        created["uid"] = element.attrib["uid"]
        node["created"] = created
        if 'lat' in element.keys() and 'lon' in element.keys():
            pos = [element.attrib['lat'], element.attrib['lon']]
            node['pos'] = [float(string) for string in pos]
        else:
            node['pos'] = None
        for tag in element.iter('tag'):
            if re.search('addr:', tag.attrib['k']):
                if len(tag.attrib['k'].split(":")) < 3:
                    addr_add = tag.attrib['k'].split(":")[1]
                    if tag.attrib['k'] == "addr:postcode":
                        tag.attrib['v'] = update_postcode(tag.attrib['v'])
                    if tag.attrib['v'] == "Chicago, IL":
                        tag.attrib['v'] = "Chicago"
                        address[addr_add] = update_name(tag.attrib['v'], mapping)
                    else:
                        address[addr_add] = update_name(tag.attrib['v'], mapping)
                    #if len(tag.attrib['v'].split("-")) == 2:
                        #tag.attrib['v'] = tag.attrib['v'].split("-")[0]
            if re.search('amenity', tag.attrib['k']):
                amenity_add = tag.attrib['k']
                amenity[amenity_add] = tag.attrib['v']
            if re.search('cuisine', tag.attrib['k']):
                cuisine_add = tag.attrib['k']
                cuisine[cuisine_add] = tag.attrib['v']
            if re.search('landuse', tag.attrib['k']):
                landuse_add = tag.attrib['k']
                landuse[landuse_add] = tag.attrib['v']
            if re.search('bicycle', tag.attrib['k']):
                bicycle_add = tag.attrib['k']
                bicycle[bicycle_add] = tag.attrib['v']
            if re.search('religion', tag.attrib['k']):
                religion_add = tag.attrib['k']
                religion[religion_add] = tag.attrib['v']
            if re.search('sport', tag.attrib['k']):
                sport_add = tag.attrib['k']
                sport[sport_add] = tag.attrib['v']
        for nd in element.iter('nd'):
            node_refs.append(nd.attrib['ref'])
                
        if address:
            node['address'] = address
        if amenity:
            node['amenity'] = amenity
        if cuisine:
            node['cuisine'] = cuisine
        if landuse:
            node['landuse'] = landuse
        if bicycle:
            node['bicycle'] = bicycle
        if religion:
            node['religion'] = religion
        if sport:
            node['sport'] = sport
        if node_refs:
            node['node_refs'] = node_refs

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    data = process_map(sample, True)
    #pprint.pprint(data)
    


#test()


# In[ ]:

#https://discussions.udacity.com/t/how-to-use-the-compile-variables-for-tag-types/198286
#https://discussions.udacity.com/t/apply-tag-types-function/181950
#https://discussions.udacity.com/t/case-study-iterative-parsing/165972/4
#https://discussions.udacity.com/t/exploring-users/172717/11
#https://discussions.udacity.com/t/tag-types-and-improving-street-names-locally/46437/20
#https://discussions.udacity.com/t/preparing-for-database-final-project/182917/3
#https://discussions.udacity.com/t/updating-zip-codes/43619/12
#https://discussions.udacity.com/t/pymongo-queries/186434
#https://discussions.udacity.com/t/last-quiz-preparing-for-database-in-lesson-6-mongodb/44559/31
#https://api.mongodb.com/python/current/examples/index.html

