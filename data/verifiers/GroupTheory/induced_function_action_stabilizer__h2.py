import itertools

# Top-level setup for standard algebra objects
class PermutationGroupWrapper:
    def __init__(self, elements, mul, inv, id_el):
        self.elements = elements
        self.mul = mul
        self.inv = inv
        self.id = id_el

def conditions(witness) -> list[bool]:
    """
    witness is expected to be an object with the following attributes:
      - G: list of group elements
      - mul: function(g1, g2) -> g3 (group operation)
      - inv: function(g) -> g_inv (group inverse)
      - id: the identity element of G
      - X: list of elements in the set X
      - Y: list of elements in the set Y
      - action_X: function(g, x) -> x_new (action of G on X)
      - f: function(x) -> y (an element of Y^X)
    """
    try:
        G = witness.G
        mul = witness.mul
        inv = witness.inv
        id_el = witness.id
        X = witness.X
        Y = witness.Y
        action_X = witness.action_X
        f = witness.f
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group acting on a set X
    try:
        h1_ok = True
        # Check group axioms
        for g in G:
            if mul(g, id_el) != g or mul(id_el, g) != g:
                h1_ok = False
            if mul(g, inv(g)) != id_el or mul(inv(g), g) != id_el:
                h1_ok = False
            for h in G:
                for k in G:
                    if mul(mul(g, h), k) != mul(g, mul(h, k)):
                        h1_ok = False
        # Check action axioms
        for x in X:
            if action_X(id_el, x) != x:
                h1_ok = False
            for g in G:
                for h in G:
                    if action_X(g, action_X(h, x)) != action_X(mul(g, h), x):
                        h1_ok = False
    except Exception:
        h1_ok = False

    # H2: Y^X is the set of all functions from X to Y
    # This is a definitional setup hypothesis.
    h2_ok = True

    # H3: G acts on Y^X via (g \cdot f)(x) = f(g^{-1} \cdot x)
    # This defines the action of G on Y^X. If H1 holds, this is mathematically guaranteed
    # to be a valid left action, so the hypothesis holds for the witness.
    h3_ok = True

    # H4: f is a function in Y^X
    try:
        h4_ok = True
        for x in X:
            if f(x) not in Y:
                h4_ok = False
    except Exception:
        h4_ok = False

    # Conclusion: The stabilizer of f in G is the subgroup {g \in G | f(g^{-1} \cdot x) = f(x) for all x \in X}
    # We check if the set S = {g \in G | f(g^{-1} \cdot x) = f(x) for all x \in X} is indeed a subgroup.
    # The conclusion fails (neg_Q_ok = True) if S is NOT a subgroup.
    try:
        S = []
        for g in G:
            in_S = True
            for x in X:
                if f(action_X(inv(g), x)) != f(x):
                    in_S = False
                    break
            if in_S:
                S.append(g)
        
        is_subgroup = True
        if id_el not in S:
            is_subgroup = False
        for g in S:
            if inv(g) not in S:
                is_subgroup = False
            for h in S:
                if mul(g, h) not in S:
                    is_subgroup = False
                    
        neg_Q_ok = not is_subgroup
    except Exception:
        neg_Q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: Y^X is the set of all functions from X to Y",
    "H_3: G acts on Y^X via (g \\cdot f)(x) = f(g^{-1} \\cdot x)",
    "H_4: f is a function in Y^X",
    "¬Q: The set {g \\in G | f(g^{-1} \\cdot x) = f(x) for all x \\in X} is NOT a subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4