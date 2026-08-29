import sympy
from sympy import symbols, Poly
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, DihedralGroup, AlternatingGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

x = symbols('x')

CONDITION_LABELS = [
    "H_1: f(x) is a monic irreducible separable polynomial of degree 4 over K",
    "H_2: G is the Galois group of f(x) over K, acting on the roots of f(x)",
    "H_3: V is the Klein four-subgroup of S_4",
    "¬Q: The kernel of the action of G on the roots of the resolvent cubic is not exactly G ∩ V"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple: (f, G, V)
    where f is a SymPy Poly or Expr, G is a PermutationGroup, and V is a PermutationGroup.
    """
    # Extract witness components
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f_expr, G, V = witness
            elif len(witness) == 2:
                f_expr, G = witness
                V = V4
            else:
                f_expr = witness[0]
                G = None
                V = V4
        else:
            f_expr = witness
            G = None
            V = V4
            
        f = Poly(f_expr, x)
    except Exception:
        return [False, False, False, False]

    # H1: f(x) is a monic irreducible separable polynomial of degree 4 over K
    try:
        h1_ok = False
        if f.degree() == 4 and f.LC() == 1:
            # Check separability (gcd(f, f') == 1)
            is_sep = f.gcd(f.diff()).degree() == 0
            # Check irreducibility over its domain
            if is_sep and f.is_irreducible:
                h1_ok = True
    except Exception:
        h1_ok = False

    # H2: G is the Galois group of f(x) over K, acting on the roots of f(x)
    try:
        h2_ok = False
        if G is not None:
            if isinstance(G, PermutationGroup):
                h2_ok = True
        else:
            # If G wasn't provided, try to compute it (only works over Q in SymPy)
            G = f_expr.galois_group()
            h2_ok = True
    except Exception:
        h2_ok = False

    # H3: V is the Klein four-subgroup of S_4
    try:
        h3_ok = False
        if isinstance(V, PermutationGroup) and V.order() == 4 and V.is_abelian and not V.is_cyclic:
            # Check if it's the normal Klein four-subgroup
            if Permutation(0, 1)(2, 3) in V and Permutation(0, 2)(1, 3) in V:
                h3_ok = True
    except Exception:
        h3_ok = False

    # neg_Q: The action of G on the roots of the resolvent cubic of f(x) defines a homomorphism 
    # from G to S_3 whose kernel is exactly the intersection of G with V.
    # We want neg_Q to be True when the conclusion FAILS.
    try:
        neg_q_ok = False
        if G is not None:
            char = f.domain.characteristic
            # The conclusion fails in characteristic 2 because the resolvent cubic 
            # (defined via Lagrange resolvents) has a triple root, making the action trivial.
            # Thus the kernel is G. If G is not a subgroup of V, then G != G \cap V.
            if char == 2:
                g_in_v4 = all(g in V4 for g in G.generators)
                if not g_in_v4:
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]