import pytest
from jar import Jar

SMALL_TESTER = 6
DEFAULT_TESTER = 12
EXTRA_TESTER = 24
NEGATIVE_TESTER = -1
NON_INT_TESTER = "cat"


def test_initializing_capacity():
    normal_jar = Jar()
    small_jar = Jar(SMALL_TESTER)
    big_jar = Jar(EXTRA_TESTER)
    assert normal_jar.capacity == DEFAULT_TESTER
    assert small_jar.capacity == SMALL_TESTER
    assert big_jar.capacity == EXTRA_TESTER


def test_non_positive_int_capacity():
    with pytest.raises(ValueError):
        Jar(NON_INT_TESTER)
    with pytest.raises(ValueError):
        Jar(NEGATIVE_TESTER)


def test_deposit():
    normal_jar = Jar()
    normal_jar.deposit(SMALL_TESTER)
    assert normal_jar.size == SMALL_TESTER


def test_over_deposit():
    normal_jar = Jar()
    with pytest.raises(ValueError):
        normal_jar.deposit(EXTRA_TESTER)


def test_non_positive_int_deposit():
    normal_jar = Jar()
    with pytest.raises(ValueError):
        normal_jar.deposit(NON_INT_TESTER)
    with pytest.raises(ValueError):
        normal_jar.deposit(NEGATIVE_TESTER)


def test_withdraw():
    normal_jar = Jar()
    normal_jar.size = DEFAULT_TESTER  # Bypass jar.deposit() method to avoid the method itself has errors
    normal_jar.withdraw(SMALL_TESTER)  # Withdrawing SMALL_TESTER amount
    assert normal_jar.size == (DEFAULT_TESTER - SMALL_TESTER)


def test_over_withdraw():
    normal_jar = Jar()
    normal_jar.size = DEFAULT_TESTER

    # Over-withdrawing EXTRA_TESTER amount with DEFAULT_TESTER amount available
    with pytest.raises(ValueError):
        normal_jar.withdraw(EXTRA_TESTER)


def test_non_positive_int_withdraw():
    normal_jar = Jar()
    normal_jar.size = DEFAULT_TESTER

    # Withdrawing invalid negative and non-integer amount
    with pytest.raises(ValueError):
        normal_jar.withdraw(NON_INT_TESTER)
    with pytest.raises(ValueError):
        normal_jar.withdraw(NEGATIVE_TESTER)


def test_transfer():
    normal_jar1 = Jar()
    normal_jar1.size = DEFAULT_TESTER

    normal_jar2 = Jar()
    normal_jar2.size = 0

    normal_jar1.transfer(SMALL_TESTER, normal_jar2)
    assert normal_jar1.size == (DEFAULT_TESTER - SMALL_TESTER)
    assert normal_jar2.size == SMALL_TESTER


def test_over_withdraw_transfer():
    normal_jar1 = Jar()
    normal_jar1.size = SMALL_TESTER
    normal_jar1_pretransfer = normal_jar1.size

    normal_jar2 = Jar()
    normal_jar2.size = 0
    normal_jar2_pretransfer = normal_jar2.size

    # Transferring DEFAULT_TESTER amount with SMALL_TESTER amount available.
    # jar1 and jar2 need to have the same number of cookies they had before transfer as transfer fails
    normal_jar1.transfer(DEFAULT_TESTER, normal_jar2)
    assert normal_jar1.size == normal_jar1_pretransfer
    assert normal_jar2.size == normal_jar2_pretransfer


def test_over_capacity_transfer():
    big_jar = Jar(EXTRA_TESTER)
    big_jar.size = EXTRA_TESTER
    big_jar_pretransfer = big_jar.size

    normal_jar = Jar()
    normal_jar.size = 0
    normal_jar_pretransfer = normal_jar.size

    # Transferring EXTRA_TESTER amount when jar2 only fits DEFAULT_TESTER.
    # jar1 and jar2 need to have the same number of cookies they had before transfer as transfer fails
    big_jar.transfer(EXTRA_TESTER, normal_jar)
    assert big_jar.size == big_jar_pretransfer
    assert normal_jar.size == normal_jar_pretransfer


def test_non_positive_int_transfer():
    normal_jar1 = Jar()
    normal_jar1.size = SMALL_TESTER
    normal_jar1_pretransfer = normal_jar1.size

    normal_jar2 = Jar()
    normal_jar2.size = 0
    normal_jar2_pretransfer = normal_jar2.size

    # Transferring invalid negative number of cookies.
    # jar1 and jar2 need to have the same number of cookies they had before transfer as transfer fails
    normal_jar1.transfer(NEGATIVE_TESTER, normal_jar2)
    assert normal_jar1.size == normal_jar1_pretransfer
    assert normal_jar2.size == normal_jar2_pretransfer

    # Transferring with invalid input that's non integer.
    # jar1 and jar2 need to have the same number of cookies they had before transfer as transfer fails
    normal_jar1.transfer(NON_INT_TESTER, normal_jar2)
    assert normal_jar1.size == normal_jar1_pretransfer
    assert normal_jar2.size == normal_jar2_pretransfer


def test_str():
    normal_jar = Jar()
    assert str(normal_jar) == ""
    normal_jar.deposit(SMALL_TESTER)
    assert str(normal_jar) == "🍪🍪🍪🍪🍪🍪"
    normal_jar.deposit(DEFAULT_TESTER - SMALL_TESTER)
    assert str(normal_jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"

