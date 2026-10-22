import pytest

from ipmanager.core.cidr import Cidr, CidrSet


def test_bare_ip_is_a_full_bitmask():
    assert str(Cidr('10.204.145.1')) == '10.204.145.1/32'


def test_host_bits_are_normalized_away():
    """Bits not covered by the bitmask are zeroed out on construction."""
    assert Cidr('10.0.0.5/8') == Cidr('10.0.0.0/8')
    assert str(Cidr('10.0.0.5/8')) == '10.0.0.0/8'


@pytest.mark.parametrize(
    'value', ['', 'not an ip', '10.0.0', '10.0.0.256', '10.0.0.0/33']
)
def test_invalid_values_are_rejected(value):
    with pytest.raises(ValueError):
        Cidr(value)


def test_empty_set():
    empty = CidrSet()

    assert len(empty) == 0
    assert str(empty) == ''
    assert Cidr('10.0.0.1') not in empty


def test_sibling_ranges_collapse():
    """Two halves of an address space are stored as the single range covering both."""
    cidrset = CidrSet(Cidr('0.0.0.0/1'), Cidr('128.0.0.0/1'))

    assert len(cidrset) == 1
    assert str(cidrset) == '0.0.0.0/0'


def test_adding_a_contained_range_is_a_no_op():
    cidrset = CidrSet(Cidr('10.0.0.0/8'))
    cidrset.add(Cidr('10.1.2.3'))

    assert len(cidrset) == 1
    assert str(cidrset) == '10.0.0.0/8'


def test_contains_only_fully_covered_ranges():
    cidrset = CidrSet(Cidr('10.0.0.0/8'))

    assert Cidr('10.1.2.3') in cidrset
    assert Cidr('10.1.0.0/16') in cidrset
    assert Cidr('11.1.2.3') not in cidrset
    # /7 is larger than the /8 in the set, so it is not fully covered
    assert Cidr('10.0.0.0/7') not in cidrset


def test_iteration_yields_the_ranges_in_ascending_order():
    cidrset = CidrSet(Cidr('192.168.0.1'), Cidr('10.0.0.0/8'))

    assert [str(cidr) for cidr in cidrset] == ['10.0.0.0/8', '192.168.0.1/32']


def test_equality_compares_contents():
    assert CidrSet(Cidr('10.0.0.0/8')) == CidrSet(Cidr('10.0.0.0/8'))
    assert not CidrSet(Cidr('10.0.0.0/8')) == CidrSet(Cidr('11.0.0.0/8'))
    assert not CidrSet(Cidr('10.0.0.0/8')) == CidrSet()


def test_equality_requires_a_cidrset():
    with pytest.raises(ValueError):
        CidrSet() == Cidr('10.0.0.1')


def test_clone_is_independent_of_the_original():
    original = CidrSet(Cidr('10.0.0.0/8'))
    clone = original.clone()
    clone.add(Cidr('192.168.0.1'))

    assert len(original) == 1
    assert len(clone) == 2


def test_union():
    a = CidrSet(Cidr('10.0.0.0/8'))
    b = CidrSet(Cidr('192.168.0.1'))

    assert str(a + b) == '10.0.0.0/8, 192.168.0.1/32'
    # the operands are left untouched
    assert str(a) == '10.0.0.0/8'
    assert str(b) == '192.168.0.1/32'


def test_difference_splits_the_remaining_space():
    """Removing a subrange expands the set into the ranges that still cover the rest."""
    a = CidrSet(Cidr('10.0.0.0/8'))
    b = CidrSet(Cidr('10.1.0.0/16'))
    difference = a - b

    assert len(difference) == 8
    assert Cidr('10.1.2.3') not in difference
    assert Cidr('10.2.3.4') in difference
    # the operands are left untouched
    assert str(a) == '10.0.0.0/8'
    assert str(b) == '10.1.0.0/16'


def test_removing_a_range_that_is_absent():
    cidrset = CidrSet(Cidr('10.0.0.0/8'))
    cidrset.remove(Cidr('192.168.0.1'))

    assert str(cidrset) == '10.0.0.0/8'

    empty = CidrSet()
    empty.remove(Cidr('10.0.0.0/8'))

    assert len(empty) == 0
