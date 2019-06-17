import os, sys, re, json, requests, collections
from io import StringIO
from lxml.etree import XMLParser, parse, tostring
from tempfile import mkstemp
from subprocess import check_call
from urllib.request import urlopen

from flask import current_app

from pele import cache


def get_etree(xml):
    """Return a tuple of [lxml etree element, prefix->namespace dict].
    """

    parser = XMLParser(remove_blank_text=True)
    if xml.startswith('<?xml') or xml.startswith('<'):
        return (parse(StringIO(xml), parser).getroot(),
                get_ns_dict(xml))
    else:
        if os.path.isfile(xml): xml_str = open(xml).read()
        else: xml_str = urlopen(xml).read()
        return (parse(StringIO(xml_str), parser).getroot(),
                get_ns_dict(xml_str))


def get_ns_dict(xml):
    """Take an xml string and return a dict of namespace prefixes to
    namespaces mapping."""
    
    nss = {} 
    def_cnt = 0
    matches = re.findall(r'\s+xmlns:?(\w*?)\s*=\s*[\'"](.*?)[\'"]', xml)
    for match in matches:
        prefix = match[0]; ns = match[1]
        if prefix == '':
            def_cnt += 1
            prefix = '_' * def_cnt
        nss[prefix] = ns
    return nss


def xpath(elt, xp, ns, default=None):
    """Run an xpath on an element and return the first result.  If no results
    were returned then return the default value."""
    
    res = elt.xpath(xp, namespaces=ns)
    if len(res) == 0: return default
    else: return res[0]
    

def pprint_xml(et):
    """Return pretty printed string of xml element."""
    
    return tostring(et, pretty_print=True)
