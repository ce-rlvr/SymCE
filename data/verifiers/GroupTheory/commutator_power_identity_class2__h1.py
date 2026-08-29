import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    Given a witness (G, x, y, n), checks if it is a valid counterexample to the conjecture.
    Returns [H1_ok, H2_ok, H3_ok, neg_Q_ok].
    """
    try:
        G, x, y, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is nilpotent of class at most 2
    # This means the derived subgroup [G, G] is contained in the center Z(G).
    try:
        if hasattr(G, 'derived_subgroup'):
            derived = G.derived_subgroup()
            h1 = True
            for d in derived.generators:
                for g in G.generators:
                    if d * g != g * d:
                        h1 = False
                        break
                if not h1:
                    break
        else:
            # Fallback for iterable of elements
            elements = list(G)
            commutators = []
            for a in elements:
                for b in elements:
                    commutators.append((a**-1) * (b**-1) * a * b)
            h1 = True
            for c in commutators:
                for g in elements:
                    if c * g != g * c:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: Let x and y be elements of G
    try:
        if hasattr(G, 'contains'):
            h2 = bool(G.contains(x) and G.contains(y))
        else:
            h2 = (x in G) and (y in G)
    except Exception:
        h2 = False

    # H_3: Let n be an integer
    try:
        h3 = isinstance(n, int)
    except Exception:
        h3 = False

    # ¬Q: (xy)^n != x^n y^n comm(y, x)^(n(n-1)/2)
    try:
        lhs = (x * y) ** n
        
        x_n = x ** n
        y_n = y ** n
        # Standard group-theoretic commutator [y, x] = y^-1 x^-1 y x
        comm = (y**-1) * (x**-1) * y * x
        exponent = n * (n - 1) // 2
        
        rhs = x_n * y_n * (comm ** exponent)
        
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is nilpotent of class at most 2",
    "H_2: x and y are elements of G",
    "H_3: n is an integer",
    "¬Q: (xy)^n != x^n y^n comm(y, x)^(n(n-1)/2)"
]

N_HYP = 3
NEG_Q_INDEX = 3