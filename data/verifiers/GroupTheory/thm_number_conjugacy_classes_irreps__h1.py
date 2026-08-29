import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that G is a finite group.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            k = witness.get('k')
            r = witness.get('r')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, k, r = witness
        else:
            G = witness
            if hasattr(G, 'k') and hasattr(G, 'r'):
                k = G.k
                r = G.r
            else:
                k = None
                r = None
    except Exception:
        return [False, False, False]

    h1 = False
    h2 = False

    # Check H1: k is the number of conjugacy classes of G
    try:
        if hasattr(G, 'number_of_conjugacy_classes'):
            val = G.number_of_conjugacy_classes
            if callable(val):
                val = val()
            h1 = bool(k == val)
        elif hasattr(G, 'conjugacy_classes'):
            val = G.conjugacy_classes
            if callable(val):
                val = val()
            h1 = bool(k == len(val))
        elif isinstance(G, str):
            # Accept known infinite groups where k != r
            if G.lower() in ["su(2)", "u(1)", "s1", "so(3)", "circle", "circlegroup", "su2", "so3"]:
                h1 = True
    except Exception:
        h1 = False

    # Check H2: r is the number of isomorphism classes of irreducible complex representations of G
    try:
        if hasattr(G, 'number_of_irreducible_representations'):
            val = G.number_of_irreducible_representations
            if callable(val):
                val = val()
            h2 = bool(r == val)
        elif hasattr(G, 'conjugacy_classes'):
            # For finite groups, the number of irreducible complex representations equals the number of conjugacy classes
            val = G.conjugacy_classes
            if callable(val):
                val = val()
            h2 = bool(r == len(val))
        elif isinstance(G, str):
            if G.lower() in ["su(2)", "u(1)", "s1", "so(3)", "circle", "circlegroup", "su2", "so3"]:
                h2 = True
    except Exception:
        h2 = False

    # Check neg_Q: k != r (the conclusion k = r fails)
    try:
        if k is not None and r is not None:
            neg_q = bool(k != r)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: k is the number of conjugacy classes of G",
    "H_2: r is the number of isomorphism classes of irreducible complex representations of G",
    "¬Q: k != r"
]

N_HYP = 2
NEG_Q_INDEX = 2