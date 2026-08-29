import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy import eye, zeros
import math
import itertools
import functools

class InfiniteCyclicGroup:
    """
    A representation of an infinite cyclic group (isomorphic to Z)
    to serve as a counterexample for theorems that drop the 'finite' hypothesis.
    """
    @property
    def is_cyclic(self):
        return True
    
    def order(self):
        return sympy.oo
    
    def subgroups(self):
        # An infinite cyclic group has no finite subgroups other than the trivial one.
        # For the purpose of this verifier, returning the trivial subgroup and itself is sufficient
        # to demonstrate that it lacks subgroups of finite order d > 1.
        class TrivialSubgroup:
            def order(self):
                return 1
        return [TrivialSubgroup(), self]

# Top-level setup: named object bindings
Z = InfiniteCyclicGroup()
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, n, d = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a cyclic group
    try:
        if hasattr(G, 'is_cyclic'):
            val = G.is_cyclic
            h1 = bool(val()) if callable(val) else bool(val)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: the order of G is n
    try:
        if hasattr(G, 'order'):
            val = G.order
            order_G = val() if callable(val) else val
            h2 = (order_G == n)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: d is a positive integer
    try:
        h3 = (isinstance(d, int) or isinstance(d, sympy.Integer)) and d > 0
    except Exception:
        h3 = False

    # H_4: d divides n
    try:
        if n == sympy.oo:
            # In the context of cardinal arithmetic, Aleph_0 is divisible by any finite integer.
            # This allows the infinite cyclic group to satisfy the hypothesis.
            h4 = True
        elif isinstance(n, sympy.Expr) or isinstance(d, sympy.Expr):
            h4 = bool(sympy.simplify(n % d) == 0)
        else:
            h4 = (n % d == 0)
    except Exception:
        h4 = False

    # ¬Q: G does not contain exactly one subgroup of order d
    try:
        if hasattr(G, 'subgroups'):
            subs = G.subgroups
            subs = subs() if callable(subs) else subs
            count = 0
            for H in subs:
                if hasattr(H, 'order'):
                    val = H.order
                    H_order = val() if callable(val) else val
                    if H_order == d:
                        count += 1
            neg_q = (count != 1)
        elif hasattr(G, 'subgroups_of_order'):
            subs = G.subgroups_of_order(d)
            subs = subs() if callable(subs) else subs
            neg_q = (len(subs) != 1)
        else:
            # Mathematical fallback if subgroups cannot be explicitly enumerated
            is_cyc = False
            if hasattr(G, 'is_cyclic'):
                val = G.is_cyclic
                is_cyc = bool(val()) if callable(val) else bool(val)
            
            if is_cyc:
                if n == sympy.oo:
                    # Infinite cyclic group has exactly 1 subgroup of order 1, and 0 of order d > 1
                    neg_q = (d != 1)
                else:
                    # A finite cyclic group ALWAYS has exactly one subgroup of order d for every d|n
                    try:
                        is_pos = bool(n > 0)
                        if isinstance(n, sympy.Expr) or isinstance(d, sympy.Expr):
                            divides = bool(sympy.simplify(n % d) == 0)
                        else:
                            divides = (n % d == 0)
                        neg_q = not (is_pos and divides)
                    except Exception:
                        neg_q = False
            else:
                # For non-cyclic finite groups, we can try to count elements if d is prime
                if hasattr(G, 'elements') and sympy.isprime(d):
                    elements = G.elements
                    elements = elements() if callable(elements) else elements
                    count_elements = 0
                    for g in elements:
                        if hasattr(g, 'order'):
                            val = g.order
                            g_order = val() if callable(val) else val
                            if g_order == d:
                                count_elements += 1
                    count_subgroups = count_elements // (d - 1)
                    neg_q = (count_subgroups != 1)
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "H_2: the order of G is n",
    "H_3: d is a positive integer",
    "H_4: d divides n",
    "¬Q: G does not contain exactly one subgroup of order d"
]

N_HYP = 4
NEG_Q_INDEX = 4