import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import totient
import math

# Top-level setup: named object bindings that the witness expression may reference.
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def holomorph_Zn(n):
    """Constructs the holomorph of Z_n as a PermutationGroup."""
    if n == 1:
        return CyclicGroup(1)
    perms = []
    for v in range(n):
        for a in range(1, n):
            if math.gcd(a, n) == 1:
                # The action of (v, a) on x is a*x + v mod n
                p = [(a * x + v) % n for x in range(n)]
                perms.append(Permutation(p))
    return PermutationGroup(perms)

def are_isomorphic(G1, G2):
    """Checks if two permutation groups are isomorphic."""
    if G1.order() != G2.order():
        return False
    if hasattr(G1, 'is_isomorphic'):
        try:
            if G1.is_isomorphic(G2):
                return True
        except Exception:
            pass
    # Fallback: compare order profiles
    try:
        def order_profile(G):
            profile = {}
            for g in G.generate():
                o = g.order()
                profile[o] = profile.get(o, 0) + 1
            return profile
        return order_profile(G1) == order_profile(G2)
    except Exception:
        return False

def get_holomorph_n(G):
    """Returns n if G is isomorphic to Hol(Z_n), else None."""
    try:
        if not hasattr(G, 'order'):
            return None
        order = G.order()
        # The order of Hol(Z_n) is n * phi(n)
        for n in range(1, order + 2):
            if n * totient(n) == order:
                H = holomorph_Zn(n)
                if are_isomorphic(G, H):
                    return n
        return None
    except Exception:
        return None

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    The conjecture claims that Hol(Z_n) admits a specific presentation.
    This is true for all n >= 2. However, for n = 1, the set of units is U_1 = {1},
    and the relation y_a * y_b = y_{ab mod n} becomes y_1 * y_1 = y_0.
    Since y_0 is not in the generating set {y_1}, the presentation is syntactically invalid.
    Thus, the conclusion fails for n = 1 (the dropped hypothesis was n >= 2).
    """
    try:
        n = get_holomorph_n(witness)
        h1 = (n is not None)
    except Exception:
        h1 = False

    try:
        # The conclusion fails (neg_Q is True) if the presentation is invalid, which happens iff n == 1.
        neg_q = (n == 1) if h1 else False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the holomorph of a finite cyclic group Z_n",
    "¬Q: G does not admit the specified presentation"
]

N_HYP = 1
NEG_Q_INDEX = 1