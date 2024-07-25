"""
@file mathlib.py
@brief File containing math library.

@author
- Vojtěch Gajdušek (xgajduv00)
- co-author Tomáš Lajda (xlajdat00)
@date April 11, 2024
"""

MAX_PRECISION = 14
TOLERANCE = 1e-10


def add(num1, num2):
    """
    @brief Function to add two numbers.

    @param num1: First number.
    @param num2: Second number.

    @return Sum of numbers num1 and num2.
    """
    return round(num1 + num2, MAX_PRECISION)


def sub(num1, num2):
    """
    @brief Function to subtract two numbers.

    @param num1: First number.
    @param num2: Second number.

    @return Difference of numbers num1 and num2 (num1 - num2).
    """
    return round(num1 - num2, MAX_PRECISION)


def mul(num1, num2):
    """
    @brief Function to multiply two numbers.

    @param num1: First number.
    @param num2: Second number.

    @return Product of num1 and num2 (num1 * num2).
    """
    return round(num1 * num2, MAX_PRECISION)


def div(dividend, divisor):
    """
    @brief Function to divide two numbers.

    @param dividend: The number to be divided (numerator).
    @param divisor: The number by which the dividend is divided (denominator).

    @return The quotient of dividend divided by divisor.

    @exception ValueError: If the divisor is zero.
    """
    if divisor == 0:
        raise ZeroDivisionError

    return round(dividend / divisor, MAX_PRECISION)


def mod(dividend, divisor):
    """
    @brief Function to compute the modulo operation.

    @param dividend: The number to be divided.
    @param divisor: The number by which the dividend is divided.

    @return The remainder after dividing dividend by divisor.

    @exception ValueError: If the divisor is zero.
    """
    if divisor == 0:
        raise ZeroDivisionError

    remainder = abs(dividend) % abs(divisor)

    if divisor < 0:
        remainder = -remainder

    if abs(divisor - remainder) < TOLERANCE:
        return 0

    return round(remainder, MAX_PRECISION)


def abs(num):
    """
    @brief Function to calculate the absolute value of a number.

    @param num: The input number.

    @return The absolute value of the input number.
    """
    if num < 0:
        return -num
    else:
        return num


def fac(num):
    """
    @brief Function to compute the factorial of a non-negative integer.

    @param num: The non-negative integer.

    @return The factorial of the input integer.

    @exception ValueError: If number is not a natural number.
    @exception ValueError: If number is bigger than 100.
    """
    if not isinstance(num, int) or num < 0:
        raise TypeError("Number must be a natural number.")

    if num > 100:
        raise ValueError("Factorial computation is limited to numbers up to 100.")

    if num == 0:
        return 1

    result = 1
    for i in range(1, num + 1):
        result *= i

    return float(result)


def pow(base, exponent):
    """
    @brief Function to compute the power of a number.

    @param base: The base number.
    @param exponent: The exponent.

    @return The result of raising base to the power of exponent.

    @exception ValueError: If exponent is not a natural number.
    @exception ValueError: If exponent and base is zero.
    """
    if not isinstance(exponent, int) or exponent < 0:
        raise TypeError("Exponent must be a natural number.")

    if base == 0 and exponent == 0:
        raise ValueError("0^0 is undefined.")

    result = base ** exponent

    if result >= 1e100:
        return float('inf')
    else:
        return round(result, MAX_PRECISION)


def root(base, index):
    """
    @brief Function to compute the nth root of a base using Newton's method.

    @param base: The base whose root is to be calculated.
    @param index: The root to be calculated (e.g., 2 for square root).

    @return Nth root of the given base.

    @exception ValueError: If index is not a natural base.
    @exception ValueError: If index is not divisible by 2 and base is negative.
    """
    if not isinstance(index, int) or index < 0:
        raise TypeError("Index must be a natural number.")

    if (index == 0):
        raise ValueError("Index cannot be zero.")

    if base < 0 and index % 2 == 0:
        raise ValueError("Cannot compute even root of negative number.")

    if base == 0:
        return 0

    if base < 0:
        return round(-((-base) ** (1 / index)), MAX_PRECISION)

    return round(base ** (1 / index), MAX_PRECISION)