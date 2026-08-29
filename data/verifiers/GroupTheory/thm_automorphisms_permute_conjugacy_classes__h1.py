import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
    try:
        G, phi, C = witness
    except Exception:
        return [False, False, False]
    
    def get_elements(group):
        if hasattr(group, 'generate'):
            return list(group.generate())
        elif hasattr(group, 'elements'):
            return list(group.elements)
        else:
            return list(group)

    try:
        elements = get_elements(G)
        try:
            elements_set = set(elements)
            def check_subset(sub, superset):
                return set(sub).issubset(superset)
            def are_sets_equal(set1, set2):
                return set(set1) == set(set2)
            def make_unique(seq):
                return set(seq)
        except TypeError:
            # Fallback for unhashable elements (e.g., mutable matrices)
            elements_set = elements
            def check_subset(sub, superset):
                return all(x in superset for x in sub)
            def are_sets_equal(set1, set2):
                return all(x in set2 for x in set1) and all(x in set1 for x in set2)
            def make_unique(seq):
                res = []
                for x in seq:
                    if x not in res:
                        res.append(x)
                return res
    except Exception:
        return [False, False, False]

    def apply_phi(x):
        if isinstance(phi, dict):
            return phi[x]
        else:
            return phi(x)

    # H_1: \phi is an automorphism of G
    try:
        mapped_elements = []
        h1 = True
        for g in elements:
            mg = apply_phi(g)
            if mg not in elements_set:
                h1 = False
                break
            mapped_elements.append(mg)
            
        if h1:
            if len(make_unique(mapped_elements)) != len(elements):
                h1 = False
            else:
                for g1 in elements:
                    for g2 in elements:
                        if apply_phi(g1 * g2) != apply_phi(g1) * apply_phi(g2):
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H_2: C is a conjugacy class of G
    try:
        C_unique = make_unique(C)
        if not C_unique:
            h2 = False
        elif not check_subset(C_unique, elements_set):
            h2 = False
        else:
            x = next(iter(C_unique)) if isinstance(C_unique, set) else C_unique[0]
            conj_class = []
            for g in elements:
                try:
                    inv_g = ~g
                except Exception:
                    inv_g = g**-1
                conj_class.append(g * x * inv_g)
            h2 = are_sets_equal(C_unique, conj_class)
    except Exception:
        h2 = False

    # ¬Q: The image \phi(C) is NOT a conjugacy class of G
    try:
        phi_C = [apply_phi(x) for x in C]
        phi_C_unique = make_unique(phi_C)
        if not phi_C_unique:
            is_conj = False
        elif not check_subset(phi_C_unique, elements_set):
            is_conj = False
        else:
            y = next(iter(phi_C_unique)) if isinstance(phi_C_unique, set) else phi_C_unique[0]
            conj_class_y = []
            for g in elements:
                try:
                    inv_g = ~g
                except Exception:
                    inv_g = g**-1
                conj_class_y.append(g * y * inv_g)
            is_conj = are_sets_equal(phi_C_unique, conj_class_y)
            
        neg_q = not is_conj
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    r"H_1: \phi is an automorphism of G",
    r"H_2: C is a conjugacy class of G",
    r"¬Q: The image \phi(C) is not a conjugacy class of G"
]

N_HYP = 2
NEG_Q_INDEX = 2