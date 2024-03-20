import pytest
from jar import Jar

SMALL_TESTER = 6
DEFAULT_TESTER = 12
EXTRA_TESTER = 24
NEGATIVE_TESTER = -1
NON_INT_TESTER = "cat"


def test_initializing_capacity():
    jar1 = Jar()
    jar2 = Jar(SMALL_TESTER)
    jar3 = Jar(EXTRA_TESTER)
    assert jar1.capacity == DEFAULT_TESTER
    assert jar2.capacity == SMALL_TESTER
    assert jar3.capacity == EXTRA_TESTER


def test_non_positive_int_capacity():
    with pytest.raises(ValueError):
        Jar(NON_INT_TESTER)
    with pytest.raises(ValueError):
        Jar(NEGATIVE_TESTER)


def test_deposit():
    jar = Jar()
    jar.deposit(SMALL_TESTER)
    assert jar.size == SMALL_TESTER


def test_over_deposit():
    jar = Jar()
    with pytest.raises(ValueError):
        jar.deposit(EXTRA_TESTER)


def test_non_positive_int_deposit():
    jar = Jar()
    with pytest.raises(ValueError):
        jar.deposit(NON_INT_TESTER)
    with pytest.raises(ValueError):
        jar.deposit(NEGATIVE_TESTER)


def test_withdraw():
    jar = Jar()
    jar.size = DEFAULT_TESTER  # Bypass jar.deposit() method to avoid the method itself has errors
    jar.withdraw(SMALL_TESTER)  # Withdrawing SMALL_TESTER amount
    assert jar.size == (DEFAULT_TESTER - SMALL_TESTER)


def test_over_withdraw():
    jar = Jar()
    with pytest.raises(ValueError):
        jar.withdraw(EXTRA_TESTER)


def test_non_positive_int_withdraw():
    jar = Jar()
    with pytest.raises(ValueError):
        jar.withdraw(NON_INT_TESTER)
    with pytest.raises(ValueError):
        jar.withdraw(NEGATIVE_TESTER)


def test_transfer():
    jar1 = Jar()
    jar2 = Jar()
    jar1.size = SMALL_TESTER
    jar2.size = SMALL_TESTER

    jar1.transfer(SMALL_TESTER, jar2)
    assert jar1.size == (SMALL_TESTER - SMALL_TESTER)
    assert jar2.size == (SMALL_TESTER + SMALL_TESTER)


def test_over_withdraw_transfer():
    jar1 = Jar()
    jar2 = Jar()
    jar1.size = SMALL_TESTER
    jar2.size = 0
    jar1_pretransfer = jar1.size
    jar2_pretransfer = jar2.size
    jar1.transfer(SMALL_TESTER + 1, jar2)

    # Transferring SMALL_TESTER + 1, when SMALL_TESTER amount available.
    # jar1 and jar2 need to have the same number of cookies they had before transfer as transfer fails
    assert jar1.size == jar1_pretransfer
    assert jar2.size == jar2_pretransfer


def test_over_capacity_transfer():
    jar1 = Jar(EXTRA_TESTER)
    jar2 = Jar()
    jar1.size = EXTRA_TESTER
    jar2.size = 0
    jar1_pretransfer = jar1.size
    jar2_pretransfer = jar2.size

    # Transferring DEFAULT_TESTER + 1 when jar2 only fits DEFAULT_TESTER (12).
    # jar1 and jar2 need to have the same number of cookies they had before transfer as transfer fails
    jar1.transfer(DEFAULT_TESTER + 1, jar2)
    assert jar1.size == jar1_pretransfer
    assert jar2.size == jar2_pretransfer


def test_non_positive_int_transfer():
    jar1 = Jar()
    jar2 = Jar()
    jar1.size = SMALL_TESTER
    jar2.size = 0
    jar1_pretransfer = jar1.size
    jar2_pretransfer = jar2.size

    # Transferring invalid NEGATIVE_TESTER number of cookies.
    # jar1 and jar2 need to have the same number of cookies they had before transfer as transfer fails
    jar1.transfer(NEGATIVE_TESTER, jar2)
    assert jar1.size == jar1_pretransfer
    assert jar2.size == jar2_pretransfer

    # Transferring invalid NON_INT_TESTER of cookies.
    # jar1 and jar2 need to have the same number of cookies they had before transfer as transfer fails
    jar1.transfer(NON_INT_TESTER, jar2)
    assert jar1.size == jar1_pretransfer
    assert jar2.size == jar2_pretransfer


def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar.deposit(SMALL_TESTER)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪"
    jar.deposit(DEFAULT_TESTER - SMALL_TESTER)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"

