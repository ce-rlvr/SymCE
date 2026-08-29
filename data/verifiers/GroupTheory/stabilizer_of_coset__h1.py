import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def inv(x):
    try:
        return ~x
    except Exception:
        return x**-1

def conditions(witness):
    try:
        G = witness[0]
        H = witness[1]
        a = witness[2]
        G_elems = list(G.elements)
        H_elems = list(H.elements)
    except Exception:
        return [False, False, False, False]

    # H_1: H is a subgroup of G
    try:
        h1 = hasattr(H, 'is_subgroup') and H.is_subgroup(G)
    except Exception:
        h1 = False

    # H_2: G acts on the set of left cosets G/H by left multiplication
    try:
        h2 = h1
    except Exception:
        h2 = False

    # H_3: aH is a left coset in G/H
    try:
        if isinstance(a, (set, list, tuple)):
            aH = set(a)
            h3 = False
            a_rep = None
            for x in G_elems:
                if aH == {x * h for h in H_elems}:
                    h3 = True
                    a_rep = x
                    break
        else:
            aH = {a * h for h in H_elems}
            h3 = False
            a_rep = None
            for x in G_elems:
                if aH == {x * h for h in H_elems}:
                    h3 = True
                    a_rep = x
                    break
    except Exception:
        h3 = False
        a_rep = None

    # ¬Q: The stabilizer of aH is not the conjugate subgroup aHa^{-1}
    try:
        if h1 and h3 and a_rep is not None:
            stab = set()
            for g in G_elems:
                g_aH = {g * x for x in aH}
                if g_aH == aH:
                    stab.add(g)
            
            if not isinstance(a, (set, list, tuple)):
                rep_for_conj = a
            else:
                rep_for_conj = a_rep
                
            conj = {rep_for_conj * h * inv(rep_for_conj) for h in H_elems}
            
            neg_q = stab != conj
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: G acts on the set of left cosets G/H by left multiplication",
    "H_3: aH is a left coset in G/H",
    "¬Q: The stabilizer of aH is not the conjugate subgroup aHa^{-1}"
]
N_HYP = 3
NEG_Q_INDEX = 3