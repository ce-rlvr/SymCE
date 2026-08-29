import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard group bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard matrix bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture.
    Witness is expected to be a tuple: (N, H, phi)
    where N and H are groups (e.g., SymPy PermutationGroups)
    and phi is a homomorphism from H to Aut(N), represented as a dict or callable.
    """
    try:
        N, H, phi = witness
    except Exception:
        return [False, False, False]
        
    # H_1: N and H are groups
    def is_group(G):
        try:
            if isinstance(G, PermutationGroup):
                return True
            elements = list(G.generate()) if hasattr(G, 'generate') else list(G)
            if not elements: 
                return False
            # check closure
            for a in elements:
                for b in elements:
                    if a * b not in elements:
                        return False
            # check identity
            id_elem = None
            for e in elements:
                if all(e * a == a and a * e == a for a in elements):
                    id_elem = e
                    break
            if id_elem is None: 
                return False
            # check inverses
            for a in elements:
                has_inv = False
                for b in elements:
                    if a * b == id_elem and b * a == id_elem:
                        has_inv = True
                        break
                if not has_inv: 
                    return False
            return True
        except Exception:
            return False

    try:
        h1 = is_group(N) and is_group(H)
    except Exception:
        h1 = False

    # H_2: phi is a group homomorphism from H to Aut(N)
    try:
        elements_N = list(N.generate()) if hasattr(N, 'generate') else list(N)
        elements_H = list(H.generate()) if hasattr(H, 'generate') else list(H)
        
        def apply_phi(h, n):
            if isinstance(phi, dict):
                mapping = phi[h]
            else:
                mapping = phi(h)
            
            if isinstance(mapping, dict):
                return mapping[n]
            else:
                return mapping(n)
                
        h2 = True
        for h in elements_H:
            mapped_N = []
            for n in elements_N:
                mapped_n = apply_phi(h, n)
                if mapped_n not in elements_N:
                    h2 = False
                    break
                mapped_N.append(mapped_n)
            if not h2: break
            
            # Check bijection
            for n in elements_N:
                if n not in mapped_N:
                    h2 = False
                    break
            if not h2: break
                
            # Check homomorphism of phi(h)
            for n1 in elements_N:
                for n2 in elements_N:
                    if apply_phi(h, n1 * n2) != apply_phi(h, n1) * apply_phi(h, n2):
                        h2 = False
                        break
                if not h2: break
            if not h2: break
            
        if h2:
            # Check phi is a homomorphism from H to Aut(N)
            for h1_el in elements_H:
                for h2_el in elements_H:
                    h12 = h1_el * h2_el
                    for n in elements_N:
                        if apply_phi(h12, n) != apply_phi(h1_el, apply_phi(h2_el, n)):
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails.
    # In the direct product N x H (the default ambient group when not specified as a semidirect product),
    # the centralizer of N x {1_H} in {1_N} x H is the entire {1_N} x H.
    # The conclusion claims this centralizer is equal to {1_N} x ker(phi).
    # This fails if and only if ker(phi) != H.
    try:
        elements_N = list(N.generate()) if hasattr(N, 'generate') else list(N)
        elements_H = list(H.generate()) if hasattr(H, 'generate') else list(H)
        
        def apply_phi(h, n):
            if isinstance(phi, dict):
                mapping = phi[h]
            else:
                mapping = phi(h)
            
            if isinstance(mapping, dict):
                return mapping[n]
            else:
                return mapping(n)
                
        ker = []
        for h in elements_H:
            is_id = True
            for n in elements_N:
                if apply_phi(h, n) != n:
                    is_id = False
                    break
            if is_id:
                ker.append(h)
        
        neg_q = len(ker) != len(elements_H)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi is a group homomorphism from H to Aut(N)",
    "¬Q: The centralizer of N x {1_H} in {1_N} x H is not equal to {1_N} x ker(phi)"
]

N_HYP = 2
NEG_Q_INDEX = 2