import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, P, phi, p = witness
        elif len(witness) == 3:
            G, P, phi = witness
            try:
                order_P = P.order()
                factors = sympy.ntheory.factorint(order_P)
                if len(factors) == 1:
                    p = list(factors.keys())[0]
                else:
                    p = 2
            except Exception:
                p = 2
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        h2_ok = False
        if isinstance(P, PermutationGroup) and all(g in G for g in P.generators):
            if sympy.isprime(p):
                order_G = G.order()
                order_P = P.order()
                factors = sympy.ntheory.factorint(order_G)
                max_power = p ** factors.get(p, 0)
                if order_P == max_power:
                    h2_ok = True
    except Exception:
        h2_ok = False

    # H_3: \phi is an automorphism of G
    try:
        h3_ok = False
        elements = list(G.elements)
        
        if isinstance(phi, dict):
            mapping = phi
        else:
            mapping = {g: phi(g) for g in elements}
            
        if set(mapping.keys()) == set(elements) and set(mapping.values()) == set(elements):
            is_hom = True
            for x in elements:
                for y in elements:
                    if mapping[x * y] != mapping[x] * mapping[y]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            h3_ok = is_hom
    except Exception:
        h3_ok = False

    # ¬Q: The image \phi(P) is NOT a Sylow p-subgroup of G
    try:
        neg_q_ok = False
        if isinstance(phi, dict):
            mapping = phi
        else:
            mapping = {g: phi(g) for g in list(G.elements)}
            
        P_elements = list(P.elements)
        phi_P_elements = [mapping[g] for g in P_elements]
        phi_P_set = set(phi_P_elements)
        
        is_subgroup_phi_P = True
        for x in phi_P_elements:
            for y in phi_P_elements:
                if (x * y) not in phi_P_set:
                    is_subgroup_phi_P = False
                    break
            if not is_subgroup_phi_P:
                break
                
        is_sylow = False
        if is_subgroup_phi_P:
            order_G = G.order()
            order_phi_P = len(phi_P_elements)
            factors = sympy.ntheory.factorint(order_G)
            max_power = p ** factors.get(p, 0)
            if order_phi_P == max_power:
                is_sylow = True
                
        neg_q_ok = not is_sylow
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: \phi is an automorphism of G",
    "¬Q: The image \phi(P) is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3