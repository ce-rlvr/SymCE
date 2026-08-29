import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard group theory bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def apply_map(m, x):
    if callable(m):
        return m(x)
    return m[x]

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the Universal Property of the Semidirect Product.
    Witness should be a tuple: (N, H, phi, K, f, g) or (N, H, phi, G, K, f, g)
    """
    try:
        if len(witness) == 7:
            N, H, phi, G, K, f, g = witness
        else:
            N, H, phi, K, f, g = witness[:6]
    except Exception:
        return [False] * 5 + [False]
    
    def get_elems(Grp):
        if hasattr(Grp, 'generate'): return list(Grp.generate())
        if hasattr(Grp, 'elements'): return list(Grp.elements)
        return list(Grp)
        
    try:
        N_elems = get_elems(N)
        H_elems = get_elems(H)
        K_elems = get_elems(K)
    except Exception:
        return [False] * 5 + [False]

    # H1: N and H are groups and phi: H -> Aut(N) is a homomorphism
    h1_ok = False
    try:
        if len(N_elems) > 0 and len(H_elems) > 0:
            h1_ok = True
            for h in H_elems:
                phi_h = apply_map(phi, h)
                mapped = [apply_map(phi_h, n) for n in N_elems]
                
                # Check bijection
                for n in N_elems:
                    if n not in mapped: h1_ok = False; break
                if not h1_ok: break
                for m in mapped:
                    if m not in N_elems: h1_ok = False; break
                if not h1_ok: break
                
                # Check homomorphism property of phi(h)
                for n1 in N_elems:
                    for n2 in N_elems:
                        if apply_map(phi_h, n1 * n2) != apply_map(phi_h, n1) * apply_map(phi_h, n2):
                            h1_ok = False; break
                    if not h1_ok: break
                if not h1_ok: break
            
            # Check homomorphism property of phi: H -> Aut(N)
            if h1_ok:
                for h1 in H_elems:
                    for h2 in H_elems:
                        phi_h1 = apply_map(phi, h1)
                        phi_h2 = apply_map(phi, h2)
                        phi_h1h2 = apply_map(phi, h1 * h2)
                        for n in N_elems:
                            if apply_map(phi_h1h2, n) != apply_map(phi_h1, apply_map(phi_h2, n)):
                                h1_ok = False; break
                        if not h1_ok: break
                    if not h1_ok: break
    except Exception:
        h1_ok = False

    # H2: G = N \rtimes_\phi H is the external semidirect product
    # This is definitional in our setup, so if H1 holds, G is well-defined.
    h2_ok = h1_ok

    # H3: K is a group
    h3_ok = False
    try:
        if len(K_elems) > 0:
            h3_ok = True
    except Exception:
        h3_ok = False

    # H4: f: N -> K and g: H -> K are group homomorphisms
    h4_ok = False
    try:
        h4_ok = True
        for n in N_elems:
            if apply_map(f, n) not in K_elems: h4_ok = False; break
        if h4_ok:
            for n1 in N_elems:
                for n2 in N_elems:
                    if apply_map(f, n1 * n2) != apply_map(f, n1) * apply_map(f, n2):
                        h4_ok = False; break
                if not h4_ok: break
        if h4_ok:
            for h in H_elems:
                if apply_map(g, h) not in K_elems: h4_ok = False; break
        if h4_ok:
            for h1 in H_elems:
                for h2 in H_elems:
                    if apply_map(g, h1 * h2) != apply_map(g, h1) * apply_map(g, h2):
                        h4_ok = False; break
                if not h4_ok: break
    except Exception:
        h4_ok = False

    # H5: f(N) is normalized by g(H) in K
    h5_ok = False
    try:
        f_N = [apply_map(f, n) for n in N_elems]
        h5_ok = True
        for h in H_elems:
            gh = apply_map(g, h)
            gh_inv = gh**(-1)
            for fn in f_N:
                if gh * fn * gh_inv not in f_N:
                    h5_ok = False; break
            if not h5_ok: break
    except Exception:
        h5_ok = False

    # neg_Q: There does not exist a unique group homomorphism Phi: G -> K extending f and g
    # Any such homomorphism must be given by Phi(n, h) = f(n)g(h).
    # We check if this map is indeed a homomorphism. If it fails, no such homomorphism exists.
    neg_q = False
    try:
        is_hom = True
        for n1 in N_elems:
            for h1 in H_elems:
                phi_h1 = apply_map(phi, h1)
                for n2 in N_elems:
                    n_prod = n1 * apply_map(phi_h1, n2)
                    f_n_prod = apply_map(f, n_prod)
                    f_n1 = apply_map(f, n1)
                    g_h1 = apply_map(g, h1)
                    f_n2 = apply_map(f, n2)
                    for h2 in H_elems:
                        h_prod = h1 * h2
                        g_h_prod = apply_map(g, h_prod)
                        
                        phi_prod = f_n_prod * g_h_prod
                        
                        g_h2 = apply_map(g, h2)
                        prod_phi = f_n1 * g_h1 * f_n2 * g_h2
                        
                        if phi_prod != prod_phi:
                            is_hom = False
                            break
                    if not is_hom: break
                if not is_hom: break
            if not is_hom: break
        neg_q = not is_hom
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, h5_ok, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups and phi: H -> Aut(N) is a homomorphism",
    "H_2: G = N \\rtimes_\\phi H is the external semidirect product",
    "H_3: K is a group",
    "H_4: f: N -> K and g: H -> K are group homomorphisms",
    "H_5: f(N) is normalized by g(H) in K",
    "¬Q: There does not exist a unique group homomorphism Phi: G -> K extending f and g"
]

N_HYP = 5
NEG_Q_INDEX = 5