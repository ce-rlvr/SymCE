import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.ntheory import factorint
from math import lcm

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        G, g = witness
        
        # H_1: G is a finite abelian p-group and g in G
        h1 = False
        if getattr(G, 'is_abelian', False):
            order = G.order() if callable(getattr(G, 'order', None)) else getattr(G, 'order', None)
            if order is not None:
                factors = factorint(order)
                if len(factors) == 1:
                    if hasattr(G, 'elements'):
                        elements = list(G.elements)
                    elif hasattr(G, 'generate'):
                        elements = list(G.generate())
                    else:
                        elements = []
                    if g in elements:
                        h1 = True
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            if hasattr(G, 'elements'):
                elements_G = list(G.elements)
            elif hasattr(G, 'generate'):
                elements_G = list(G.generate())
            else:
                elements_G = []
                
            identity = G.identity
            
            def get_order(x):
                if hasattr(x, 'order'):
                    return x.order() if callable(x.order) else x.order
                k = 1
                curr = x
                while curr != identity:
                    curr = curr * x
                    k += 1
                return k

            orders_G = [get_order(x) for x in elements_G]
            
            H_elements = set()
            current = identity
            while current not in H_elements:
                H_elements.add(current)
                current = current * g
                
            orders_H = [get_order(x) for x in H_elements]
            
            coset_reps = []
            seen = set()
            for x in elements_G:
                if x not in seen:
                    coset_reps.append(x)
                    for h in H_elements:
                        seen.add(x * h)
                        
            orders_Q = []
            for x in coset_reps:
                k = 1
                curr = x
                while curr not in H_elements:
                    curr = curr * x
                    k += 1
                orders_Q.append(k)
                
            orders_sum = []
            for oh in orders_H:
                for oq in orders_Q:
                    orders_sum.append(lcm(oh, oq))
                    
            # For finite abelian groups, H is a direct summand of G iff G is isomorphic to H ⊕ (G/H).
            # This is true iff the multiset of element orders of G matches that of H ⊕ (G/H).
            is_direct_summand = (sorted(orders_G) == sorted(orders_sum))
            neg_q = not is_direct_summand
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite abelian p-group and g in G",
    "¬Q: <g> is not a direct summand of G"
]
N_HYP = 1
NEG_Q_INDEX = 1