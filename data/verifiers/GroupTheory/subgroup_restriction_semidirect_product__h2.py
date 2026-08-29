import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
    """
    Given a witness (N, H, phi, K), checks if it satisfies the remaining hypotheses
    and if the conclusion fails.
    """
    try:
        N, H, phi, K = witness
        if isinstance(K, PermutationGroup):
            K_elems = list(K.elements)
        else:
            K_elems = list(K)
        N_elems = list(N.elements)
        H_elems = list(H.elements)
    except Exception:
        return [False, False, False, False]
        
    def apply_map(m, x):
        if isinstance(m, dict):
            return m[x]
        return m(x)

    # H_1: N and H are PermutationGroups
    try:
        h1_ok = isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: phi is a homomorphism from H to Aut(N)
    try:
        h2_ok = True
        for h in H_elems:
            seen = set()
            phi_h = apply_map(phi, h)
            for n in N_elems:
                pn = apply_map(phi_h, n)
                if pn not in N_elems:
                    h2_ok = False
                    break
                seen.add(pn)
            if not h2_ok: 
                break
            if len(seen) != len(N_elems):
                h2_ok = False
                break
                
            for n1 in N_elems:
                for n2 in N_elems:
                    if apply_map(phi_h, n1 * n2) != apply_map(phi_h, n1) * apply_map(phi_h, n2):
                        h2_ok = False
                        break
                if not h2_ok: 
                    break
            if not h2_ok: 
                break
            
        if h2_ok:
            for h1 in H_elems:
                for h2 in H_elems:
                    phi_h1h2 = apply_map(phi, h1 * h2)
                    phi_h1 = apply_map(phi, h1)
                    phi_h2 = apply_map(phi, h2)
                    for n in N_elems:
                        if apply_map(phi_h1h2, n) != apply_map(phi_h1, apply_map(phi_h2, n)):
                            h2_ok = False
                            break
                    if not h2_ok: 
                        break
                if not h2_ok: 
                    break
    except Exception:
        h2_ok = False
        
    # H_3: K is a subset of H
    try:
        h3_ok = True
        for k in K_elems:
            if k not in H_elems:
                h3_ok = False
                break
    except Exception:
        h3_ok = False
        
    # neg_Q: N x K is NOT a subgroup of G (which happens iff K is not a subgroup of H)
    try:
        id_H = next(h for h in H_elems if h * h == h)
        
        is_subgroup = True
        if id_H not in K_elems:
            is_subgroup = False
        else:
            for k1 in K_elems:
                for k2 in K_elems:
                    if (k1 * k2) not in K_elems:
                        is_subgroup = False
                        break
                if not is_subgroup: 
                    break
            
            if is_subgroup:
                for k in K_elems:
                    if (k**-1) not in K_elems:
                        is_subgroup = False
                        break
                        
        neg_q = not is_subgroup
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are valid groups",
    "H_2: phi is a valid homomorphism from H to Aut(N)",
    "H_3: K is a subset of H",
    "¬Q: N x K is not a subgroup of G or not isomorphic to N rtimes K"
]

N_HYP = 3
NEG_Q_INDEX = 3