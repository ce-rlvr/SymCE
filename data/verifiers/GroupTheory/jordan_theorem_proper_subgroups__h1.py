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
    h1 = False
    neg_q = False
    
    try:
        G_elems = None
        H_elems = None
        
        # Unpack witness
        if hasattr(witness, 'G') and hasattr(witness, 'H'):
            G = witness.G
            H = witness.H
        else:
            G, H = witness
            
        # Check H_1: H is a proper subgroup of G
        if hasattr(H, 'is_proper_subgroup'):
            h1 = bool(H.is_proper_subgroup(G))
        elif hasattr(H, 'is_subgroup') and hasattr(G, 'order'):
            h1 = bool(H.is_subgroup(G) and H.order() < G.order())
        else:
            G_elems = []
            for i, g in enumerate(G):
                if i > 2000: raise ValueError("Group G is too large or infinite")
                G_elems.append(g)
            H_elems = []
            for i, h in enumerate(H):
                if i > 2000: raise ValueError("Group H is too large or infinite")
                H_elems.append(h)
            
            # H must be a subset of G, and G must have at least one element not in H
            h1 = all(h in G_elems for h in H_elems) and any(g not in H_elems for g in G_elems)
            
        # Check neg_Q: The union of conjugates of H is NOT strictly contained in G (i.e., it equals G)
        if hasattr(G, 'union_of_conjugates_equals'):
            neg_q = bool(G.union_of_conjugates_equals(H))
        else:
            if G_elems is None:
                G_elems = []
                for i, g in enumerate(G):
                    if i > 2000: raise ValueError("Group G is too large or infinite")
                    G_elems.append(g)
                H_elems = []
                for i, h in enumerate(H):
                    if i > 2000: raise ValueError("Group H is too large or infinite")
                    H_elems.append(h)
                    
            all_in_conjugates = True
            for a in G_elems:
                is_conj = False
                for g in G_elems:
                    # Compute g^-1 * a * g
                    try:
                        ginv = g**-1
                    except Exception:
                        try:
                            ginv = ~g
                        except Exception:
                            ginv = g.inv()
                            
                    conj = ginv * a * g
                    if conj in H_elems:
                        is_conj = True
                        break
                
                if not is_conj:
                    all_in_conjugates = False
                    break
                    
            neg_q = all_in_conjugates
            
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a proper subgroup of G",
    "¬Q: The union of conjugates of H is not strictly contained in G"
]

N_HYP = 1
NEG_Q_INDEX = 1