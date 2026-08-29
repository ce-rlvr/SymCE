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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, B) where G is a PermutationGroup and B is a subset of its domain.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        G, B = witness
    except Exception:
        return [False, False]

    # H_1: G is a group acting transitively on a set X (and B is a non-empty subset of X)
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        elif not G.is_transitive:
            h1 = False
        elif not isinstance(B, (set, list, tuple)):
            h1 = False
        elif len(B) == 0:
            h1 = False
        elif not set(B).issubset(set(range(G.degree))):
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: The setwise stabilizer of B in G does NOT act transitively on the elements of B
    try:
        if not h1:
            neg_q = False
        else:
            # Safeguard against excessively large groups
            order = G.order() if callable(G.order) else G.order
            if order > 10000:
                neg_q = False
            else:
                B_set = set(B)
                stab_elements = []
                
                # Find all elements in G that stabilize the set B
                for g in G.elements:
                    if {g(b) for b in B_set} == B_set:
                        stab_elements.append(g)
                
                # Check if the setwise stabilizer acts transitively on B
                # Since B is non-empty, we can check the orbit of a single element
                b0 = next(iter(B_set))
                orbit = {g(b0) for g in stab_elements}
                
                if orbit == B_set:
                    neg_q = False  # Acts transitively, so negated conclusion is False
                else:
                    neg_q = True   # Does NOT act transitively, so negated conclusion is True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting transitively on a set X",
    "¬Q: The setwise stabilizer of B in G does not act transitively on the elements of B"
]

N_HYP = 1
NEG_Q_INDEX = 1