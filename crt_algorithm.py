"""
Alternative Chinese Remainder Theorem Implementation
=====================================================

This algorithm finds the smallest positive number x such that:
- x ≡ r₁ (mod d₁)
- x ≡ r₂ (mod d₂)
- x ≡ r₃ (mod d₃)
- ...
- x ≡ rₙ (mod dₙ)

Where:
- d₁, d₂, d₃, ... are divisors (moduli)
- r₁, r₂, r₃, ... are remainders
"""

from math import gcd
from functools import reduce


def lcm(a, b):
    """Calculate Least Common Multiple"""
    return abs(a * b) // gcd(a, b)


def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm
    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd_val, x, y


def mod_inverse(a, m):
    """
    Find modular multiplicative inverse of a modulo m
    Returns x such that (a * x) % m == 1
    """
    gcd_val, x, _ = extended_gcd(a, m)
    if gcd_val != 1:
        raise ValueError(f"Modular inverse does not exist for {a} mod {m}")
    return (x % m + m) % m


def alternative_crt(divisors, remainders):
    """
    Alternative Chinese Remainder Theorem
    
    Args:
        divisors: List of divisors (d₁, d₂, d₃, ...)
        remainders: List of remainders (r₁, r₂, r₃, ...)
    
    Returns:
        Smallest positive integer x satisfying all congruences
    
    Approach:
    ---------
    Solve iteratively:
    1. Start with first congruence: x ≡ r₁ (mod d₁)
    2. For each subsequent congruence, find x that satisfies both:
       - Previous result: x ≡ r_prev (mod d_prev)
       - New congruence: x ≡ r_curr (mod d_curr)
    3. General form: x = r_prev + k * d_prev (find k such that x ≡ r_curr (mod d_curr))
    """
    
    if len(divisors) != len(remainders):
        raise ValueError("Divisors and remainders must have same length")
    
    if len(divisors) == 0:
        raise ValueError("At least one congruence is required")
    
    # Start with the first congruence
    x = remainders[0]
    mod = divisors[0]
    
    # Iteratively solve each pair of congruences
    for i in range(1, len(divisors)):
        d_new = divisors[i]
        r_new = remainders[i]
        
        # We need to find x such that:
        # x ≡ x (mod mod) [previous result]
        # x ≡ r_new (mod d_new) [new congruence]
        
        # General form: x = x + k * mod
        # We need: (x + k * mod) ≡ r_new (mod d_new)
        # => k * mod ≡ (r_new - x) (mod d_new)
        
        gcd_val, _, _ = extended_gcd(mod, d_new)
        
        if (r_new - x) % gcd_val != 0:
            raise ValueError(f"No solution exists: congruence {i} is incompatible")
        
        # Reduce the problem
        mod_reduced = mod // gcd_val
        d_new_reduced = d_new // gcd_val
        remainder_reduced = (r_new - x) // gcd_val
        
        # Find k such that k * mod_reduced ≡ remainder_reduced (mod d_new_reduced)
        inv = mod_inverse(mod_reduced, d_new_reduced)
        k = (remainder_reduced * inv) % d_new_reduced
        
        # Update solution
        x = x + k * mod
        mod = lcm(mod, d_new)
    
    # Ensure positive result
    x = x % mod
    if x < 0:
        x += mod
    
    return x, mod


# ============================================================================
# EXAMPLE: Solving the system of congruences
# ============================================================================

def example():
    """
    Example: Find the smallest positive number x such that:
    - x ≡ 2 (mod 3)   [leaves remainder 2 when divided by 3]
    - x ≡ 3 (mod 5)   [leaves remainder 3 when divided by 5]
    - x ≡ 2 (mod 7)   [leaves remainder 2 when divided by 7]
    """
    
    print("=" * 70)
    print("ALTERNATIVE CHINESE REMAINDER THEOREM - EXAMPLE")
    print("=" * 70)
    print()
    
    divisors = [3, 5, 7]
    remainders = [2, 3, 2]
    
    print("Problem Statement:")
    print("-" * 70)
    print("Find the smallest positive integer x such that:")
    for d, r in zip(divisors, remainders):
        print(f"  • x ≡ {r} (mod {d})  [x leaves remainder {r} when divided by {d}]")
    print()
    
    # Solve using the algorithm
    print("Solution Process:")
    print("-" * 70)
    
    solution, modulus = alternative_crt(divisors, remainders)
    
    print(f"✓ Result: x = {solution}")
    print(f"✓ The solution repeats every {modulus} integers")
    print()
    
    # Verification
    print("Verification:")
    print("-" * 70)
    all_valid = True
    for d, r in zip(divisors, remainders):
        remainder = solution % d
        valid = (remainder == r)
        status = "✓" if valid else "✗"
        print(f"{status} {solution} ÷ {d} = {solution // d} remainder {remainder} (expected {r})")
        all_valid = all_valid and valid
    
    print()
    if all_valid:
        print(f"✓✓✓ All congruences satisfied! Answer: {solution} ✓✓✓")
    else:
        print("✗ Verification failed")
    
    print()
    
    # Show all solutions in range [0, 105]
    print("All solutions in range [0, 105]:")
    print("-" * 70)
    solutions_in_range = [solution + k * modulus for k in range(5) if solution + k * modulus <= 105]
    print(f"{solutions_in_range}")
    print()


# ============================================================================
# ADDITIONAL EXAMPLES
# ============================================================================

def example2():
    """Example 2: A simpler case"""
    print("=" * 70)
    print("EXAMPLE 2: Simpler Case")
    print("=" * 70)
    print()
    
    divisors = [4, 6]
    remainders = [1, 5]
    
    print("Problem:")
    print(f"  • x ≡ {remainders[0]} (mod {divisors[0]})")
    print(f"  • x ≡ {remainders[1]} (mod {divisors[1]})")
    print()
    
    try:
        solution, modulus = alternative_crt(divisors, remainders)
        print(f"Solution: x = {solution}")
        print(f"Repeats every: {modulus}")
        print()
        
        print("Verification:")
        for d, r in zip(divisors, remainders):
            remainder = solution % d
            print(f"  {solution} mod {d} = {remainder} (expected {r}) {'✓' if remainder == r else '✗'}")
    
    except ValueError as e:
        print(f"Error: {e}")
    
    print()


def example3():
    """Example 3: More divisors"""
    print("=" * 70)
    print("EXAMPLE 3: Four Congruences")
    print("=" * 70)
    print()
    
    divisors = [2, 3, 5, 11]
    remainders = [1, 2, 3, 4]
    
    print("Problem:")
    for d, r in zip(divisors, remainders):
        print(f"  • x ≡ {r} (mod {d})")
    print()
    
    solution, modulus = alternative_crt(divisors, remainders)
    
    print(f"Solution: x = {solution}")
    print(f"LCM of all moduli: {modulus}")
    print()
    
    print("Verification:")
    for d, r in zip(divisors, remainders):
        remainder = solution % d
        status = "✓" if remainder == r else "✗"
        print(f"  {status} {solution} mod {d} = {remainder} (expected {r})")


if __name__ == "__main__":
    example()
    example2()
    example3()
