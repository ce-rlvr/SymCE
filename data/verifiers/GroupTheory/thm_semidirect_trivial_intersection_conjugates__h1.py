import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            H = witness.get('H')
            g = witness.get('g')
        else:
            G, N, H, g = witness
    except Exception:
        return [False, False]

    # H_1: Let g be an arbitrary element of G
    h1 = False
    try:
        if hasattr(G, 'contains'):
            h1 = bool(G.contains(g))
        elif hasattr(G, 'elements'):
            h1 = g in G.elements
        else:
            h1 = g in G
    except Exception:
        h1 = False

    # neg_Q: The intersection N \cap gHg^{-1} is NOT the trivial subgroup {e}
    neg_q = False
    try:
        N_elements = set(N.elements) if hasattr(N, 'elements') else set(N)
        H_elements = set(H.elements) if hasattr(H, 'elements') else set(H)
        
        try:
            g_inv = ~g
        except Exception:
            try:
                g_inv = g.inv()
            except Exception:
                g_inv = g**(-1)
                
        gHg_inv_elements = set()
        for h in H_elements:
            gHg_inv_elements.add(g * h * g_inv)
            
        intersect = N_elements.intersection(gHg_inv_elements)
        
        is_trivial = False
        if len(intersect) == 1:
            elem = list(intersect)[0]
            is_id = False
            if hasattr(elem, 'is_Identity') and elem.is_Identity:
                is_id = True
            elif hasattr(elem, 'is_identity') and elem.is_identity:
                is_id = True
            elif hasattr(elem, 'shape') and len(elem.shape) == 2 and elem.shape[0] == elem.shape[1] and elem == eye(elem.shape[0]):
                is_id = True
            elif elem == 1:
                is_id = True
            
            if is_id:
                is_trivial = True
                
        neg_q = not is_trivial
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: g is an element of G",
    "¬Q: The intersection N \\cap gHg^{-1} is not the trivial subgroup {e}"
]

N_HYP = 1
NEG_Q_INDEX = 1