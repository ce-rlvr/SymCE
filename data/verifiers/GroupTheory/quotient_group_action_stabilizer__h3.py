import itertools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: N is a normal subgroup of G",
    "H_3: G/N acts on X via the induced action (gN) \\cdot x = g \\cdot x",
    "H_4: x is an element of X",
    "¬Q: The stabilizer of x in G/N is NOT the quotient group G_x/N"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be an object (e.g., a custom class or namedtuple) with attributes:
      - G: a group (e.g., a SymPy PermutationGroup or a list of elements with a defined multiplication)
      - X: a list or set of elements representing the set X
      - action: a callable `action(g, y)` returning the result of g acting on y
      - N: a subgroup of G (same type as G)
      - x: an element of X
      - mul: (optional) a callable `mul(g1, g2)` for group multiplication if G is a custom list
      - e: (optional) the identity element of G
    """
    try:
        G = witness.G
        X = list(witness.X)
        action = witness.action
        N = witness.N
        x_elem = witness.x
        
        # Determine elements and group operations
        if hasattr(G, 'elements'):
            G_elements = list(G.elements)
            N_elements = list(N.elements) if hasattr(N, 'elements') else list(N)
            mul = lambda g1, g2: g1 * g2
            e = G.identity if hasattr(G, 'identity') else G_elements[0] # Fallback
        else:
            G_elements = list(G)
            N_elements = list(N)
            mul = witness.mul
            e = witness.e

        # H_1: G is a group acting on a set X
        h1 = True
        if x_elem not in X:
            h1 = False
        for y in X:
            if action(e, y) != y:
                h1 = False
                break
            for g1 in G_elements:
                for g2 in G_elements:
                    if action(g1, action(g2, y)) != action(mul(g1, g2), y):
                        h1 = False
                        break
                if not h1:
                    break
            if not h1:
                break

        # H_2: N is a normal subgroup of G
        h2 = True
        if e not in N_elements:
            h2 = False
        else:
            for n1 in N_elements:
                for n2 in N_elements:
                    if mul(n1, n2) not in N_elements:
                        h2 = False
                        break
                if not h2:
                    break
            if h2:
                for g in G_elements:
                    # Find inverse of g
                    g_inv = next((h for h in G_elements if mul(g, h) == e), None)
                    if g_inv is None:
                        h2 = False
                        break
                    for n in N_elements:
                        if mul(g, mul(n, g_inv)) not in N_elements:
                            h2 = False
                            break
                    if not h2:
                        break

        # H_3: G/N acts on X via the induced action (gN) \cdot x = g \cdot x
        # For the induced action to be well-defined on X, N must act trivially on X.
        h3 = True
        for n in N_elements:
            for y in X:
                if action(n, y) != y:
                    h3 = False
                    break
            if not h3:
                break

        # H_4: x is an element of X
        h4 = x_elem in X

        # ¬Q: The stabilizer of x in G/N is NOT the quotient group G_x/N
        # G_x is the stabilizer of x in G
        G_x = [g for g in G_elements if action(g, x_elem) == x_elem]
        
        # For G_x/N to be a valid quotient group, N must be a subgroup of G_x.
        # If N is a subgroup of G_x, then the stabilizer of x in G/N is exactly G_x/N.
        # If N is not a subgroup of G_x, then G_x/N is not a valid quotient group,
        # so the conclusion fails.
        N_in_Gx = all(n in G_x for n in N_elements)
        neg_q = not N_in_Gx

        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]