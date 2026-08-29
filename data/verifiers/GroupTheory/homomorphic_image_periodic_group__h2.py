import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, H, f), checks if it is a valid counterexample to the conjecture.
    G and H are groups, f is a mapping from G to H.
    """
    try:
        G, H, f = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G and H are groups, and f is a function from G to H
    try:
        h1 = hasattr(G, 'elements') and hasattr(G, 'identity') and \
             hasattr(H, 'elements') and hasattr(H, 'identity')
        if h1:
            image = set()
            for g in G.elements:
                if isinstance(f, dict):
                    image.add(f[g])
                else:
                    image.add(f(g))
            # f must map elements of G into H
            if not image.issubset(set(H.elements)):
                h1 = False
    except Exception:
        h1 = False

    # H_2: G is a periodic group (every element has finite order)
    try:
        h2 = True
        for g in G.elements:
            if not hasattr(g, 'order'):
                h2 = False
                break
            ord_g = g.order()
            if ord_g <= 0 or ord_g == float('inf'):
                h2 = False
                break
    except Exception:
        h2 = False

    # ¬Q: The image f(G) is NOT a periodic group
    # This happens if f(G) fails to be a group (not closed under H's operations) 
    # or if it contains an element of infinite order.
    try:
        image = set()
        for g in G.elements:
            if isinstance(f, dict):
                image.add(f[g])
            else:
                image.add(f(g))
                
        is_group_and_periodic = True
        
        # Check if image forms a subgroup of H
        if H.identity not in image:
            is_group_and_periodic = False
        else:
            for a in image:
                if a**-1 not in image:
                    is_group_and_periodic = False
                    break
                for b in image:
                    if a * b not in image:
                        is_group_and_periodic = False
                        break
                if not is_group_and_periodic:
                    break
            
            # If it is a group, check if it is periodic
            if is_group_and_periodic:
                for a in image:
                    if not hasattr(a, 'order'):
                        is_group_and_periodic = False
                        break
                    ord_a = a.order()
                    if ord_a <= 0 or ord_a == float('inf'):
                        is_group_and_periodic = False
                        break
                        
        neg_q = not is_group_and_periodic
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G is a periodic group",
    "¬Q: The image f(G) is not a periodic group"
]

N_HYP = 2
NEG_Q_INDEX = 2