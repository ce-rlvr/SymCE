import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False

    # H3: P is a subgroup of G (so N_G(P) is well-defined)
    try:
        if isinstance(P, PermutationGroup) and isinstance(G, PermutationGroup):
            try:
                h3 = P.is_subgroup(G)
            except Exception:
                G_elements = set(G.generate())
                h3 = all(gen in G_elements for gen in P.generators)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: N_G(N_G(P)) != N_G(P)
    try:
        if not (h1 and h3):
            neg_q = False
        else:
            P_elements = set(P.generate())
            P_gens = P.generators
            
            norm_P_elements = []
            for g in G.generate():
                if all(g * p_gen * ~g in P_elements for p_gen in P_gens):
                    norm_P_elements.append(g)
            
            N_P = PermutationGroup(norm_P_elements)
            N_P_elements = set(norm_P_elements)
            N_P_gens = N_P.generators
            
            norm_N_P_elements = []
            for g in G.generate():
                if all(g * n_gen * ~g in N_P_elements for n_gen in N_P_gens):
                    norm_N_P_elements.append(g)
            
            neg_q = len(norm_N_P_elements) != len(norm_P_elements)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: N_G(P) is the normalizer of P in G",
    "¬Q: The normalizer of N_G(P) in G is not equal to N_G(P)"
]

N_HYP = 3
NEG_Q_INDEX = 3