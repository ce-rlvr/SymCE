import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
V4 = AbelianGroup(2, 2)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: A is a cyclic group of finite order m",
    "¬Q: The tensor product of A and B over the integers is NOT isomorphic to the cyclic group of order gcd(m,n)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    def get_order(obj):
        if callable(obj.order):
            return int(obj.order())
        return int(obj.order)

    def get_elements(obj):
        if callable(obj.elements):
            return list(obj.elements())
        return list(obj.elements)

    def get_generators(obj):
        if callable(obj.generators):
            return list(obj.generators())
        return list(obj.generators)

    try:
        A, B = witness
    except Exception:
        return [False, False]
        
    # H_1: A is a cyclic group of finite order m
    try:
        m = get_order(A)
        h1_ok = False
        for g in get_elements(A):
            if get_order(g) == m:
                h1_ok = True
                break
    except Exception:
        h1_ok = False
        
    # neg_Q: The tensor product of A and B over the integers is NOT isomorphic to the cyclic group of order gcd(m,n)
    try:
        m = get_order(A)
        n = get_order(B)
        target_order = math.gcd(m, n)
        
        gens_K = []
        elements_B = get_elements(B)
        
        # The tensor product A \otimes B over Z, where A is cyclic of order m,
        # is isomorphic to B / (B' B^m). We compute the subgroup K = B' B^m.
        for g in elements_B:
            gens_K.append(g**m)
            
        gens_B = get_generators(B)
        for g in gens_B:
            for h in gens_B:
                gens_K.append(g * h * (~g) * (~h))
                
        K = PermutationGroup(gens_K)
        
        tp_order = n // get_order(K)
        
        is_iso = False
        if tp_order == target_order:
            # Check if the quotient group B/K is cyclic.
            # It is cyclic if there exists an element whose order in B/K equals tp_order.
            for b in elements_B:
                e = 1
                curr = b
                while curr not in K:
                    curr = curr * b
                    e += 1
                if e == tp_order:
                    is_iso = True
                    break
                    
        neg_q_ok = not is_iso
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]