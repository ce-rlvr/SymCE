import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            g = witness.get('g')
        else:
            G, H, g = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # neg_Q: The conjugate subgroup gHg^{-1} is NOT isomorphic to H
    try:
        is_iso = False
        
        if isinstance(g, Permutation):
            # g is a single element
            try:
                g_inv = ~g
            except Exception:
                g_inv = g**-1
            
            conj_elements = [g * h * g_inv for h in H.elements]
            conj_group = PermutationGroup(conj_elements)
            
            # Verify that the set of conjugates is closed (forms the group exactly)
            if len(set(conj_elements)) == conj_group.order():
                is_iso = conj_group.is_isomorphic(H)
                
        elif hasattr(g, 'elements') or isinstance(g, (list, set, tuple)):
            # g is a subgroup or a collection of elements
            if hasattr(g, 'elements'):
                g_elems = g.elements
            else:
                g_elems = list(g)
                
            conj_elements = set()
            for k in g_elems:
                try:
                    k_inv = ~k
                except Exception:
                    k_inv = k**-1
                for h in H.elements:
                    conj_elements.add(k * h * k_inv)
                    
            conj_group = PermutationGroup(list(conj_elements))
            
            # If the set of conjugates does not form a group, its size will be 
            # strictly less than the order of the group it generates.
            if len(conj_elements) == conj_group.order():
                is_iso = conj_group.is_isomorphic(H)
        else:
            # g is an invalid type, gHg^{-1} is undefined
            is_iso = False
            
        neg_q = not is_iso
    except Exception:
        # If any error occurs (e.g., g cannot be inverted, multiplication fails),
        # then gHg^{-1} is undefined or not a group, so it's not isomorphic to H.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: The conjugate subgroup gHg^{-1} is not isomorphic to H"
]

N_HYP = 2
NEG_Q_INDEX = 2