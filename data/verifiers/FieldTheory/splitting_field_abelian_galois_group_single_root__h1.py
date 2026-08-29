import sympy as sp
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings that the witness expression may reference.
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
# V4 is the Klein four-group, a transitive abelian subgroup of S4
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for a given witness.
    The witness is expected to be a PermutationGroup representing the Galois group 
    Gal(E/F) acting on the roots of f(x), or a tuple (G, alpha) where alpha is a specific root.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, alpha = witness
        else:
            G = witness
            alpha = None
            
        # H_1: f(x) is an irreducible separable polynomial
        # In terms of the Galois group acting on the roots, f(x) is irreducible 
        # if and only if the Galois group acts transitively.
        h1 = bool(G.is_transitive)
    except Exception:
        h1 = False

    # H_2: E is the splitting field of f(x) over F
    # The permutation group G represents Gal(E/F) by definition, so E is the splitting field.
    h2 = True

    try:
        # H_3: Gal(E/F) is an abelian group
        h3 = bool(G.is_abelian)
    except Exception:
        h3 = False

    # H_4: alpha is a root of f(x)
    # alpha corresponds to a point in the domain of the permutation group.
    h4 = True

    try:
        # ¬Q: F(alpha) is not equal to E
        # By the Orbit-Stabilizer Theorem and Galois correspondence:
        # [E : F] = |G| = G.order()
        # [F(alpha) : F] = size of the orbit of alpha
        # Therefore, F(alpha) != E iff the orbit size is not equal to the group order.
        order = G.order()
        if alpha is not None:
            orbit_size = 0
            for orbit in G.orbits():
                if alpha in orbit:
                    orbit_size = len(orbit)
                    break
            neg_q = bool(orbit_size != order)
        else:
            # If no specific root is provided, check if there exists any root alpha such that F(alpha) != E
            neg_q = any(len(orbit) != order for orbit in G.orbits())
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is an irreducible separable polynomial",
    "H_2: E is the splitting field of f(x) over F",
    "H_3: Gal(E/F) is an abelian group",
    "H_4: alpha is a root of f(x)",
    "¬Q: F(alpha) is not equal to E"
]

N_HYP = 4
NEG_Q_INDEX = 4