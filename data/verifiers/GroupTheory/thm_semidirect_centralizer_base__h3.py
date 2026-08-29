import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
import itertools

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

CONDITION_LABELS = [
    "H_1: G is the external semidirect product of N by H with respect to φ: H → Aut(N)",
    "H_2: Z(N) is the center of the group N",
    "¬Q: C_G(N) is not given by the set of elements (n, h) where n ∈ Z(N) and h ∈ ker(φ) or is not isomorphic to Z(N) × ker(φ)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_elements(G):
    if hasattr(G, 'generate'):
        return list(G.generate())
    elif hasattr(G, 'elements'):
        return list(G.elements)
    elif isinstance(G, (list, tuple, set)):
        return list(G)
    else:
        raise ValueError("Unknown group type")

def conditions(witness):
    try:
        N, H, phi = witness
        
        N_elems = get_elements(N)
        H_elems = get_elements(H)
        
        if not N_elems or not H_elems:
            return [False, False, False]
            
        def find_identity(elems):
            for e in elems:
                if all(e * x == x and x * e == x for x in elems):
                    return e
            return None
            
        id_N = find_identity(N_elems)
        id_H = find_identity(H_elems)
        
        if id_N is None or id_H is None:
            return [False, False, False]
            
        h1_ok = True
        
        # Check closure and inverses for N
        for x in N_elems:
            has_inv = False
            for y in N_elems:
                try:
                    xy = x * y
                    if xy not in N_elems:
                        h1_ok = False
                    if xy == id_N and y * x == id_N:
                        has_inv = True
                except Exception:
                    h1_ok = False
            if not has_inv:
                h1_ok = False
                
        # Check closure and inverses for H
        for x in H_elems:
            has_inv = False
            for y in H_elems:
                try:
                    xy = x * y
                    if xy not in H_elems:
                        h1_ok = False
                    if xy == id_H and y * x == id_H:
                        has_inv = True
                except Exception:
                    h1_ok = False
            if not has_inv:
                h1_ok = False
                
        def apply_phi(h, n):
            if callable(phi):
                return phi(h, n)
            return phi[h][n]
            
        if h1_ok:
            for h in H_elems:
                for n in N_elems:
                    try:
                        if apply_phi(h, n) not in N_elems:
                            h1_ok = False
                    except Exception:
                        h1_ok = False
                        
            for h in H_elems:
                for n1 in N_elems:
                    for n2 in N_elems:
                        try:
                            if apply_phi(h, n1 * n2) != apply_phi(h, n1) * apply_phi(h, n2):
                                h1_ok = False
                        except Exception:
                            h1_ok = False
                            
            for h1 in H_elems:
                for h2 in H_elems:
                    for n in N_elems:
                        try:
                            if apply_phi(h1 * h2, n) != apply_phi(h1, apply_phi(h2, n)):
                                h1_ok = False
                        except Exception:
                            h1_ok = False
                            
            for n in N_elems:
                try:
                    if apply_phi(id_H, n) != n:
                        h1_ok = False
                except Exception:
                    h1_ok = False

        # H2: Z(N) is the center of the group N
        # This is true by definition in our context.
        h2_ok = True
        
        Z_N = []
        for n in N_elems:
            if all(n * m == m * n for m in N_elems):
                Z_N.append(n)
                
        C_G_N = []
        for n in N_elems:
            for h in H_elems:
                is_in_C = True
                for m in N_elems:
                    try:
                        if n * apply_phi(h, m) != m * n:
                            is_in_C = False
                            break
                    except Exception:
                        is_in_C = False
                        break
                if is_in_C:
                    C_G_N.append((n, h))
                    
        ker_phi = []
        for h in H_elems:
            try:
                if all(apply_phi(h, m) == m for m in N_elems):
                    ker_phi.append(h)
            except Exception:
                pass
                
        S = []
        for n in Z_N:
            for h in ker_phi:
                S.append((n, h))
                
        neg_q = False
        if len(C_G_N) != len(S):
            neg_q = True
        else:
            for x in C_G_N:
                if x not in S:
                    neg_q = True
                    break
                    
        return [h1_ok, h2_ok, neg_q]
    except Exception:
        return [False, False, False]