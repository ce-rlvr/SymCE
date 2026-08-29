import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, X, x) or a dict with these keys.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            x = witness.get('x')
        else:
            G, X, x = witness
    except Exception:
        return [False, False]

    # H_1: G is a group acting on a set X
    try:
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(X, (set, list, tuple)):
            # Check if X is closed under the action of G
            is_closed = True
            for g in G.generators:
                for y in X:
                    try:
                        if g(y) not in X:
                            is_closed = False
                            break
                    except Exception:
                        is_closed = False
                        break
                if not is_closed:
                    break
            h1 = is_closed
    except Exception:
        h1 = False

    # ¬Q: The element x is a fixed point of the action of G if and only if the stabilizer of x in G is equal to G.
    try:
        # x is a fixed point of the action of G on X if it is in X and fixed by all elements of G.
        is_fixed_point = (x in X) and all(g(x) == x for g in G.generators)
        
        # The stabilizer of x in G is equal to G if all elements of G fix x.
        # Note: The stabilizer is well-defined even if x is not in X.
        stab_equals_G = all(g(x) == x for g in G.generators)
        
        # The conjecture states: is_fixed_point == stab_equals_G
        # We want the negation of this conjecture (i.e., it fails at the witness).
        conjecture_holds = (is_fixed_point == stab_equals_G)
        neg_q = not conjecture_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "¬Q: The stabilizer of x is G, but x is not a fixed point of the action (e.g., x is not in X)"
]

N_HYP = 1
NEG_Q_INDEX = 1