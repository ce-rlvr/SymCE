import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: phi is an automorphism of G",
    "H_3: For all g in G, phi(g) = g implies g is the identity element",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3

def evaluate_phi(phi, g):
    if isinstance(phi, dict):
        return phi[g]
    return phi(g)

def conditions(witness):
    try:
        G, phi = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            elements = list(G.elements)
            h1 = len(elements) > 0
    except Exception:
        h1 = False

    # H_2: phi is an automorphism of G
    try:
        if not h1:
            h2 = False
        else:
            is_hom = True
            for x in elements:
                for y in elements:
                    if evaluate_phi(phi, x * y) != evaluate_phi(phi, x) * evaluate_phi(phi, y):
                        is_hom = False
                        break
                if not is_hom:
                    break
            
            if is_hom:
                images = set(evaluate_phi(phi, x) for x in elements)
                h2 = (images == set(elements))
            else:
                h2 = False
    except Exception:
        h2 = False

    # H_3: For all g in G, phi(g) = g implies g is the identity element
    try:
        if not h1:
            h3 = False
        else:
            h3 = True
            identity = G.identity
            for g in elements:
                if evaluate_phi(phi, g) == g:
                    if g != identity:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # ¬Q: G is not a solvable group
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = not G.is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]