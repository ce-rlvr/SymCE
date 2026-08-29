import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    'Absence of Small Index Subgroups in Semisimple Groups'
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            G = witness
            H = None
    except Exception:
        G, H = witness, None

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is a semisimple group
    # A finite group is semisimple if it has no non-trivial abelian normal subgroups
    try:
        if h1:
            h2 = True
            for N in G.normal_subgroups():
                if N.order() > 1 and N.is_abelian:
                    h2 = False
                    break
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: G is a non-trivial group
    try:
        if h1:
            h3 = G.order() > 1
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The index of H in G is <= 4
    try:
        neg_q = False
        if h1:
            if H is not None:
                if isinstance(H, list):
                    H = PermutationGroup(H)
                if isinstance(H, PermutationGroup):
                    # Check if H is a subgroup of G
                    is_sub = True
                    for g in H.generators:
                        if g not in G:
                            is_sub = False
                            break
                    
                    # Check if H is a proper subgroup with index <= 4
                    if is_sub and H.order() < G.order():
                        idx = G.order() / H.order()
                        if idx <= 4:
                            neg_q = True
            else:
                # Fallback: if H is not explicitly provided, check if any proper normal subgroup has index <= 4
                for N in G.normal_subgroups():
                    if N.order() < G.order() and G.order() / N.order() <= 4:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: G is a non-trivial group",
    "¬Q: The index of H in G is <= 4"
]

N_HYP = 3
NEG_Q_INDEX = 3