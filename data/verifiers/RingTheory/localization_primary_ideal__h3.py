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
# We interpret the witness as ideals and subsets in the ring of integers Z.
# A witness is a dictionary {'p': p, 's': s, 'q': q} or a tuple (p, s, q)
# where p generates the prime ideal P, s generates the multiplicatively closed set S,
# and q generates the ideal Q.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = int(witness['p'])
            s_input = witness['s']
            q = int(witness['q'])
        else:
            p = int(witness[0])
            s_input = witness[1]
            q = int(witness[2])
            
        if isinstance(s_input, (list, tuple, set)):
            s_gens = [int(x) for x in s_input]
        else:
            s_gens = [int(s_input)]
    except Exception:
        return [False] * 5

    # H_1: R is a commutative ring
    # We are working in Z, which is a commutative ring.
    h1 = True

    # H_2: P is a prime ideal of R
    try:
        p_abs = abs(p)
        h2 = (p_abs == 0) or sympy.isprime(p_abs)
    except Exception:
        h2 = False

    # H_3: S is a multiplicatively closed subset of R
    # S is generated multiplicatively by s_gens, so it is closed by definition.
    h3 = True

    # H_4: S \cap P is the empty set
    try:
        if p_abs == 0:
            h4 = all(s != 0 for s in s_gens)
        else:
            h4 = all(s % p_abs != 0 for s in s_gens)
    except Exception:
        h4 = False

    # neg_Q: The extended ideal S^{-1}Q is not an S^{-1}P-primary ideal in S^{-1}R
    try:
        q_prime = abs(q)
        for s in s_gens:
            s_abs = abs(s)
            if s_abs > 1:
                for f in sympy.primefactors(s_abs):
                    while q_prime > 0 and q_prime % f == 0:
                        q_prime //= f
        
        if 0 in s_gens:
            is_primary = False
        elif q_prime == 0:
            is_primary = (p_abs == 0)
        elif q_prime == 1:
            is_primary = False
        else:
            if p_abs == 0:
                is_primary = False
            else:
                temp = q_prime
                while temp % p_abs == 0:
                    temp //= p_abs
                is_primary = (temp == 1)
                
        neg_q = not is_primary
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal of R",
    "H_3: S is a multiplicatively closed subset of R",
    "H_4: S \\cap P is the empty set",
    "¬Q: The extended ideal S^{-1}Q is not an S^{-1}P-primary ideal in S^{-1}R"
]

N_HYP = 4
NEG_Q_INDEX = 4