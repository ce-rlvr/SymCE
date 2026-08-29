import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    witness is expected to be a tuple: (n, a, factors)
    where factors is a list of tuples (p_i, e_i) representing the prime factorization.
    """
    try:
        n, a, factors = witness
    except Exception:
        return [False, False, False]
        
    # H_1: n is a positive integer with prime factorization n = p_1^{e_1} ... p_k^{e_k}
    try:
        h1 = False
        if isinstance(n, int) and n > 0:
            if isinstance(factors, (list, tuple)):
                prod = 1
                valid_factors = True
                for item in factors:
                    if not isinstance(item, (list, tuple)) or len(item) != 2:
                        valid_factors = False
                        break
                    p, e = item
                    if not (isinstance(p, int) and isinstance(e, int)):
                        valid_factors = False
                        break
                    if not sympy.isprime(p):
                        valid_factors = False
                        break
                    if e <= 0:
                        valid_factors = False
                        break
                    prod *= (p ** e)
                if valid_factors and prod == n:
                    h1 = True
    except Exception:
        h1 = False

    # H_2: a is an integer
    try:
        h2 = isinstance(a, int)
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails
    try:
        def has_sol(val, mod):
            if mod == 1:
                return True
            if mod > 100000:
                raise ValueError("Modulus too large for safe execution")
            val_mod = val % mod
            for x in range(mod):
                if (x * x) % mod == val_mod:
                    return True
            return False
            
        P = has_sol(a, n)
        Q = True
        for p, e in factors:
            if not has_sol(a, p ** e):
                Q = False
                break
                
        # The conclusion is P == Q. The negated conclusion is P != Q.
        neg_q = (P != Q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer with prime factorization n = p_1^{e_1} ... p_k^{e_k}",
    "H_2: a is an integer",
    "¬Q: The congruence x^2 ≡ a (mod n) has a solution iff x^2 ≡ a (mod p_i^{e_i}) has a solution for all i FAILS"
]

N_HYP = 2
NEG_Q_INDEX = 2