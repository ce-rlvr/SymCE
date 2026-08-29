import sympy
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
# Witnesses can use an integer n to represent the finite commutative ring Z/nZ.
# S and I should be iterables of integers representing subsets of Z/nZ.

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should represent a ring R (as Z/nZ), a multiplicatively closed subset S, and an ideal I.
    Format expected: tuple (n, S, I) or dict {'R': n, 'S': S, 'I': I}.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            I = witness.get('I')
        else:
            R, S, I = witness
            
        if isinstance(R, int):
            n = R
        elif hasattr(R, '__len__'):
            n = len(R)
        else:
            n = int(R)
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring
    try:
        # We restrict to finite rings Z/nZ with n >= 2 for verifiable counterexamples
        h1 = isinstance(n, int) and n >= 2
    except Exception:
        h1 = False

    # H_2: S is a multiplicatively closed subset of R not containing 0
    try:
        if not h1:
            h2 = False
        else:
            S_mod = set(int(e) % n for e in S)
            if 0 in S_mod:
                h2 = False
            else:
                h2 = all((a * b) % n in S_mod for a in S_mod for b in S_mod)
    except Exception:
        h2 = False

    # ¬Q: I is not a prime ideal of R
    try:
        if not h1:
            neg_q = False
        else:
            I_mod = set(int(e) % n for e in I)
            
            # Verify that I is actually an ideal of R
            is_ideal = True
            if 0 not in I_mod:
                is_ideal = False
            else:
                for a in I_mod:
                    for b in I_mod:
                        if (a + b) % n not in I_mod:
                            is_ideal = False
                    for r in range(n):
                        if (a * r) % n not in I_mod:
                            is_ideal = False
                            
            # Check if I is a prime ideal
            is_prime = False
            if is_ideal and len(I_mod) < n:  # Must be a proper ideal to be prime
                is_prime = True
                for a in range(n):
                    for b in range(n):
                        if (a * b) % n in I_mod:
                            if a not in I_mod and b not in I_mod:
                                is_prime = False
                                break
                    if not is_prime:
                        break
                        
            # The conclusion is "I is a prime ideal".
            # We want the negation to be true, so I must NOT be a prime ideal.
            # To ensure the witness is well-typed, we require I to be a valid ideal.
            neg_q = is_ideal and not is_prime
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R not containing 0",
    "¬Q: I is not a prime ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2