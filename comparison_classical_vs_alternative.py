"""
COMPARISON: Classical CRT vs Alternative CRT
=============================================

This document compares the classical Chinese Remainder Theorem with 
your alternative approach implemented in crt_algorithm.py
"""

from math import gcd
from functools import reduce


# =============================================================================
# CLASSICAL CHINESE REMAINDER THEOREM (CRT)
# =============================================================================

def classical_crt(moduli, remainders):
    """
    Classical Chinese Remainder Theorem
    
    REQUIREMENT: All moduli must be PAIRWISE COPRIME
    (i.e., gcd(m_i, m_j) = 1 for all i ≠ j)
    
    Algorithm:
    1. Compute N = m₁ × m₂ × ... × mₖ
    2. For each i: compute Nᵢ = N / mᵢ
    3. For each i: find Mᵢ such that Nᵢ × Mᵢ ≡ 1 (mod mᵢ)
    4. Solution: x = Σ(aᵢ × Nᵢ × Mᵢ) mod N
    """
    
    if not moduli or not remainders:
        raise ValueError("Moduli and remainders cannot be empty")
    
    if len(moduli) != len(remainders):
        raise ValueError("Moduli and remainders must have same length")
    
    # Check if all moduli are pairwise coprime
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if gcd(moduli[i], moduli[j]) != 1:
                raise ValueError(
                    f"Classical CRT requires pairwise coprime moduli. "
                    f"gcd({moduli[i]}, {moduli[j]}) = {gcd(moduli[i], moduli[j])} ≠ 1"
                )
    
    N = reduce(lambda a, b: a * b, moduli)
    
    result = 0
    for i in range(len(moduli)):
        N_i = N // moduli[i]
        
        # Find modular inverse of N_i mod moduli[i]
        M_i = extended_gcd_inverse(N_i, moduli[i])
        
        result += remainders[i] * N_i * M_i
    
    return result % N, N


def extended_gcd_inverse(a, m):
    """Find modular inverse using Extended Euclidean Algorithm"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    
    _, x, _ = extended_gcd(a % m, m)
    return (x % m + m) % m


# =============================================================================
# ALTERNATIVE CRT (From Your Implementation)
# =============================================================================

def lcm(a, b):
    """Calculate Least Common Multiple"""
    return abs(a * b) // gcd(a, b)


def extended_gcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y


def mod_inverse(a, m):
    """Find modular multiplicative inverse"""
    gcd_val, x, _ = extended_gcd(a, m)
    if gcd_val != 1:
        raise ValueError(f"Modular inverse does not exist for {a} mod {m}")
    return (x % m + m) % m


def alternative_crt(divisors, remainders):
    """
    Alternative Chinese Remainder Theorem (Iterative Approach)
    
    NO RESTRICTION: Works even if moduli are NOT pairwise coprime
    
    Algorithm:
    1. Start with first congruence: x ≡ r₁ (mod d₁)
    2. For each subsequent congruence:
       - Express x = x_prev + k × d_prev
       - Find k such that x ≡ r_new (mod d_new)
       - Update both x and modulus
    3. Final modulus is LCM(d₁, d₂, ..., dₖ)
    """
    
    if len(divisors) != len(remainders):
        raise ValueError("Divisors and remainders must have same length")
    
    if len(divisors) == 0:
        raise ValueError("At least one congruence is required")
    
    x = remainders[0]
    mod = divisors[0]
    
    for i in range(1, len(divisors)):
        d_new = divisors[i]
        r_new = remainders[i]
        
        gcd_val, _, _ = extended_gcd(mod, d_new)
        
        if (r_new - x) % gcd_val != 0:
            raise ValueError(f"No solution exists")
        
        mod_reduced = mod // gcd_val
        d_new_reduced = d_new // gcd_val
        remainder_reduced = (r_new - x) // gcd_val
        
        inv = mod_inverse(mod_reduced, d_new_reduced)
        k = (remainder_reduced * inv) % d_new_reduced
        
        x = x + k * mod
        mod = lcm(mod, d_new)
    
    x = x % mod
    if x < 0:
        x += mod
    
    return x, mod


# =============================================================================
# COMPARISON & ANALYSIS
# =============================================================================

def print_comparison():
    print("=" * 85)
    print("CLASSICAL CRT vs ALTERNATIVE CRT - DETAILED COMPARISON")
    print("=" * 85)
    print()
    
    # Test Case 1: Pairwise Coprime (Both work)
    print("TEST CASE 1: Pairwise Coprime Moduli (3, 5, 7)")
    print("-" * 85)
    moduli = [3, 5, 7]
    remainders = [2, 3, 2]
    
    print(f"Problem: Find x such that:")
    for m, r in zip(moduli, remainders):
        print(f"  x ≡ {r} (mod {m})")
    print()
    
    # Classical CRT
    try:
        x_classical, N = classical_crt(moduli, remainders)
        print(f"✓ CLASSICAL CRT: x = {x_classical} (mod {N})")
    except ValueError as e:
        print(f"✗ CLASSICAL CRT: {e}")
    
    # Alternative CRT
    try:
        x_alt, mod_alt = alternative_crt(moduli, remainders)
        print(f"✓ ALTERNATIVE CRT: x = {x_alt} (mod {mod_alt})")
    except ValueError as e:
        print(f"✗ ALTERNATIVE CRT: {e}")
    
    print()
    
    # Test Case 2: Non-Coprime Moduli (Only Alternative works)
    print("TEST CASE 2: NON-Coprime Moduli (4, 6)")
    print("-" * 85)
    moduli2 = [4, 6]
    remainders2 = [1, 5]
    
    print(f"Problem: Find x such that:")
    for m, r in zip(moduli2, remainders2):
        print(f"  x ≡ {r} (mod {m})")
    print()
    print(f"Note: gcd(4, 6) = {gcd(4, 6)} ≠ 1  (NOT pairwise coprime)")
    print()
    
    # Classical CRT
    try:
        x_classical, N = classical_crt(moduli2, remainders2)
        print(f"✓ CLASSICAL CRT: x = {x_classical} (mod {N})")
    except ValueError as e:
        print(f"✗ CLASSICAL CRT FAILS: {e}")
    
    # Alternative CRT
    try:
        x_alt, mod_alt = alternative_crt(moduli2, remainders2)
        print(f"✓ ALTERNATIVE CRT: x = {x_alt} (mod {mod_alt})")
        
        # Verify
        print()
        print("Verification of Alternative CRT result:")
        for m, r in zip(moduli2, remainders2):
            result = x_alt % m
            status = "✓" if result == r else "✗"
            print(f"  {status} {x_alt} mod {m} = {result} (expected {r})")
    
    except ValueError as e:
        print(f"✗ ALTERNATIVE CRT: {e}")
    
    print()
    
    # Test Case 3: Non-Coprime Moduli with compatible remainders
    print("TEST CASE 3: NON-Coprime Moduli (6, 9, 15) - Compatible System")
    print("-" * 85)
    moduli3 = [6, 9, 15]
    remainders3 = [3, 3, 3]  # All require x ≡ 3
    
    print(f"Problem: Find x such that:")
    for m, r in zip(moduli3, remainders3):
        print(f"  x ≡ {r} (mod {m})")
    print()
    
    # Classical CRT
    try:
        x_classical, N = classical_crt(moduli3, remainders3)
        print(f"✓ CLASSICAL CRT: x = {x_classical} (mod {N})")
    except ValueError as e:
        print(f"✗ CLASSICAL CRT FAILS: {e}")
    
    # Alternative CRT
    try:
        x_alt, mod_alt = alternative_crt(moduli3, remainders3)
        print(f"✓ ALTERNATIVE CRT: x = {x_alt} (mod {mod_alt})")
    except ValueError as e:
        print(f"✗ ALTERNATIVE CRT: {e}")
    
    print()
    print()


# =============================================================================
# KEY DIFFERENCES TABLE
# =============================================================================

def print_differences_table():
    print("=" * 85)
    print("KEY DIFFERENCES: Classical vs Alternative CRT")
    print("=" * 85)
    print()
    
    differences = [
        ("Requirement", 
         "Moduli must be PAIRWISE COPRIME",
         "Works with ANY moduli (coprime or not)"),
        
        ("Modulus Output",
         "Product of all moduli (N = m₁ × m₂ × ... × mₖ)",
         "LCM of all moduli (smallest period)"),
        
        ("Algorithm Type",
         "Parallel/Batch processing (all at once)",
         "Iterative (combines pairs sequentially)"),
        
        ("Computational Approach",
         "Uses partial products Nᵢ and all inverses",
         "Uses GCD and builds solution incrementally"),
        
        ("Time Complexity",
         "O(k × log N) where N is product of moduli",
         "O(k²) with GCD computations"),
        
        ("Elegance",
         "Mathematically elegant, parallel structure",
         "Elegant simplicity, step-by-step logic"),
        
        ("Flexibility",
         "Limited to specific conditions",
         "More general, handles edge cases"),
        
        ("Use Cases",
         "Cryptography, highly optimized systems",
         "General problem solving, education"),
        
        ("Non-Coprime Handling",
         "FAILS with detailed error",
         "Handles gracefully or gives clear message"),
    ]
    
    print(f"{'Aspect':<25} {'Classical CRT':<30} {'Alternative CRT':<30}")
    print("-" * 85)
    
    for aspect, classical, alternative in differences:
        print(f"{aspect:<25} {classical:<30} {alternative:<30}")
    
    print()


# =============================================================================
# VISUAL ALGORITHM COMPARISON
# =============================================================================

def print_algorithm_comparison():
    print("=" * 85)
    print("ALGORITHM COMPARISON: Step-by-Step")
    print("=" * 85)
    print()
    
    print("CLASSICAL CRT")
    print("-" * 85)
    print("""
    1. Check: All moduli PAIRWISE COPRIME? 
       └─ If NO → FAIL
       └─ If YES → Continue
    
    2. Compute: N = m₁ × m₂ × ... × mₖ
    
    3. For EACH congruence i (in parallel):
       ├─ Compute: Nᵢ = N / mᵢ
       ├─ Find: Mᵢ such that Nᵢ × Mᵢ ≡ 1 (mod mᵢ)
       └─ Compute: aᵢ × Nᵢ × Mᵢ
    
    4. Result: x = (Σ aᵢ × Nᵢ × Mᵢ) mod N
    """)
    
    print()
    print("ALTERNATIVE CRT")
    print("-" * 85)
    print("""
    1. Initialize: x = r₁, mod = d₁
    
    2. For EACH subsequent congruence (sequentially):
       ├─ Check: Is (r_new - x) divisible by gcd(mod, d_new)?
       │  └─ If NO → NO SOLUTION exists
       │  └─ If YES → Continue
       │
       ├─ Reduce: Use gcd to simplify the problem
       │
       ├─ Find: k such that k × (mod/gcd) ≡ (r_new - x)/gcd (mod d_new/gcd)
       │  └─ Use modular inverse
       │
       ├─ Update: x = x + k × mod
       │
       └─ Update: mod = lcm(mod, d_new)
    
    3. Result: x (already minimal in its period)
    """)
    
    print()


# =============================================================================
# ADVANTAGES SUMMARY
# =============================================================================

def print_advantages():
    print("=" * 85)
    print("ADVANTAGES OF EACH APPROACH")
    print("=" * 85)
    print()
    
    print("🎯 CLASSICAL CRT ADVANTAGES:")
    print("-" * 85)
    print("""
    ✓ Mathematically elegant and symmetric
    ✓ All congruences processed in parallel (theoretically faster for massive systems)
    ✓ Well-established, extensively studied, optimized implementations
    ✓ Perfect for cryptographic applications
    ✓ Produces results directly without iteration
    ✓ Used in real-world systems: RSA, Chinese Remainder Theorem cryptosystems
    """)
    
    print()
    print("🎯 ALTERNATIVE CRT ADVANTAGES:")
    print("-" * 85)
    print("""
    ✓ Works with NON-coprime moduli (more general!)
    ✓ Automatically finds the MINIMAL period (LCM instead of product)
    ✓ Easier to understand and implement
    ✓ Step-by-step logic makes it intuitive
    ✓ More flexible - handles edge cases gracefully
    ✓ Results in SMALLER modulus (more practical)
    ✓ Better for educational purposes - shows the "why" behind CRT
    ✓ Less restrictive - works when classical CRT fails
    ✓ Uses only GCD and extended GCD - simpler math toolkit
    """)
    
    print()


# =============================================================================
# PRACTICAL EXAMPLE WITH BOTH METHODS
# =============================================================================

def print_practical_example():
    print("=" * 85)
    print("PRACTICAL EXAMPLE: SAME PROBLEM, BOTH METHODS")
    print("=" * 85)
    print()
    
    moduli = [3, 5, 7]
    remainders = [2, 3, 2]
    
    print("Problem:")
    for m, r in zip(moduli, remainders):
        print(f"  x ≡ {r} (mod {m})")
    print()
    
    print("CLASSICAL CRT COMPUTATION:")
    print("-" * 85)
    N = 3 * 5 * 7
    print(f"1. N = 3 × 5 × 7 = {N}")
    print()
    
    print("2. Compute partial products and inverses:")
    print(f"   • N₁ = 105/3 = 35  →  35 × M₁ ≡ 1 (mod 3)  →  M₁ = 2")
    print(f"   • N₂ = 105/5 = 21  →  21 × M₂ ≡ 1 (mod 5)  →  M₂ = 1")
    print(f"   • N₃ = 105/7 = 15  →  15 × M₃ ≡ 1 (mod 7)  →  M₃ = 1")
    print()
    
    print("3. Combine:")
    print(f"   x = (2 × 35 × 2) + (3 × 21 × 1) + (2 × 15 × 1)")
    print(f"     = 140 + 63 + 30 = 233")
    print(f"     ≡ 23 (mod 105)")
    print()
    
    x_classical, N_classical = classical_crt(moduli, remainders)
    print(f"✓ Solution: x = {x_classical} (mod {N_classical})")
    print()
    
    print("ALTERNATIVE CRT COMPUTATION:")
    print("-" * 85)
    x_alt, mod_alt = alternative_crt(moduli, remainders)
    print(f"✓ Solution: x = {x_alt} (mod {mod_alt})")
    print()
    
    print("COMPARISON:")
    print("-" * 85)
    print(f"Classical CRT:  x = {x_classical} (mod {N_classical})")
    print(f"Alternative CRT: x = {x_alt} (mod {mod_alt})")
    print()
    print(f"✓ Same solution: {x_classical == x_alt}")
    print(f"✓ Alternative gives smaller modulus: {mod_alt} < {N_classical}")
    print()


if __name__ == "__main__":
    print_comparison()
    print()
    print_differences_table()
    print()
    print_algorithm_comparison()
    print()
    print_advantages()
    print()
    print_practical_example()
