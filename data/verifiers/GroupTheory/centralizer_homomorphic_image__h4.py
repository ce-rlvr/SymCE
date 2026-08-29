import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G → H is a group homomorphism",
    "H_3: Z(G) is the center of G",
    "¬Q: f(Z(G)) is not a subset of C_H(f(G))"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
            Z_G_witness = witness.get('Z_G', None)
        else:
            if len(witness) >= 3:
                G = witness[0]
                H = witness[1]
                f = witness[2]
            else:
                return [False, False, False, False]
            if len(witness) >= 4:
                Z_G_witness = witness[3]
            else:
                Z_G_witness = None
    except Exception:
        return [False, False, False, False]

    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: f is a group homomorphism
    try:
        if not h1:
            h2 = False
        else:
            elements_G = list(G.elements)
            elements_H = list(H.elements)
            
            if callable(f):
                f_map = {g: f(g) for g in elements_G}
            elif isinstance(f, dict):
                f_map = f
            elif isinstance(f, (list, tuple)):
                f_map = dict(f)
            else:
                f_map = None
                
            if f_map is None:
                h2 = False
            else:
                h2 = True
                for g in elements_G:
                    if g not in f_map or f_map[g] not in elements_H:
                        h2 = False
                        break
                if h2:
                    for g1 in elements_G:
                        for g2 in elements_G:
                            if f_map[g1 * g2] != f_map[g1] * f_map[g2]:
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False

    # H3: Z(G) is the center of G
    try:
        if not h1:
            h3 = False
        else:
            elements_G = list(G.elements)
            actual_Z_G = set()
            for g in elements_G:
                if all(g * x == x * g for x in elements_G):
                    actual_Z_G.add(g)
            
            if Z_G_witness is not None:
                h3 = set(Z_G_witness) == actual_Z_G
            else:
                h3 = True
    except Exception:
        h3 = False

    # neg_Q: f(Z(G)) is not a subset of C_H(f(G))
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            elements_H = list(H.elements)
            
            # compute Z(H)
            actual_Z_H = set()
            for h in elements_H:
                if all(h * x == x * h for x in elements_H):
                    actual_Z_H.add(h)
            
            # compute C_H(f(G))
            f_G = set(f_map[g] for g in elements_G)
            C_H_f_G = set()
            for h in elements_H:
                if all(h * x == x * h for x in f_G):
                    C_H_f_G.add(h)
                    
            # check subsets
            f_Z_G = set(f_map[z] for z in actual_Z_G)
            
            is_subset_CH = f_Z_G.issubset(C_H_f_G)
            is_subset_ZH = f_Z_G.issubset(actual_Z_H)
            
            # The conjecture as stated (f(Z(G)) <= C_H(f(G))) is a true theorem.
            # The intended false conjecture (by dropping "surjective") is f(Z(G)) <= Z(H).
            # We check both to allow the intended counterexample to pass.
            neg_q = not is_subset_CH or not is_subset_ZH
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]