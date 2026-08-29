import sympy
import math
import itertools
import functools

# ATOMIC CONCLUSION: [h1, h2, neg_q] boolean array evaluated via Z/nZ integer factorization.
# 80/20 LOGIC COMPRESSION: Initial logic and parameters are validated.
# Sub-Conclusion Leaping: Jump directly to prime factorization length for primary ideal check.

# Top-level setup
# Witnesses are expected as integer tuples (n, m) representing R = Z/nZ and I = mZ/nZ.
# No specific named bindings required for this domain.

def conditions(witness) -> list[bool]:
    # Standard processing applied
    try:
        n, m = witness
        
        h1 = isinstance(n, int) and n >= 2
        h2 = isinstance(m, int) and n % m == 0 and m > 1
        
        neg_q = len(sympy.factorint(m)) > 1
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a proper ideal of R",
    "¬Q: I is not a primary ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2