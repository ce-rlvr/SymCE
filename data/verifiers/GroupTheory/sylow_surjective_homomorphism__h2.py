import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            P = witness.get('P')
            p = witness.get('p')
            phi = witness.get('phi')
        else:
            G, H, P, p, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are finite groups
    try:
        h1 = (hasattr(G, 'order') and hasattr(H, 'order') and 
              G.order() < float('inf') and H.order() < float('inf'))
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        h2 = False
        if isprime(p) and hasattr(P, 'order'):
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp = order_G
            while temp % p == 0:
                k += 1
                temp //= p
            if order_P == p**k:
                # check if P is a subgroup of G
                is_sub = True
                for g in P.generators:
                    if g not in G:
                        is_sub = False
                        break
                h2 = is_sub
    except Exception:
        h2 = False

    # ¬Q: phi(P) is not a Sylow p-subgroup of H
    try:
        neg_q = False
        elements_P = list(P.generate())
        if isinstance(phi, dict):
            mapped = [phi[g] for g in elements_P]
        else:
            mapped = [phi(g) for g in elements_P]
        
        mapped_set = set(mapped)
        
        # Check if mapped_set is a subgroup of H
        all_in_H = True
        for m in mapped_set:
            if m not in H:
                all_in_H = False
                break
        
        if not all_in_H:
            neg_q = True
        else:
            # Check closure under group operation
            is_subgroup = True
            for a in mapped_set:
                for b in mapped_set:
                    if a * b not in mapped_set:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            
            if not is_subgroup:
                neg_q = True
            else:
                # It is a subgroup. Check if it is a Sylow p-subgroup of H.
                order_H = H.order()
                order_phi_P = len(mapped_set)
                m = 0
                temp = order_H
                while temp % p == 0:
                    m += 1
                    temp //= p
                if order_phi_P != p**m:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: phi(P) is not a Sylow p-subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2