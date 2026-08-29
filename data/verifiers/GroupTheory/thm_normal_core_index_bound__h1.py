import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup: named object bindings
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

def conditions(witness):
    try:
        if len(witness) == 3:
            G, H, N = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = bool(H.is_subgroup(G))
        else:
            if hasattr(G, 'elements'):
                G_elems = set(G.elements)
            else:
                G_elems = set(G)
                
            if hasattr(H, 'elements'):
                H_elems = set(H.elements)
            else:
                H_elems = set(H)
                
            h1 = H_elems.issubset(G_elems)
            for a in H_elems:
                if (a**-1) not in H_elems:
                    h1 = False
                for b in H_elems:
                    if (a * b) not in H_elems:
                        h1 = False
    except Exception:
        h1 = False
        
    # H2: The index of H in G is a finite integer n
    try:
        if hasattr(G, 'order') and hasattr(H, 'order'):
            order_G = G.order()
            order_H = H.order()
        else:
            if hasattr(G, 'elements'):
                order_G = len(list(G.elements))
            else:
                order_G = len(G)
            if hasattr(H, 'elements'):
                order_H = len(list(H.elements))
            else:
                order_H = len(H)
                
        n = order_G // order_H
        h2 = (order_G % order_H == 0) and (n >= 1)
    except Exception:
        h2 = False
        
    # H3: N is the normal core of H in G
    try:
        if hasattr(G, 'elements'):
            G_elems = set(G.elements)
        else:
            G_elems = set(G)
            
        if hasattr(H, 'elements'):
            H_elems = set(H.elements)
        else:
            H_elems = set(H)
            
        N_elements = set(G_elems)
        for g in G_elems:
            conj = set()
            for h in H_elems:
                conj.add(g * h * (g**-1))
            N_elements = N_elements.intersection(conj)
            
        if hasattr(N, 'elements'):
            N_eval_elements = set(N.elements)
        else:
            N_eval_elements = set(N)
            
        h3 = (N_eval_elements == N_elements)
    except Exception:
        h3 = False
        
    # neg_Q: N is a normal subgroup of G and the index of N in G divides n!
    try:
        is_normal = True
        for g in G_elems:
            for n_elem in N_eval_elements:
                if (g * n_elem * (g**-1)) not in N_eval_elements:
                    is_normal = False
                    break
            if not is_normal:
                break
                
        index_N = order_G // len(N_eval_elements)
        divides = (math.factorial(n) % index_N == 0)
        
        q = is_normal and divides
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The index of H in G is a finite integer n",
    "H_3: N is the normal core of H in G",
    "not Q: N is not a normal subgroup of G or the index of N in G does not divide n factorial"
]

N_HYP = 3
NEG_Q_INDEX = 3