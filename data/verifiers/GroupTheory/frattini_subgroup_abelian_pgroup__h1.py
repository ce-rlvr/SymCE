import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros
from sympy.ntheory import primefactors
import math
import itertools
import functools

# Top-level setup for potential witness objects
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
    # The dropped hypothesis from the true theorem is that "p is a prime".
    # Without it, p can be composite (e.g., p=4, G=Z4), which makes the conclusion fail.
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            try:
                elements = list(G.elements)
                p = len(elements)
            except Exception:
                p = 2
    except Exception:
        return [False, False, False]

    # H_1: G is a finite abelian p-group
    try:
        h1 = False
        if getattr(G, 'is_abelian', False):
            p_val = int(p)
            if p_val >= 1:
                elements = list(G.elements)
                order = len(elements)
                if order == 1:
                    h1 = True
                elif p_val > 1:
                    n = order
                    while n % p_val == 0:
                        n //= p_val
                    if n == 1:
                        h1 = True
    except Exception:
        h1 = False

    # H_2: Phi(G) is the Frattini subgroup of G
    # This is definitional; we just verify G is a valid group.
    try:
        h2 = getattr(G, 'is_group', False) or hasattr(G, 'elements')
    except Exception:
        h2 = False

    # ¬Q: Phi(G) != pG
    try:
        elements = list(G.elements)
        order = len(elements)
        p_val = int(p)
        
        if order == 1:
            phi = set(elements)
        else:
            # For a finite abelian group, the Frattini subgroup is the intersection 
            # of qG for all prime factors q of the group's order.
            primes = primefactors(order)
            phi = set(elements)
            for q in primes:
                qG = set(g**q for g in elements)
                phi = phi.intersection(qG)
                
        # pG in multiplicative notation is the set of p-th powers
        pG = set(g**p_val for g in elements)
        
        neg_q = (phi != pG)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite abelian p-group",
    "H_2: Phi(G) is the Frattini subgroup of G",
    "¬Q: Phi(G) != pG"
]

N_HYP = 2
NEG_Q_INDEX = 2