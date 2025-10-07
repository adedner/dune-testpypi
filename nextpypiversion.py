#!/usr/bin/env python3

import requests
import sys

class DuneVersion:
    def __init__(self, version : (str,list) ):
        if isinstance(version, str):
            self.version = self._convert( version )
        else:
            self.version = version.copy()
        assert len(self.version) == 4

    def _convert(self, version : str ):
        # remove git string from version
        version = version.replace('-git', '')
        v = version.split('.')
        v = [int(s) for s in v]
        assert len(v) >= 2

        while len(v) < 4:
            v.append(-1)
        return v

    def __le__(self, other):
        for v1,v2 in zip(self.version, other.version):
            if v1 >= v2:
                return False
        return True

    def __leq__(self, other):

        for v1,v2 in zip(self.version, other.version):
            if v1 > v2:
                return False
        return True

    def __eq__( self, other ):
        for v1,v2 in zip(self.version, other.version):
            if v1 !=  v2:
                return False
        return True

    def __str__(self):
        s = str(self.version[0])
        for i in range(1,len(self.version)):
            if self.version[i] >= 0:
                s += '.' + str(self.version[i])
        return s

    def next( self, prev ):
        v = []
        larger = False
        assert len(self.version) == len(prev.version)
        for i in range(len(self.version)):
            v1 = self.version[i]
            v2 = prev.version[i]
            if v1 > v2:
                v.append(v1)
                larger = True
            elif i == len(self.version)-1 and not larger:
                v.append(max(v1,v2)+1)
            else:
                # make all entries at least 0
                v.append(max(max(v1,v2), 0))
        return DuneVersion( v )

    def __repr__(self):
        return str(self)

# next version is major.minor.micro.post
# if micro was not provided it is set to 0
# post is computed from the last version

try:
    package = sys.argv[1]
    basever = sys.argv[2]
except IndexError:
    print(f"Usage: {sys.argv[0]} <package name> <major.minor or major.minor.micro>")
    sys.exit(1)

# remove potential -git
baseversion = DuneVersion( basever )
response  = requests.get(f'https://pypi.org/pypi/{package}/json')
try:
    lastver = response.json()['info']['version']
except KeyError:
    print(f"Package {package} not found!")
    sys.exit(1)

lv = DuneVersion( lastver )
nextver = baseversion.next( lv )

print(f"""Package {package}:
Last version: {lv}
Next version: {nextver}""")
