import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # Extract witness components
    try:
        if isinstance(witness, dict):
            N = witness.get('N')
            H = witness.get('H')
            n1 = witness.get('n1')
            n2 = witness.get('n2')
            h1 = witness.get('h1')
            h2 = witness.get('h2')
        else:
            w = list(witness)
            if len(w) == 6:
                N, H, n1, n2, h1, h2 = w
            elif len(w) >= 7:
                G, N, H, n1, n2, h1, h2 = w[:7]
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: n1, n2 are elements of N
    try:
        h1_ok = (n1 in N) and (n2 in N)
    except Exception:
        h1_ok = False

    # H_2: h1, h2 are elements of H
    try:
        h2_ok = (h1 in H) and (h2 in H)
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion fails
    # Conclusion states: (n1*h1)*(n2*h2) == (n1*(h1*n2*h1^-1))*(h1*h2)
    # AND n1*(h1*n2*h1^-1) in N
    # AND h1*h2 in H
    try:
        inv_h1 = h1**-1
        part1 = n1 * h1 * n2 * inv_h1
        part2 = h1 * h2
        
        prod1 = n1 * h1
        prod2 = n2 * h2
        
        prod_eq = (prod1 * prod2 == part1 * part2)
        
        def is_in(elem, coll):
            try:
                if elem in coll:
                    return True
            except Exception:
                pass
            try:
                for x in coll:
                    if x == elem:
                        return True
            except Exception:
                pass
            return False

        in_N = is_in(part1, N)
        in_H = is_in(part2, H)
        
        # The conclusion holds if all three conditions are met.
        # We want the negation of the conclusion.
        neg_q = not (prod_eq and in_N and in_H)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: n1, n2 are elements of N",
    "H_2: h1, h2 are elements of H",
    "¬Q: The product formula fails or the factors are not in N and H respectively"
]

N_HYP = 2
NEG_Q_INDEX = 2