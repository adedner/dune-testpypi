from nextpypiversion import DuneVersion


def increment( version : str ):
    v = DuneVersion( version )
    b = DuneVersion( v.version[:2] )
    n = v.next( b )
    return v < n

def test_increment():
    version = "2.10.0"
    assert increment( version )
