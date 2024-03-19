class Jar:
    @classmethod
    def _determine_form(cls, n):
        return 'cookie' if n == 1 else 'cookies'

    def __init__(self, capacity=12):
        self._size = 0
        self.capacity = capacity

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("Positive integers only.")
        elif n < self._size:
            raise ValueError(
                f"Jar needs to fit at least {self._size} {Jar._determine_form(self._size)} currently in jar.")
        self._capacity = n

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, n):
        if not isinstance(n, int):
            raise ValueError(f"Invalid number of cookies for this jar.")
        elif n < 0:
            raise ValueError(
                f"Not enough {Jar._determine_form(self._size - n)}. Withdrawing {self._size - n} {Jar._determine_form(self._size - n)} with {self._size} {Jar._determine_form(self._size)} available.")
        elif n > self._capacity:
            raise ValueError(f"Exceeded max jar capacity of {self._capacity} {Jar._determine_form(self._capacity)}.")
        self._size = n

    # to add cookies
    def deposit(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("Positive numbers only to deposit cookies.")
        self.size += n

    # to withdraw cookies
    def withdraw(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("Positive numbers only to withdraw cookies.")
        self.size -= n
        return n

    # to transfer cookies to another jar
    def transfer(self, n, other):
        pre_transfer_size = self._size
        try:
            other.deposit(self.withdraw(n))
        except ValueError as error_message:
            print(f'Transfer Failed: {error_message}')

            # reversing cookies withdrawn from self when it cannot be deposited to the other jar due to other jar's capacity issue.
            if isinstance(n, int) and pre_transfer_size >= n > other.capacity:
                self.deposit(n)  # effectively returned to pre_transfer_size

    def __str__(self):
        return "🍪" * self._size


def main():
    jar1 = Jar(10)
    jar2 = Jar(1)
    jar1.size = 5
    print(f"jar1: {jar1}")
    print(f"jar2: {jar2}")
    jar1.transfer("cat", jar2)
    print(f"jar1: {jar1}")
    print(f"jar2: {jar2}")


if __name__ == "__main__":
    main()
