import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    return list(G)

def is_conjugate_in(G, a, b):
    elements = get_elements(G)
    for x in elements:
        try:
            if x * a * x**-1 == b:
                return True
        except Exception:
            pass
        try:
            if x * a * ~x == b:
                return True
        except Exception:
            pass
    return False

def is_conjugate_in_GxH(G, H, g1, h1, g2, h2):
    elements_G = get_elements(G)
    elements_H = get_elements(H)
    for x in elements_G:
        for y in elements_H:
            try:
                cond_g = (x * g1 * x**-1 == g2) or (x * g1 * ~x == g2)
                cond_h = (y * h1 * y**-1 == h2) or (y * h1 * ~y == h2)
                if cond_g and cond_h:
                    return True
            except Exception:
                pass
    return False

def conditions(witness) -> list[bool]:
    try:
        G, H, g1, h1, g2, h2 = witness
    except Exception:
        return [False, False]

    # H_1: (g_1, h_1) and (g_2, h_2) are elements of the direct product G x H
    try:
        elements_G = get_elements(G)
        elements_H = get_elements(H)
        h1_ok = (g1 in elements_G) and (h1 in elements_H) and (g2 in elements_G) and (h2 in elements_H)
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion FAILS at the witness
    # Conclusion: (g_1, h_1) and (g_2, h_2) are conjugate in G x H iff g_1 ~ g_2 in G and h_1 ~ h_2 in H
    try:
        conj_GxH = is_conjugate_in_GxH(G, H, g1, h1, g2, h2)
        conj_G = is_conjugate_in(G, g1, g2)
        conj_H = is_conjugate_in(H, h1, h2)
        
        conclusion = (conj_GxH == (conj_G and conj_H))
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: (g_1, h_1) and (g_2, h_2) are elements of the direct product G x H",
    "¬Q: (g_1, h_1) and (g_2, h_2) are conjugate in G x H is NOT equivalent to g_1 conjugate to g_2 in G and h_1 conjugate to h_2 in H"
]

N_HYP = 1
NEG_Q_INDEX = 1