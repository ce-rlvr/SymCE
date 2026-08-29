import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def get_attr_or_key(obj, key):
    if isinstance(obj, dict):
        return obj[key]
    return getattr(obj, key)

def get_identity(G):
    elements = list(G.elements)
    for e in elements:
        if e * e == e:
            return e
    return elements[0]

def apply_map(m, x):
    if callable(m):
        return m(x)
    return m[x]

def apply_phi(phi, h, n):
    if callable(phi):
        return phi(h, n)
    return phi[h][n]

def conditions(witness) -> list[bool]:
    try:
        N = get_attr_or_key(witness, 'N')
        H = get_attr_or_key(witness, 'H')
        K = get_attr_or_key(witness, 'K')
        phi = get_attr_or_key(witness, 'phi')
        f = get_attr_or_key(witness, 'f')
        g = get_attr_or_key(witness, 'g')
    except Exception:
        return [False, False, False, False]

    # H1: N, H, K are groups
    try:
        H1_ok = hasattr(N, 'elements') and hasattr(H, 'elements') and hasattr(K, 'elements')
    except Exception:
        H1_ok = False

    # H2: phi is an action of H on N by automorphisms
    try:
        H2_ok = True
        N_elements = list(N.elements)
        H_elements = list(H.elements)
        for h in H_elements:
            for n1 in N_elements:
                for n2 in N_elements:
                    if apply_phi(phi, h, n1 * n2) != apply_phi(phi, h, n1) * apply_phi(phi, h, n2):
                        H2_ok = False
        for h1 in H_elements:
            for h2 in H_elements:
                for n in N_elements:
                    if apply_phi(phi, h1 * h2, n) != apply_phi(phi, h1, apply_phi(phi, h2, n)):
                        H2_ok = False
        id_H = get_identity(H)
        for n in N_elements:
            if apply_phi(phi, id_H, n) != n:
                H2_ok = False
    except Exception:
        H2_ok = False

    # H3: f maps N to K, g maps H to K
    try:
        H3_ok = True
        K_elements = list(K.elements)
        N_elements = list(N.elements)
        H_elements = list(H.elements)
        for n in N_elements:
            if apply_map(f, n) not in K_elements:
                H3_ok = False
        for h in H_elements:
            if apply_map(g, h) not in K_elements:
                H3_ok = False
    except Exception:
        H3_ok = False

    # Conclusion: P <==> Q
    try:
        P = True
        N_elements = list(N.elements)
        H_elements = list(H.elements)
        id_N = get_identity(N)
        id_H = get_identity(H)
        id_K = get_identity(K)
        
        if apply_map(f, id_N) != id_K:
            P = False
        if apply_map(g, id_H) != id_K:
            P = False
            
        if P:
            for n1 in N_elements:
                for n2 in N_elements:
                    for h1 in H_elements:
                        for h2 in H_elements:
                            left = apply_map(f, n1 * apply_phi(phi, h1, n2)) * apply_map(g, h1 * h2)
                            right = apply_map(f, n1) * apply_map(g, h1) * apply_map(f, n2) * apply_map(g, h2)
                            if left != right:
                                P = False
                                break
                        if not P: break
                    if not P: break
                if not P: break

        Q = True
        for n in N_elements:
            for h in H_elements:
                if apply_map(f, apply_phi(phi, h, n)) != apply_map(g, h) * apply_map(f, n) * apply_map(g, h)**(-1):
                    Q = False
                    break
            if not Q: break

        neg_Q_ok = (P != Q)
    except Exception:
        neg_Q_ok = False

    return [H1_ok, H2_ok, H3_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: N, H, K are groups",
    "H_2: phi is an action of H on N by automorphisms",
    "H_3: f maps N to K and g maps H to K",
    "¬Q: The equivalence P <==> Q fails"
]

N_HYP = 3
NEG_Q_INDEX = 3