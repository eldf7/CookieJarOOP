import pytest
from jar import Jar


def test_initializing_capacity():
    jar1 = Jar()
    jar2 = Jar(24)
    assert jar1.capacity == 12
    assert jar2.capacity == 24


def test_non_positive_int_capacity():
    with pytest.raises(ValueError):
        Jar("cat")
    with pytest.raises(ValueError):
        Jar(-1)


def test_deposit():
    jar = Jar()
    jar.deposit(5)
    assert jar.size == 5


def test_over_deposit():
    jar = Jar()
    with pytest.raises(ValueError):
        jar.deposit(20)


def test_non_positive_int_deposit():
    jar = Jar()
    with pytest.raises(ValueError):
        jar.deposit("cat")
    with pytest.raises(ValueError):
        jar.deposit(-1)


def test_withdraw():
    jar = Jar()
    jar.size = 5  # Bypass jar.deposit() method to avoid the method itself has errors
    jar.withdraw(4)
    assert jar.size == 1


def test_over_withdraw():
    jar = Jar()
    with pytest.raises(ValueError):
        jar.withdraw(20)


def test_non_positive_int_withdraw():
    jar = Jar()
    with pytest.raises(ValueError):
        jar.withdraw("cat")
    with pytest.raises(ValueError):
        jar.withdraw(-1)


def test_transfer():
    jar1 = Jar()
    jar2 = Jar(24)
    jar1.size = 6
    jar2.size = 6

    jar1.transfer(6, jar2)
    assert jar1.size == 0
    assert jar2.size == 12


def test_over_withdraw_transfer():
    jar1 = Jar()
    jar2 = Jar()
    jar1.size = 5
    jar2.size = 0
    original1 = jar1.size
    original2 = jar2.size
    jar1.transfer(6, jar2)

    # Transferring 6, when 5 available.
    # jar1 and jar2 need to have the same number of cookies they had before transfer as transfer failed
    assert jar1.size == original1
    assert jar2.size == original2


def test_over_deposit_transfer():
    jar1 = Jar(24)
    jar2 = Jar()
    jar1.size = 20
    jar2.size = 0
    original1 = jar1.size
    original2 = jar2.size
    jar1.transfer(13, jar2)

    # Transferring 13 when jar2 only fits 12.
    # jar1 and jar2 need to have the same number of cookies they had before transfer as transfer failed
    assert jar1.size == original1
    assert jar2.size == original2


def test_non_positive_int_transfer():
    jar1 = Jar()
    jar2 = Jar()
    jar1.size = 5
    jar2.size = 0
    original1 = jar1.size
    original2 = jar2.size
    jar1.transfer(-1, jar2)

    # Transferring invalid -1 number of cookies.
    # jar1 and jar2 need to have the same number of cookies they had before transfer as transfer failed
    assert jar1.size == original1
    assert jar2.size == original2

    # Transferring invalid "cat" number of cookies.
    # jar1 and jar2 need to have the same number of cookies they had before transfer as transfer failed
    jar1.transfer("cat", jar2)
    assert jar1.size == original1
    assert jar2.size == original2


def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar.deposit(1)
    assert str(jar) == "🍪"
    jar.deposit(11)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"

