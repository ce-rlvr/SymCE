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
    Checks the hypotheses and negated conclusion for the conjecture:
    "Every finite subgroup of the multiplicative group of a field is cyclic."
    
    The witness is expected to be a tuple (F, G), where:
      - F is a SymPy domain representing a field (e.g., sympy.QQ, sympy.GF(5))
      - G is a finite iterable (list, set, etc.) of elements in F
    """
    try:
        F, G = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    def get_one(F):
        if hasattr(F, 'one'): return F.one
        return 1

    def mul(F, a, b):
        if hasattr(F, 'mul'): return F.mul(a, b)
        return a * b

    def is_zero(F, a):
        if hasattr(F, 'zero'): return a == F.zero
        try:
            if a == F(0): return True
        except Exception:
            pass
        return a == 0

    # H_2: G is a subgroup of F^\times
    try:
        h2 = True
        if not G:
            h2 = False
        else:
            one = get_one(F)
            # Check subset of F^\times
            for g in G:
                if (g not in F) or is_zero(F, g):
                    h2 = False
                    break
            # Check closure under multiplication
            if h2:
                for g1 in G:
                    for g2 in G:
                        if mul(F, g1, g2) not in G:
                            h2 = False
                            break
                    if not h2:
                        break
            # Check identity
            if h2:
                if one not in G:
                    h2 = False
            # Check inverses
            if h2:
                for g in G:
                    has_inv = False
                    for h in G:
                        if mul(F, g, h) == one:
                            has_inv = True
                            break
                    if not has_inv:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # H_3: G is finite
    try:
        h3 = hasattr(G, '__iter__') and hasattr(G, '__len__')
        if h3:
            _ = len(G)
    except Exception:
        h3 = False

    # ¬Q: G is not a cyclic group
    try:
        if not h3:
            neg_q = False
        else:
            G_unique = []
            for g in G:
                if g not in G_unique:
                    G_unique.append(g)
            
            is_cyclic = False
            n = len(G_unique)
            one = get_one(F)
            
            for g in G_unique:
                powers = []
                curr = one
                for _ in range(n):
                    curr = mul(F, curr, g)
                    if curr not in powers:
                        powers.append(curr)
                
                # If g generates exactly n distinct elements, and all are in G, it's cyclic
                if len(powers) == n and all(p in G_unique for p in powers):
                    is_cyclic = True
                    break
                    
            neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: G is a subgroup of F^\\times",
    "H_3: G is finite",
    "¬Q: G is not a cyclic group"
]

N_HYP = 3
NEG_Q_INDEX = 3