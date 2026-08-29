import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math
import z3

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

def conditions(witness):
    try:
        H_grp, N_grp, N_prime, phi = witness
    except Exception:
        return [False, False]

    # H_1: N' is the commutator subgroup of N
    try:
        derived = N_grp.derived_subgroup()
        h1_ok = set(N_prime.elements) == set(derived.elements)
    except Exception:
        h1_ok = False

    # neg_Q: The induced map φ* is NOT a well-defined group action by automorphisms on N/N'
    try:
        H_elems = list(H_grp.elements)
        N_elems = list(N_grp.elements)
        N_prime_elems = set(N_prime.elements)
        
        def in_N_prime(x):
            return x in N_prime_elems
            
        def get_phi(h, n):
            if callable(phi):
                return phi(h, n)
            elif isinstance(phi, dict):
                val = phi[h]
                if callable(val):
                    return val(n)
                else:
                    return val[n]
            else:
                raise ValueError("phi must be callable or dict")

        is_well_defined = True
        is_homomorphism = True
        is_action = True
        is_identity = True
        is_bijection = True

        # Check if phi maps into N
        for h in H_elems:
            for n in N_elems:
                if get_phi(h, n) not in N_elems:
                    is_well_defined = False
                    break
            if not is_well_defined: break

        # Check well-definedness on cosets
        if is_well_defined:
            for h in H_elems:
                for n1 in N_elems:
                    for n2 in N_elems:
                        if in_N_prime(~n1 * n2):
                            if not in_N_prime(~get_phi(h, n1) * get_phi(h, n2)):
                                is_well_defined = False
                                break
                    if not is_well_defined: break
                if not is_well_defined: break

        # Check homomorphism property
        if is_well_defined:
            for h in H_elems:
                for n1 in N_elems:
                    for n2 in N_elems:
                        val1 = get_phi(h, n1 * n2)
                        val2 = get_phi(h, n1) * get_phi(h, n2)
                        if not in_N_prime(~val1 * val2):
                            is_homomorphism = False
                            break
                    if not is_homomorphism: break
                if not is_homomorphism: break

        # Check action property
        if is_well_defined:
            for h1 in H_elems:
                for h2 in H_elems:
                    for n in N_elems:
                        val1 = get_phi(h1 * h2, n)
                        val2 = get_phi(h1, get_phi(h2, n))
                        if not in_N_prime(~val1 * val2):
                            is_action = False
                            break
                    if not is_action: break
                if not is_action: break

        # Check identity property
        if is_well_defined:
            eH = H_grp.identity
            for n in N_elems:
                if not in_N_prime(~get_phi(eH, n) * n):
                    is_identity = False
                    break

        # Check bijection property
        if is_well_defined:
            for h in H_elems:
                images = set()
                for n in N_elems:
                    coset_image = frozenset([get_phi(h, n) * c for c in N_prime_elems])
                    images.add(coset_image)
                if len(images) * len(N_prime_elems) != len(N_elems):
                    is_bijection = False
                    break

        conclusion_holds = (is_well_defined and is_homomorphism and 
                            is_action and is_identity and is_bijection)
        neg_q_ok = not conclusion_holds

    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N' is the commutator subgroup of N",
    "¬Q: The induced map φ* is not a well-defined group action by automorphisms on N/N'"
]

N_HYP = 1
NEG_Q_INDEX = 1