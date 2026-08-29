import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness):
    """
    witness: (G, X, Y, x, y)
    G: PermutationGroup
    X, Y: lists or sets of integers representing orbits of G (transitive G-sets)
    x, y: integers in the domain of G
    """
    try:
        if len(witness) != 5:
            return [False, False, False]
        G, X, Y, x, y = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: X and Y are transitive G-sets
    # In the natural action, a transitive G-set is exactly one orbit of G.
    try:
        if not h1:
            h2 = False
        else:
            orbits = [set(o) for o in G.orbits()]
            h2 = (set(X) in orbits) and (set(Y) in orbits)
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails at the witness.
    # Conclusion: X and Y are isomorphic as G-sets <=> Stab_G(x) and Stab_G(y) are conjugate in G.
    # We check if the LHS and RHS of the iff statement have different truth values.
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            # LHS: X and Y are isomorphic as G-sets.
            # Two orbits are isomorphic iff the stabilizer of an element in X 
            # is exactly the stabilizer of some element in Y.
            x0 = list(X)[0]
            stab_x0 = G.stabilizer(x0)
            lhs = any(stab_x0 == G.stabilizer(y_elem) for y_elem in Y)
            
            # RHS: Stab_G(x) and Stab_G(y) are conjugate in G.
            # The conjugates of Stab_G(y) are exactly the stabilizers of the elements in the orbit of y.
            stab_x = G.stabilizer(x)
            rhs = any(stab_x == G.stabilizer(z) for z in G.orbit(y))
            
            # The conjecture claims LHS == RHS. It fails if LHS != RHS.
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X and Y are transitive G-sets",
    "¬Q: (X and Y are isomorphic) XOR (Stab(x) and Stab(y) are conjugate)"
]

N_HYP = 2
NEG_Q_INDEX = 2