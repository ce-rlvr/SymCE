import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
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
    witness is expected to be a tuple (n, M) or a dict {'n': n, 'M': M}
    representing the ring Z_n and a subset M.
    """
    try:
        if isinstance(witness, dict):
            n = witness['n']
            M = witness['M']
        else:
            n, M = witness
        n = int(n)
        M = set(int(x) for x in M)
    except Exception:
        return [False, False]
        
    if n < 2:
        return [False, False]
        
    # H_1: M is a proper ideal of R
    try:
        h1_ok = False
        if M.issubset(set(range(n))) and len(M) > 0 and 1 not in M:
            add_closed = all((a + b) % n in M for a in M for b in M)
            mul_closed = all((a * r) % n in M for a in M for r in range(n))
            h1_ok = add_closed and mul_closed
    except Exception:
        h1_ok = False

    # neg_Q: M is a maximal ideal if and only if for every element x in R, exactly one of the elements x and 1-x belongs to M.
    # We need this equivalence to FAIL.
    try:
        # Check if M is maximal
        is_max = True
        for x in range(n):
            if x not in M:
                ideal_gen = set()
                for m in M:
                    for r in range(n):
                        ideal_gen.add((m + r * x) % n)
                if 1 not in ideal_gen:
                    is_max = False
                    break
        
        # Check condition P: for all x, exactly one of x and 1-x is in M
        cond_P = True
        for x in range(n):
            in_x = x in M
            in_1_minus_x = (1 - x) % n in M
            if in_x == in_1_minus_x:
                cond_P = False
                break
                
        neg_q_ok = (is_max != cond_P)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: M is a proper ideal of R",
    "¬Q: The equivalence (M is maximal iff for all x, exactly one of x and 1-x is in M) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1