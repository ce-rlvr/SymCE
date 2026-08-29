import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_num_conjugacy_classes(G):
    try:
        elements = list(G.elements)
        classes = []
        seen = set()
        for x in elements:
            if x in seen:
                continue
            cclass = set()
            for g in elements:
                conj = g * x * (~g)
                cclass.add(conj)
                seen.add(conj)
            classes.append(cclass)
        return len(classes)
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            k = witness.get('k')
            r = witness.get('r')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, k, r = witness
            elif len(witness) == 2:
                G, k = witness
                r = get_num_conjugacy_classes(G)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: r is the number of isomorphism classes of irreducible complex representations of G
    try:
        num_classes = get_num_conjugacy_classes(G)
        h2_ok = (num_classes is not None) and (r == num_classes)
    except Exception:
        h2_ok = False

    # ¬Q: k != r
    try:
        neg_q_ok = (k != r)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: r is the number of isomorphism classes of irreducible complex representations of G",
    "¬Q: k != r"
]

N_HYP = 2
NEG_Q_INDEX = 2