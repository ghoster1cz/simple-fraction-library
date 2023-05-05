def lcm(*numbers):
    """
    Least common multiple
    :param numbers: list of numbers to which find the least common multiple
    :return: Least common multiple of passed numbers
    """
    top = max(numbers)
    done = True
    while True:
        for number in numbers:
            if top % number != 0:
                done = False
        
        if done:
            return top

        top += 1
        done = True
            

def compute_new_numerator(fraction, denominator):
    """
    Used to compute new numerator to new denominator
    :param fraction: fraction used to compute new numerator
    :param denominator: new fraction denominator
    :return: new numerator
    """
    return fraction.numerator * (denominator // fraction.denominator)


def float_to_fraction(number):
    """
    Make a fraction out of float
    :param number: float to be turned into fraction
    :return: fraction representing float number
    """
    decimal_places = len(str(number).split('.')[1])
    return Fraction(int(number * (10 ** decimal_places)), int(10 ** decimal_places))


def float_fraction_parameters_to_integers(numerator, denominator):
    """
    Calculates new numerator and denominator values if one (or both) of the parameters are float
    :param numerator: fraction numerator
    :param denominator: fraction denominator
    :return: integer numerator and denominator
    """
    decimal_point, numerator_decimal_point, denominator_decimal_point = 0, 0, 0

    if numerator.__class__ == float:
        numerator_decimal_point = len(str(numerator).split('.')[1])

    if denominator.__class__ == float:
        denominator_decimal_point = len(str(denominator).split('.')[1])

    decimal_point = max(numerator_decimal_point, denominator_decimal_point)

    return int(numerator * (10 ** decimal_point)), int(denominator * (10 ** decimal_point))


class Fraction:
    def __init__(self, numerator, denominator):
        """
        Initialize new fraction
        :param numerator: fraction numerator
        :param denominator: fraction denominator
        """
        if denominator == 0:
            raise ZeroDivisionError

        if numerator.__class__ == float or denominator.__class__ == float:
            numerator, denominator = float_fraction_parameters_to_integers(numerator, denominator)

        self.numerator = numerator  # top
        self.denominator = denominator  # bottom

    def reducing_number(self):
        """
        Try to find number which can divide numerator and denominator
        :return: Number to reduce fraction or 1 if fraction can't be reduced
        """
        for i in range(abs(self.numerator), 1, -1):
            if self.numerator % i == 0 and self.denominator % i == 0:
                return i

        return 1

    def reduce(self, divisor):
        """
        Reduce fraction by given divisor
        :param divisor: number to use in reduction
        :return: reduced fraction
        """
        return self.numerator//divisor, self.denominator//divisor

    def calculate(self):
        """
        Calculate value of fraction
        :return: Calculate number
        """
        return self.numerator / self.denominator

    def __add__(self, other):
        # If other is number turn it into fraction
        if other.__class__ == int:
            other = Fraction(other, 1)
        elif other.__class__ == float:
            other = float_to_fraction(other)

        if other.__class__ != Fraction:  # check if other is of class Fraction
            raise ValueError("Object is incompatible!")

        denominator = lcm(self.denominator, other.denominator)  # Finds least common multiplier as new denominator

        # Use least common multiplier as divider to compute new numerator value
        numerator = compute_new_numerator(self, denominator) + compute_new_numerator(other, denominator)

        return Fraction(numerator, denominator)

    def __sub__(self, other):
        # If other is number turn it into fraction
        if other.__class__ == int:
            other = Fraction(other, 1)
        elif other.__class__ == float:
            other = float_to_fraction(other)

        if other.__class__ != Fraction:  # check if other is of class Fraction
            raise ValueError("Object is incompatible!")

        denominator = lcm(self.denominator, other.denominator)  # Finds least common multiplier as new denominator

        # Use least common multiplier as divider to compute new numerator value
        numerator = compute_new_numerator(self, denominator) - compute_new_numerator(other, denominator)

        return Fraction(numerator, denominator)

    def __mul__(self, other):
        # If other is number turn it into fraction
        if other.__class__ == int:
            other = Fraction(other, 1)
        elif other.__class__ == float:
            other = float_to_fraction(other)

        if other.__class__ != Fraction:  # check if other is of class Fraction
            raise ValueError("Object is incompatible!")

        denominator = self.denominator * other.denominator
        numerator = self.numerator * other.numerator

        return Fraction(numerator, denominator)

    def __truediv__(self, other):
        # If other is number turn it into fraction
        if other.__class__ == int:
            other = Fraction(other, 1)
        elif other.__class__ == float:
            other = float_to_fraction(other)

        if other.__class__ != Fraction:  # check if other is of class Fraction
            raise ValueError("Object is incompatible!")

        denominator = self.denominator * other.numerator
        numerator = self.numerator * other.denominator

        return Fraction(numerator, denominator)

    def __eq__(self, other):
        if other.__class__ == Fraction:
            return self.reduce(self.reducing_number()) == other.reduce(other.reducing_number())

        elif other.__class__ == int or other.__class__ == float:
            return self.calculate() == other

        raise ValueError("Object is incompatible!")

    def __lt__(self, other):
        if other.__class__ == Fraction:  # check if other is of class Fraction
            return self.calculate() < other.calculate()
        elif other.__class__ == int or other.__class__ == float:
            return self.calculate() < other

        raise ValueError("Object is incompatible!")

    def __le__(self, other):
        if other.__class__ == Fraction:  # check if other is of class Fraction
            return self.calculate() <= other.calculate()
        elif other.__class__ == int or other.__class__ == float:
            return self.calculate() <= other

        raise ValueError("Object is incompatible!")

    def __gt__(self, other):
        if other.__class__ == Fraction:  # check if other is of class Fraction
            return self.calculate() > other.calculate()
        elif other.__class__ == int or other.__class__ == float:
            return self.calculate() > other

        raise ValueError("Object is incompatible!")

    def __ge__(self, other):
        if other.__class__ == Fraction:  # check if other is of class Fraction
            return self.calculate() >= other.calculate()
        elif other.__class__ == int or other.__class__ == float:
            return self.calculate() >= other

        raise ValueError("Object is incompatible!")

    def __str__(self):
        # Represent negative fraction in right format
        if self.denominator < 0:
            self.denominator *= -1
            self.numerator *= -1

        # Simple reduce
        if self.numerator % self.denominator == 0:
            return str(self.numerator // self.denominator)

        # Try to reduce fraction
        divisor = self.reducing_number()
        numerator, denominator = self.reduce(divisor) if divisor != 1 else (self.numerator, self.denominator)

        # Format fraction
        return "{0}/{1}".format(numerator, denominator)
