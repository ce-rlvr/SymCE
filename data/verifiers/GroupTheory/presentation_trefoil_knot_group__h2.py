import sympy
from sympy.combinatorics import PermutationGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: K is the trefoil knot in the 3-sphere S^3",
    "¬Q: G does not admit the presentation <x, y | x^2 = y^3>"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    K = None
    G = None
    
    # Parse the witness
    try:
        if isinstance(witness, dict):
            K = witness.get('K')
            G = witness.get('G')
        elif hasattr(witness, 'K') and hasattr(witness, 'G'):
            K = witness.K
            G = witness.G
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            K, G = witness
        else:
            if isinstance(witness, str):
                K = witness
            else:
                G = witness
    except Exception:
        pass

    # Evaluate H_1: K is the trefoil knot
    try:
        if isinstance(K, str):
            h1_ok = 'trefoil' in K.lower()
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # Evaluate ¬Q: G does not admit the presentation <x, y | x^2 = y^3>
    # The presentation defines the braid group B_3, which is infinite.
    # Any finite group (like a PermutationGroup) cannot admit this presentation.
    try:
        neg_q_ok = False
        if G is not None:
            if isinstance(G, PermutationGroup):
                neg_q_ok = True
            elif hasattr(G, 'order'):
                try:
                    ord_g = G.order()
                    if ord_g != float('inf'):
                        neg_q_ok = True
                except Exception:
                    pass
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]