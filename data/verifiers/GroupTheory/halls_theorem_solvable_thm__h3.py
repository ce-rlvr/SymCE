import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
import math
import itertools
from sympy.ntheory import factorint

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def has_subgroup_of_order(G, m):
    m = int(m)
    if m <= 0:
        return False
    order = int(G.order())
    
    # By Lagrange's theorem, the order of a subgroup must divide the order of the group
    if order % m != 0:
        return False
        
    if m == 1 or m == order:
        return True
        
    # By Sylow's First Theorem and properties of p-groups, 
    # if m is a prime power dividing the group order, a subgroup of order m always exists.
    factors = factorint(m)
    if len(factors) == 1:
        return True
        
    # For small combinations, we can brute-force search for a subgroup
    if math.comb(order, m) <= 10000:
        elements = list(G.elements)
        identity = next((p for p in elements if p.is_Identity), None)
        if identity is None:
            # Fallback to find identity
            for p in elements:
                if p * p == p:
                    identity = p
                    break
                    
        for subset in itertools.combinations(elements, m):
            if identity not in subset:
                continue
            subset_set = set(subset)
            closed = True
            # Check closure under multiplication (sufficient for finite subsets)
            for a in subset_set:
                for b in subset_set:
                    if a * b not in subset_set:
                        closed = False
                        break
                if not closed:
                    break
            if closed:
                return True
        return False
        
    # If we cannot definitively determine existence, raise to prevent false positives in neg_Q
    raise NotImplementedError(f"Subgroup existence check for order {m} in group of order {order} is not implemented.")

def conditions(witness):
    try:
        G, m, n = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(G.is_solvable)
    except Exception:
        h2 = False
        
    try:
        h3 = math.gcd(int(m), int(n)) == 1
    except Exception:
        h3 = False
        
    try:
        has_sub = has_subgroup_of_order(G, int(m))
        neg_q = not has_sub
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a solvable group",
    "H_3: The greatest common divisor of m and n is 1",
    "¬Q: G does not contain a subgroup of order m"
]

N_HYP = 3
NEG_Q_INDEX = 3