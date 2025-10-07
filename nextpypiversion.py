#!/usr/bin/env python3

class DuneVersion:
    # length of DuneVersion is 4, i.e. major.minor.micro.post, e.g. 2.11.0.0
    _length = 4

    def __init__(self, version : (str,list,tuple), emptyvalue = -1 ):
        if isinstance(version, str):
            self.version = self._convertToList( version )
        else:
            assert isinstance(version, (list,tuple))
            self.version = list(version)

        # pad remaining slots with emptyvalue
        self.version = self.version + [emptyvalue]*(self._length-len(self.version))
        assert len(self.version) == self._length


    def _convertToList(self, version : str ):
        version = version.strip()
        # remove git string from version
        version = version.replace('-git', '')
        v = version.split('.')
        # convert to integer
        v = [int(s) for s in v]
        assert len(v) >= 2
        return v

    # operator <
    def __lt__(self, other):
        smaller = False
        for v1,v2 in zip(self.version, other.version):
            if v1 > v2:
                return False
        return not(self == other)

    # operator <=
    def __leq__(self, other):

        for v1,v2 in zip(self.version, other.version):
            if v1 > v2:
                return False
        return True

    # operator ==
    def __eq__( self, other ):
        for v1,v2 in zip(self.version, other.version):
            if v1 !=  v2:
                return False
        return True

    # convert to string (-1 is ignored)
    def __str__(self):
        s = str(self.version[0])
        for i in range(1,len(self.version)):
            if self.version[i] >= 0:
                s += '.' + str(self.version[i])
        return s

    # increment version number based on previous version
    def next( self, prev ):

        significant = sum([ v >= 0 for v in self.version])
        # check base version
        prevbase = DuneVersion( prev.version[:significant] )
        # if base version is smaller, then take base version and pad with zero
        if prevbase < self:
            return DuneVersion( self.version[:significant], emptyvalue = 0 )
        else:
            # otherwise base should be identical
            assert prevbase == self

        assert len(self.version) == len(prev.version) == self._length
        v = []
        larger = False
        for i in range(len(self.version)):
            v1 = self.version[i]
            v2 = prev.version[i]
            if v1 > v2:
                v.append(v1)
                larger = True
            elif i >= len(self.version)-1 and not larger:
                v.append(max(v1,v2)+1)
            else:
                # make all entries at least 0
                v.append(max(max(v1,v2), 0))
        return DuneVersion( v )

    def __repr__(self):
        return str(self)

if __name__ == '__main__':
    import requests
    import sys

    # next version is major.minor.micro.post
    # if micro was not provided it is set to 0
    # post is computed from the last version

    try:
        package = sys.argv[1]
        basever = sys.argv[2]
    except IndexError:
        print(f"Usage: {sys.argv[0]} <package name> <major.minor or major.minor.micro>")
        sys.exit(1)

    baseversion = DuneVersion( basever )
    response  = requests.get(f'https://pypi.org/pypi/{package}/json')
    try:
        lastver = response.json()['info']['version']
    except KeyError:
        print(f"Package {package} not found!")
        sys.exit(1)

    lv = DuneVersion( lastver )
    nextver = baseversion.next( lv )

    #print(f"""Package {package}:
    #Last version: {lv}
    #Next version: {nextver}""")
    print(nextver)
