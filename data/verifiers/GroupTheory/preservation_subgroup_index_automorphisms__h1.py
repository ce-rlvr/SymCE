import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_index(G, H):
    try:
        if hasattr(G, 'order') and hasattr(H, 'order'):
            g_ord = G.order()
            h_ord = H.order()
            if g_ord != sympy.oo and h_ord != sympy.oo and h_ord > 0:
                if g_ord % h_ord == 0:
                    return g_ord // h_ord
    except Exception:
        pass
    return None

def conditions(witness):
    try:
        G, H, alpha = witness
    except Exception:
        return [False, False, False, False]
        
    def apply_alpha(x):
        if isinstance(alpha, dict):
            return alpha[x]
        return alpha(x)

    try:
        h1 = all(g in G for g in H.generators)
    except Exception:
        h1 = False

    n = None
    try:
        if h1:
            n = get_index(G, H)
            h2 = (n is not None and n > 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        h3 = False
        if hasattr(alpha, 'is_isomorphism'):
            try:
                if alpha.domain == G and alpha.codomain == G:
                    h3 = alpha.is_isomorphism()
            except Exception:
                h3 = alpha.is_isomorphism()
        
        if not h3:
            g_ord = None
            try:
                g_ord = G.order()
            except Exception:
                pass
                
            if g_ord is not None and g_ord != sympy.oo:
                G_elements = list(G.elements)
                mapped_elements = [apply_alpha(x) for x in G_elements]
                
                is_bijection = len(set(mapped_elements)) == len(G_elements) and all(y in G for y in mapped_elements)
                
                if is_bijection:
                    is_hom = True
                    for g in G.generators:
                        for y in G_elements:
                            if apply_alpha(g * y) != apply_alpha(g) * apply_alpha(y):
                                is_hom = False
                                break
                        if not is_hom:
                            break
                    h3 = is_hom
    except Exception:
        h3 = False

    try:
        neg_q = False
        if n is not None:
            alpha_H_gens = [apply_alpha(g) for g in H.generators]
            if not alpha_H_gens:
                try:
                    id_el = G.identity
                except Exception:
                    try:
                        id_el = list(G.elements)[0]**0
                    except Exception:
                        id_el = None
                if id_el is not None:
                    alpha_H_gens = [id_el]
                
            alpha_H = PermutationGroup(alpha_H_gens)
            index_alpha_H = get_index(G, alpha_H)
            if index_alpha_H is not None:
                neg_q = (index_alpha_H != n)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The index of H in G is a finite integer n",
    "H_3: alpha is an automorphism of G",
    "not Q: The index of the image subgroup alpha(H) in G is not equal to n"
]

N_HYP = 3
NEG_Q_INDEX = 3