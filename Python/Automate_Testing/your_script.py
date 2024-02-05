import sys


def add_numbers(a, b):
    """
    Add two numbers and return the sum.
    """
    return a + b


def multiply_numbers(a, b):
    """
    Multiply two numbers and return the product.
    """
    return a * b


def divide_numbers(a, b):
    """
    Divide two numbers and return the quotient.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def calculate_factorial(n):
    """
    Calculate the factorial of a number and return the result.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0:
        return 1
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    return factorial


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Please provide two numbers as command-line arguments.")
        sys.exit(1)

    a = int(sys.argv[1])
    b = int(sys.argv[2])

    # Example usage of the functions
    print(add_numbers(a, b))
    print(multiply_numbers(a, b))
    print(divide_numbers(a, b))
    print(calculate_factorial(a))
