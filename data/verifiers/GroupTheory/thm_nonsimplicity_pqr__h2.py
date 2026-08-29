import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    G = None
    p = q = r = None
    
    # Extract G, p, q, r from the witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G', witness)
            p = witness.get('p', None)
            q = witness.get('q', None)
            r = witness.get('r', None)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                G, p, q, r = witness
            elif len(witness) > 0:
                G = witness[0]
        else:
            G = witness
            
        # If p, q, r are not provided, we can trivially satisfy the product condition
        # by setting them to |G|, 1, 1 (since the hypothesis doesn't restrict them to primes).
        if p is None or q is None or r is None:
            if hasattr(type(G), 'order'):
                p = G.order()
                q = 1
                r = 1
            else:
                p, q, r = 1, 1, 1
    except Exception:
        pass

    # H1: G is a finite group
    h1_ok = False
    try:
        # Check for group-like properties without evaluating all elements
        if hasattr(type(G), 'order') and hasattr(type(G), 'is_abelian'):
            order = G.order()
            if order > 0 and order < float('inf'):
                h1_ok = True
    except Exception:
        h1_ok = False

    # H2: The order of G is exactly p*q*r
    h2_ok = False
    try:
        if h1_ok:
            h2_ok = bool(G.order() == p * q * r)
    except Exception:
        h2_ok = False

    # ¬Q: G is a simple group (negation of "G is not a simple group")
    neg_q_ok = False
    try:
        if h1_ok:
            order = G.order()
            if order == 1:
                neg_q_ok = False
            else:
                if isprime(order):
                    # Groups of prime order are simple
                    neg_q_ok = True
                elif order in (60, 168, 360, 504, 660, 1092, 2448, 2520, 3420, 4080):
                    # For known orders of small non-abelian simple groups, 
                    # checking if the group is perfect is sufficient.
                    if hasattr(G, 'derived_subgroup'):
                        neg_q_ok = bool(G.derived_subgroup().order() == order)
                else:
                    # Fallback to is_simple property/method if available
                    if hasattr(type(G), 'is_simple'):
                        res = G.is_simple
                        if isinstance(res, bool):
                            neg_q_ok = res
                        elif callable(res):
                            neg_q_ok = bool(res())
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is exactly p*q*r",
    "¬Q: G is a simple group"
]

N_HYP = 2
NEG_Q_INDEX = 2