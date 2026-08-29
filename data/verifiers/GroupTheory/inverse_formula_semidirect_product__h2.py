import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def apply_phi(phi, h, n):
    if callable(phi):
        return phi(h, n)
    else:
        return phi[h][n]

def conditions(witness):
    try:
        N, H, phi, n, h = witness
    except Exception:
        return [False, False, False, False]

    # H1: N and H are groups
    try:
        N_elements = list(N.elements) if hasattr(N, 'elements') else list(N)
        H_elements = list(H.elements) if hasattr(H, 'elements') else list(H)
        e_N = N.identity if hasattr(N, 'identity') else N_elements[0]**-1 * N_elements[0]
        e_H = H.identity if hasattr(H, 'identity') else H_elements[0]**-1 * H_elements[0]
        h1 = True
    except Exception:
        h1 = False

    # H2: G = N \rtimes_\phi H is the external semidirect product of N and H
    try:
        h2 = True
        for x in H_elements:
            for y in N_elements:
                res = apply_phi(phi, x, y)
                if res not in N_elements:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # H3: (n, h) is an element of G
    try:
        h3 = (n in N_elements) and (h in H_elements)
    except Exception:
        h3 = False

    # neg_Q: The inverse of (n, h) in G is not (\phi_{h^{-1}}(n^{-1}), h^{-1})
    try:
        h_inv = h**-1
        n_inv = n**-1
        
        prop_inv_n = apply_phi(phi, h_inv, n_inv)
        prop_inv_h = h_inv
        
        # Right inverse check: (n, h) * (prop_inv_n, prop_inv_h)
        right_n = n * apply_phi(phi, h, prop_inv_n)
        right_h = h * prop_inv_h
        
        # Left inverse check: (prop_inv_n, prop_inv_h) * (n, h)
        left_n = prop_inv_n * apply_phi(phi, prop_inv_h, n)
        left_h = prop_inv_h * h
        
        is_right_inv = (right_n == e_N) and (right_h == e_H)
        is_left_inv = (left_n == e_N) and (left_h == e_H)
        
        is_inverse = is_right_inv and is_left_inv
        neg_q = not is_inverse
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    r"H_1: N and H are groups",
    r"H_2: G = N \rtimes_\phi H is the external semidirect product of N and H",
    r"H_3: (n, h) is an element of G",
    r"¬Q: The inverse of (n, h) in G is not (\phi_{h^{-1}}(n^{-1}), h^{-1})"
]

N_HYP = 3
NEG_Q_INDEX = 3