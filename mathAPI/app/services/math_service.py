# math_service.py
#
# This file contains the core mathematical logic used by the FastAPI endpoints.
# It defines three functions that perform the required operations:
#   - compute_pow(x, y): raises x to the power of y
#   - compute_fib(n): calculates the nth Fibonacci number
#   - compute_factorial(n): calculates the factorial of n
#
# These functions are pure (no side effects), efficient, and reusable.

from functools import lru_cache

def compute_pow(x: float, y: float) -> float:
    return x ** y

@lru_cache(maxsize=128)
def compute_fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@lru_cache(maxsize=128)
def compute_factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be ≥ 0")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
