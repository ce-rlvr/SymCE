import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        G_elements = list(G.generate())
        N_elements = list(N.generate())
        H_elements = list(H.generate())
    except Exception:
        return [False, False, False, False]

    # H_1: N is a normal subgroup of G
    try:
        N_set = set(N_elements)
        G_set = set(G_elements)
        h1 = N_set.issubset(G_set)
        if h1:
            for g in G_elements:
                for n in N_elements:
                    if (g * n * ~g) not in N_set:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        H_set = set(H_elements)
        h2 = H_set.issubset(G_set)
    except Exception:
        h2 = False

    # H_3: G is the internal semidirect product of N and H
    try:
        if h1 and h2:
            int_elements = N_set.intersection(H_set)
            # Internal semidirect product requires N intersect H to be trivial and |G| = |N| * |H|
            h3 = (len(int_elements) == 1) and (len(G_elements) == len(N_elements) * len(H_elements))
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: N_G(H) is not equal to the internal semidirect product of C_N(H) and H
    try:
        # Normalizer of H in G
        N_G_H = set()
        for g in G_elements:
            if all((g * h * ~g) in H_set for h in H_elements):
                N_G_H.add(g)
        
        # Centralizer of H in N
        C_N_H = set()
        for n in N_elements:
            if all((n * h * ~n) == h for h in H_elements):
                C_N_H.add(n)
        
        # Set product of C_N(H) and H
        C_N_H_times_H = set()
        for c in C_N_H:
            for h in H_elements:
                C_N_H_times_H.add(c * h)
        
        # If they are not equal as sets, they cannot be equal as internal semidirect products
        neg_q = (N_G_H != C_N_H_times_H)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "H_3: G is the internal semidirect product of N and H",
    "¬Q: N_G(H) is not equal to the internal semidirect product of C_N(H) and H"
]

N_HYP = 3
NEG_Q_INDEX = 3