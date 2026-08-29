import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def apply_map(func, x):
    if callable(func):
        return func(x)
    return func[x]

def conditions(witness):
    try:
        G, H1, H2, f, g = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G, H_1, and H_2 are groups
    try:
        h1_ok = hasattr(G, 'elements') and hasattr(H1, 'elements') and hasattr(H2, 'elements')
    except Exception:
        h1_ok = False

    # H_2: f: G \to H_1 is a group homomorphism
    try:
        h2_ok = True
        for x in G.elements:
            fx = apply_map(f, x)
            if fx not in H1.elements:
                h2_ok = False
                break
            for y in G.elements:
                fy = apply_map(f, y)
                fxy = apply_map(f, x * y)
                if fxy != fx * fy:
                    h2_ok = False
                    break
            if not h2_ok:
                break
    except Exception:
        h2_ok = False

    # H_3: \phi: G \to H_1 \times H_2 is defined by \phi(x) = (f(x), g(x))
    # This means g is a well-defined function from G to H2.
    try:
        h3_ok = True
        for x in G.elements:
            gx = apply_map(g, x)
            if gx not in H2.elements:
                h3_ok = False
                break
    except Exception:
        h3_ok = False

    # ¬Q: The conclusion "The kernel of \phi is equal to \ker(f) \cap \ker(g)" fails.
    # The conclusion fails if \phi is not a homomorphism, because then "The kernel of \phi" is undefined.
    # Given f is a homomorphism, \phi is a homomorphism iff g is a homomorphism.
    try:
        neg_q = False
        for x in G.elements:
            for y in G.elements:
                gx = apply_map(g, x)
                gy = apply_map(g, y)
                gxy = apply_map(g, x * y)
                if gxy != gx * gy:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G, H_1, and H_2 are groups",
    "H_2: f: G \\to H_1 is a group homomorphism",
    "H_3: \\phi: G \\to H_1 \\times H_2 is defined by \\phi(x) = (f(x), g(x))",
    "¬Q: The kernel of \\phi is not equal to \\ker(f) \\cap \\ker(g) (e.g., \\phi is not a homomorphism)"
]

N_HYP = 3
NEG_Q_INDEX = 3