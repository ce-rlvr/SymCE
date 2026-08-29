import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    return list(G)

def conditions(witness) -> list[bool]:
    try:
        elements = get_elements(witness)
        if not elements:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H1: G acts on itself by conjugation, where g \cdot x = gxg^{-1} for all g, x \in G.
    h1_ok = True
    try:
        for g in elements:
            for x in elements:
                conj = g * x * g**-1
                if conj not in elements:
                    h1_ok = False
                    break
            if not h1_ok:
                break
    except Exception:
        h1_ok = False

    # ¬Q: The kernel of this conjugation action is not exactly the center Z(G) of the group.
    neg_q_ok = False
    try:
        kernel = []
        for g in elements:
            is_k = True
            for x in elements:
                if g * x * g**-1 != x:
                    is_k = False
                    break
            if is_k:
                kernel.append(g)
                
        center = []
        for g in elements:
            is_c = True
            for x in elements:
                if g * x != x * g:
                    is_c = False
                    break
            if is_c:
                center.append(g)
                
        # Check if kernel and center contain exactly the same elements
        k_in_c = all(k in center for k in kernel)
        c_in_k = all(c in kernel for c in center)
        
        conclusion = k_in_c and c_in_k
        neg_q_ok = not conclusion
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G acts on itself by conjugation",
    "¬Q: The kernel of the conjugation action is not exactly the center Z(G) of the group"
]

N_HYP = 1
NEG_Q_INDEX = 1