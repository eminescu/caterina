#!/usr/bin/python -u

import config, cache

import urlparse
from BeautifulSoup import BeautifulSoup

try:
    import json
except ImportError:
    import simplejson as json

class Auto:
    def __init__(self):
        self.cases = []

class Case:
    def __init__(self):
        pass

class JSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, obj):
        
        if isinstance(obj, Auto):
            ret = dict(obj.__dict__)
            ret["cases"] = [ (pair[0], pair[1].id) for pair in obj.cases ]
            return ret

        if isinstance(obj, Case):
            ret = dict(obj.__dict__)
            ret["auto"] = obj.auto.name
            return ret

        return json.JSONEncoder.default(self, obj)


C = cache.Cacher( )

autos = {}
cases = {}

page = C.get(config.URL_CASELLI)

soup = BeautifulSoup( page.data )

for autoTd in soup('td', id="nomeAuto"):
    autoAnchor = autoTd.contents[0]

    auto = Auto()

    auto.name = autoAnchor.contents[0].strip()
    auto.url =  urlparse.urljoin( page.url, autoAnchor['href'].strip() )
    auto.length = autoTd.parent('td')[1].contents[0]

    autos[ auto.name ] = auto

    autoPage = C.get( auto.url )
    autoSoup = BeautifulSoup( autoPage.data )
    for caseLengthTd in autoSoup('td', attrs={"class":"kmAuto"}):
        
        caseTds = caseLengthTd.parent('td')

        case = Case()
        case.id = int(caseTds[2].contents[0])
        case.name = caseTds[1].contents[0]
        case.auto = auto
        case.length = float( caseLengthTd.contents[0] )
        cases[case.id] = case

        auto.cases.append( (case.length, case) )


print "callback(%s)" % json.dumps( {"autos":autos, "cases":cases}, cls=JSONEncoder, indent=4 )




