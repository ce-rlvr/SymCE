import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
V4 = AlternatingGroup(4)
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that if phi: H -> Aut(N) is trivial, then N rtimes H is isomorphic to N x H.
    This is a tautology for external semidirect products, so the false conjecture must refer to 
    the internal semidirect product NH where the hypothesis N intersect H = {1} was dropped.
    """
    try:
        # The witness could be (N, H), (G, N, H), or (N, H, phi)
        if len(witness) == 2:
            N, H = witness
            phi = None
        elif len(witness) == 3:
            if isinstance(witness[2], dict) or callable(witness[2]):
                N, H, phi = witness
            else:
                G, N, H = witness
                phi = None
        else:
            return [False, False, False]
            
        N_elems = list(N.elements) if hasattr(N, 'elements') else list(N)
        H_elems = list(H.elements) if hasattr(H, 'elements') else list(H)
        
        def contains(lst, item):
            for x in lst:
                if x == item:
                    return True
            return False

        if phi is None:
            # Internal semidirect product case (phi is implicitly conjugation)
            
            # H1: phi is a group homomorphism H -> Aut(N)
            # This requires H to normalize N
            h1_ok = True
            for h in H_elems:
                try:
                    h_inv = h**-1
                except Exception:
                    h1_ok = False
                    break
                for n in N_elems:
                    if not contains(N_elems, h * n * h_inv):
                        h1_ok = False
                        break
                if not h1_ok: break
                
            # H2: phi(h) is the identity automorphism of N for all h in H
            # This requires H to centralize N
            h2_ok = True
            for h in H_elems:
                try:
                    h_inv = h**-1
                except Exception:
                    h2_ok = False
                    break
                for n in N_elems:
                    if (h * n * h_inv) != n:
                        h2_ok = False
                        break
                if not h2_ok: break
                
            # neg_Q: The "semidirect product" NH is NOT isomorphic to N x H
            # For finite groups, if H centralizes N, NH is isomorphic to N x H iff |NH| == |N||H|
            NH_elems = []
            for n in N_elems:
                for h in H_elems:
                    nh = n * h
                    if not contains(NH_elems, nh):
                        NH_elems.append(nh)
                        
            size_NH = len(NH_elems)
            size_NxH = len(N_elems) * len(H_elems)
            
            neg_q = (size_NH != size_NxH)
            
            return [h1_ok, h2_ok, neg_q]
            
        else:
            # External semidirect product case
            def apply_phi(h, n):
                if isinstance(phi, dict):
                    mapping = phi[h]
                else:
                    mapping = phi(h)
                
                if isinstance(mapping, dict):
                    return mapping[n]
                else:
                    return mapping(n)
                    
            # H1: phi is a group homomorphism H -> Aut(N)
            h1_ok = True
            for h in H_elems:
                img = []
                for n in N_elems:
                    try:
                        val = apply_phi(h, n)
                    except Exception:
                        h1_ok = False
                        break
                    if not contains(img, val):
                        img.append(val)
                if not h1_ok: break
                
                if len(img) != len(N_elems):
                    h1_ok = False
                    break
                    
                for n1 in N_elems:
                    for n2 in N_elems:
                        if apply_phi(h, n1 * n2) != apply_phi(h, n1) * apply_phi(h, n2):
                            h1_ok = False
                            break
                    if not h1_ok: break
                if not h1_ok: break
                
            if h1_ok:
                for h1 in H_elems:
                    for h2 in H_elems:
                        h1h2 = h1 * h2
                        for n in N_elems:
                            if apply_phi(h1h2, n) != apply_phi(h1, apply_phi(h2, n)):
                                h1_ok = False
                                break
                        if not h1_ok: break
                    if not h1_ok: break
                    
            # H2: phi(h) is the identity automorphism of N for all h in H
            h2_ok = True
            for h in H_elems:
                for n in N_elems:
                    if apply_phi(h, n) != n:
                        h2_ok = False
                        break
                if not h2_ok: break
                
            # neg_Q: N rtimes H is NOT isomorphic to N x H
            # For external semidirect product, if H2 holds, the operation is exactly the direct product.
            # Thus they are identical and always isomorphic.
            neg_q = False
            
            return [h1_ok, h2_ok, neg_q]
            
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from H to Aut(N)",
    "H_2: phi(h) is the identity automorphism of N for all h in H",
    "¬Q: The semidirect product N rtimes H is not isomorphic to the direct product N x H"
]

N_HYP = 2
NEG_Q_INDEX = 2