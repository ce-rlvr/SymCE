import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def _eval_map(m, x):
    if callable(m):
        return m(x)
    return m[x]

def conditions(witness) -> list[bool]:
    try:
        G = witness['G']
        H = witness['H']
        K = witness['K']
        phi = witness['phi']
        psi = witness['psi']
    except Exception:
        return [False, False]

    # H_1: phi: G -> H is a surjective group homomorphism
    try:
        G_elements = list(G.elements)
        H_elements = list(H.elements)
        
        valid_map = True
        phi_values = set()
        for g in G_elements:
            try:
                val = _eval_map(phi, g)
                if val not in H_elements:
                    valid_map = False
                    break
                phi_values.add(val)
            except Exception:
                valid_map = False
                break
                
        if valid_map:
            surjective = (phi_values == set(H_elements))
            homo = True
            for g1 in G_elements:
                for g2 in G_elements:
                    if _eval_map(phi, g1 * g2) != _eval_map(phi, g1) * _eval_map(phi, g2):
                        homo = False
                        break
                if not homo:
                    break
            h1_ok = surjective and homo
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # neg_Q: psi o phi: G -> K is NOT a surjective group homomorphism
    try:
        K_elements = list(K.elements)
        
        valid_comp = True
        comp_values = set()
        for g in G_elements:
            try:
                val_phi = _eval_map(phi, g)
                val_comp = _eval_map(psi, val_phi)
                if val_comp not in K_elements:
                    valid_comp = False
                    break
                comp_values.add(val_comp)
            except Exception:
                valid_comp = False
                break
                
        if valid_comp:
            comp_surjective = (comp_values == set(K_elements))
            comp_homo = True
            for g1 in G_elements:
                for g2 in G_elements:
                    val1 = _eval_map(psi, _eval_map(phi, g1))
                    val2 = _eval_map(psi, _eval_map(phi, g2))
                    val12 = _eval_map(psi, _eval_map(phi, g1 * g2))
                    if val12 != val1 * val2:
                        comp_homo = False
                        break
                if not comp_homo:
                    break
            q_ok = comp_surjective and comp_homo
        else:
            q_ok = False
            
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: phi: G -> H is a surjective group homomorphism",
    "¬Q: psi o phi: G -> K is not a surjective group homomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1