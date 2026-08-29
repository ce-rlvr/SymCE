import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(3), Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    try:
        if hasattr(G, 'elements'):
            return list(G.elements)
    except Exception:
        pass
    try:
        return list(G.generate())
    except Exception:
        pass
    return list(G)

def get_identity(G):
    elements = get_elements(G)
    for e in elements:
        is_id = True
        for x in elements:
            if e * x != x or x * e != x:
                is_id = False
                break
        if is_id:
            return e
    return None

def conditions(witness):
    try:
        if len(witness) == 3:
            N, H, phi = witness
        elif len(witness) == 4:
            _, N, H, phi = witness
        else:
            return [False, False, False]
            
        N_els = get_elements(N)
        H_els = get_elements(H)
        id_N = get_identity(N)
        id_H = get_identity(H)
        
        if id_N is None or id_H is None:
            return [False, False, False]
            
        def apply_phi(h, n):
            if isinstance(phi, dict):
                ph = phi.get(h)
            else:
                ph = phi(h)
            if isinstance(ph, dict):
                return ph.get(n)
            else:
                return ph(n)

        # H1: phi is a group homomorphism from H to Aut(N)
        h1_ok = True
        for h in H_els:
            mapped = []
            for n in N_els:
                try:
                    pn = apply_phi(h, n)
                    if pn is None or pn not in N_els:
                        h1_ok = False
                        break
                    mapped.append(pn)
                except Exception:
                    h1_ok = False
                    break
            if not h1_ok:
                break
            
            # Check bijection
            if len(set(mapped)) != len(N_els):
                h1_ok = False
                break
                
            # Check homomorphism of phi(h)
            for n1 in N_els:
                for n2 in N_els:
                    if apply_phi(h, n1 * n2) != apply_phi(h, n1) * apply_phi(h, n2):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
            if not h1_ok:
                break
                
        if h1_ok:
            # Check if phi is a group homomorphism
            for h1 in H_els:
                for h2 in H_els:
                    h12 = h1 * h2
                    for n in N_els:
                        if apply_phi(h12, n) != apply_phi(h1, apply_phi(h2, n)):
                            h1_ok = False
                            break
                    if not h1_ok:
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H2: G = N \rtimes_\phi H is the external semidirect product
    # This is definitional setup; if H1 holds, the semidirect product is well-defined.
    h2_ok = h1_ok

    # Conclusion: The centralizer of N x {1_H} in the subgroup {1_N} x H is equal to {1_N} x ker(phi)
    try:
        if not h1_ok:
            neg_q = False
        else:
            centralizer = []
            for h in H_els:
                is_in_centralizer = True
                for n in N_els:
                    # Multiplication in semidirect product: (n1, h1) * (n2, h2) = (n1 * phi(h1)(n2), h1 * h2)
                    # Left: (id_N, h) * (n, id_H)
                    left_n = id_N * apply_phi(h, n)
                    left_h = h * id_H
                    
                    # Right: (n, id_H) * (id_N, h)
                    right_n = n * apply_phi(id_H, id_N)
                    right_h = id_H * h
                    
                    if left_n != right_n or left_h != right_h:
                        is_in_centralizer = False
                        break
                if is_in_centralizer:
                    centralizer.append(h)
                    
            ker_phi = []
            for h in H_els:
                is_in_ker = True
                for n in N_els:
                    if apply_phi(h, n) != n:
                        is_in_ker = False
                        break
                if is_in_ker:
                    ker_phi.append(h)
                    
            def is_subset(list1, list2):
                for x in list1:
                    if x not in list2:
                        return False
                return True
                
            are_equal = is_subset(centralizer, ker_phi) and is_subset(ker_phi, centralizer)
            neg_q = not are_equal
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from H to Aut(N)",
    "H_2: G is the external semidirect product of N and H",
    "¬Q: The centralizer of N x {1_H} in {1_N} x H is NOT equal to {1_N} x ker(phi)"
]

N_HYP = 2
NEG_Q_INDEX = 2