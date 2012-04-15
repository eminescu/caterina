#!/usr/bin/python -u


import urllib2, urllib, cPickle

class CacherEntry:
    def __init__(self, url, info, data):
        self.url = url
        self.info = info
        self.data = data


class Cacher:
    def __init__(self, path=".cache"):
        self.path = path

    def get(self, url):
        fn = "%s/%s" % (self.path, urllib.quote_plus(url))
        try:
            with open(fn, "rb") as fo:
                #print "Cache hit"
                return cPickle.load( fo )

        except:
            #print "Cache miss"

            req = urllib2.Request( url )
            #req.add_header('Referer', 'http://www.python.org/')
            #req.add_header('User-agent', 'Mozilla/5.0')
            conn = urllib2.urlopen(req)

            entry = CacherEntry( conn.geturl(), conn.info(), conn.read() )

            conn.close()

            with open(fn, "wb") as fo:
                cPickle.dump(entry, fo)

            return entry


if __name__ == "__main__":
    import sys
    C = Cacher()
    print len( C.get( sys.argv[1] ).data )



