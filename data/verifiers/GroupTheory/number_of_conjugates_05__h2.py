import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import math

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
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The normalizer N_G(H) has finite index in G
    try:
        if isinstance(H, PermutationGroup):
            H_set = set(H.generate())
        else:
            H_set = set(H)
            
        G_elements = list(G.generate())
        if not H_set.issubset(set(G_elements)):
            h2 = False
        else:
            norm_elements = []
            for g in G_elements:
                conj = set(g * h * ~g for h in H_set)
                if conj == H_set:
                    norm_elements.append(g)
            index = len(G_elements) // len(norm_elements)
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: The number of distinct conjugate subgroups of H in G is exactly the index
    try:
        if isinstance(H, PermutationGroup):
            H_set = set(H.generate())
        else:
            H_set = set(H)
            
        G_elements = list(G.generate())
        if not H_set.issubset(set(G_elements)):
            neg_q = False
        else:
            conjugates = set()
            norm_elements = []
            for g in G_elements:
                conj = frozenset(g * h * ~g for h in H_set)
                conjugates.add(conj)
                if conj == frozenset(H_set):
                    norm_elements.append(g)
                    
            index = len(G_elements) // len(norm_elements)
            
            def is_subgroup(subset):
                if not subset: 
                    return False
                id_el = next((e for e in G_elements if e * e == e), None)
                if id_el not in subset: 
                    return False
                for a in subset:
                    for b in subset:
                        if a * b not in subset:
                            return False
                return True

            num_conj_subgroups = sum(1 for conj in conjugates if is_subgroup(conj))
            
            q = (num_conj_subgroups == index)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The normalizer N_G(H) has finite index in G",
    "not Q: The number of distinct conjugate subgroups of H in G is not exactly the index of N_G(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2