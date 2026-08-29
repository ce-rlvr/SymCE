import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for standard algebra objects
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

def is_group(G):
    """Helper to check if an object is a group."""
    return hasattr(G, 'is_group') and G.is_group

def is_homomorphism(f, G, H):
    """Helper to check if f is a group homomorphism from G to H."""
    if not (is_group(G) and is_group(H)):
        return False
    try:
        for x in G.elements:
            for y in G.elements:
                if f(x * y) != f(x) * f(y):
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion at the witness.
    witness is expected to be a tuple: (G, H1, H2, f, H1xH2, pi1, pi2)
    """
    try:
        G, H1, H2, f, H1xH2, pi1, pi2 = witness
    except Exception:
        return [False, False, False]

    # H_1: f: G -> H1 x H2 is a function
    try:
        h1_ok = True
        for x in G.elements:
            fx = f(x)
            if fx not in H1xH2.elements:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # H_2: pi1 and pi2 are the canonical projection homomorphisms
    try:
        h2_ok = True
        # Check if pi1 and pi2 are homomorphisms
        if not (is_homomorphism(pi1, H1xH2, H1) and is_homomorphism(pi2, H1xH2, H2)):
            h2_ok = False
        else:
            # Check if they are canonical projections
            for elem in H1xH2.elements:
                if pi1(elem) != elem[0] or pi2(elem) != elem[1]:
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False

    # neg_Q: The conclusion FAILS.
    # Conclusion: f is a group homomorphism iff both pi1 o f and pi2 o f are group homomorphisms.
    try:
        def pi1_f(x): return pi1(f(x))
        def pi2_f(x): return pi2(f(x))
        
        f_is_hom = is_homomorphism(f, G, H1xH2)
        pi1_f_is_hom = is_homomorphism(pi1_f, G, H1)
        pi2_f_is_hom = is_homomorphism(pi2_f, G, H2)
        
        rhs = pi1_f_is_hom and pi2_f_is_hom
        conclusion = (f_is_hom == rhs)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f: G -> H_1 x H_2 is a function",
    "H_2: pi_1 and pi_2 are the canonical projection homomorphisms",
    "¬Q: It is NOT the case that (f is a group homomorphism iff both pi_1 o f and pi_2 o f are group homomorphisms)"
]

N_HYP = 2
NEG_Q_INDEX = 2