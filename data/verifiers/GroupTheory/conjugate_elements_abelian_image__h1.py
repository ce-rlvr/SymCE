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
    Check if the witness is a valid counterexample to the conjecture.
    witness format expected: (G, H, f, x, y)
    where f can be a callable, a dictionary, or a list of (g, f(g)) tuples.
    """
    try:
        G, H, f_map, x, y = witness
    except Exception:
        return [False, False, False, False]

    # Normalize the mapping f
    try:
        if callable(f_map):
            f = f_map
        elif isinstance(f_map, (list, tuple)):
            f_dict = dict(f_map)
            f = lambda g: f_dict[g]
        else:
            f = lambda g: f_map[g]
    except Exception:
        return [False, False, False, False]

    # Extract elements
    try:
        G_elems = list(G.elements)
        H_elems = list(H.elements)
    except Exception:
        return [False, False, False, False]

    # H_1: f: G -> H is a group homomorphism
    try:
        h1 = True
        for g in G_elems:
            if f(g) not in H_elems:
                h1 = False
                break
        if h1:
            for g1 in G_elems:
                for g2 in G_elems:
                    if f(g1 * g2) != f(g1) * f(g2):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: H is an abelian group
    try:
        h2 = bool(H.is_abelian)
    except Exception:
        h2 = False

    # H_3: x and y are elements of G such that x and y are conjugate in G
    try:
        h3 = False
        if x in G_elems and y in G_elems:
            for g in G_elems:
                try:
                    inv_g = ~g
                except Exception:
                    inv_g = g**-1
                
                if g * x * inv_g == y:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # neg_Q: f(x) != f(y)  (Conclusion FAILS)
    try:
        neg_q = bool(f(x) != f(y))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "H_2: H is an abelian group",
    "H_3: x and y are conjugate elements in G",
    "¬Q: f(x) != f(y)"
]

N_HYP = 3
NEG_Q_INDEX = 3