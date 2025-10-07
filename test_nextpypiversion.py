import pytest

from nextpypiversion import DuneVersion

@pytest.mark.parametrize("ipt, expt", [(("2.10.0", "2.11-git"), "2.11.0.0"),
                                       (("2.10.2.3", "2.11-git"), "2.11.0.0"),
                                       (("2.11.2.3", "2.11-git"), "2.11.2.4"),
                                       (("2.11.0.3", "2.11-git"), "2.11.0.4")])
def test(ipt, expt):
    last, base = ipt
    l = DuneVersion(last)
    b = DuneVersion(base)
    n = b.next(l)
    assert expt == str(n)

if __name__ == '__main__':
    test(("2.10.2.3", "2.11-git"), "2.11.0.0")
