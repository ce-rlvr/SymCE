import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy import eye, zeros

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

def is_valid_action(G_list, mul, identity, S, action):
    try:
        for p in S:
            if action(identity, p) != p:
                return False
        for g in G_list:
            for p in S:
                if action(g, p) not in S:
                    return False
        is_left = True
        is_right = True
        for g in G_list:
            for h in G_list:
                for p in S:
                    if action(g, action(h, p)) != action(mul(g, h), p):
                        is_left = False
                    if action(g, action(h, p)) != action(mul(h, g), p):
                        is_right = False
        return is_left or is_right
    except Exception:
        return False

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture.
    witness is expected to be a dictionary with:
      - "G": A SymPy PermutationGroup OR an iterable of elements
      - "mul": Group operation (if G is not a PermutationGroup)
      - "id": Identity element (if G is not a PermutationGroup)
      - "X": Iterable representing set X
      - "Y": Iterable representing set Y
      - "action_X": Callable f(g, x) for the action of G on X
      - "action_Y": Callable f(g, y) for the action of G on Y
      - "x": The element whose stabilizer is being considered
    """
    G = witness.get("G")
    X = witness.get("X", [])
    Y = witness.get("Y", [])
    action_X = witness.get("action_X")
    action_Y = witness.get("action_Y")
    x = witness.get("x")
    
    try:
        if isinstance(G, PermutationGroup):
            if hasattr(G, "generate"):
                G_list = list(G.generate())
            elif hasattr(G, "elements"):
                G_list = list(G.elements)
            else:
                G_list = list(G)
            mul = lambda a, b: a * b
            identity = G.identity
        else:
            G_list = list(G)
            mul = witness.get("mul")
            identity = witness.get("id")
    except Exception:
        return [False, False, False, False, False]
        
    # H1: G is a group
    h1 = False
    try:
        if isinstance(G, PermutationGroup):
            h1 = True
        else:
            h1 = True
            for g in G_list:
                if mul(identity, g) != g or mul(g, identity) != g:
                    h1 = False
                    break
            if h1:
                for g in G_list:
                    has_inv = False
                    for h in G_list:
                        if mul(g, h) == identity and mul(h, g) == identity:
                            has_inv = True
                            break
                    if not has_inv:
                        h1 = False
                        break
            if h1:
                for a in G_list:
                    for b in G_list:
                        if mul(a, b) not in G_list:
                            h1 = False
                            break
            if h1:
                for a in G_list:
                    for b in G_list:
                        for c in G_list:
                            if mul(mul(a, b), c) != mul(a, mul(b, c)):
                                h1 = False
                                break
    except Exception:
        h1 = False

    # H2: X and Y are disjoint sets
    h2 = False
    try:
        h2 = True
        for x_elem in X:
            if x_elem in Y:
                h2 = False
                break
    except Exception:
        h2 = False

    # H3: G acts on X and G acts on Y
    h3 = False
    try:
        h3 = is_valid_action(G_list, mul, identity, X, action_X) and \
             is_valid_action(G_list, mul, identity, Y, action_Y)
    except Exception:
        h3 = False

    # H4: G acts on the disjoint union X U Y as defined
    h4 = False
    try:
        def action_XY(g, p):
            if p in X:
                return action_X(g, p)
            elif p in Y:
                return action_Y(g, p)
            else:
                raise ValueError("p not in X U Y")
                
        XY = list(X) + list(Y)
        h4 = is_valid_action(G_list, mul, identity, XY, action_XY)
    except Exception:
        h4 = False

    # neg_Q: The stabilizer of x in X U Y is not equal to the stabilizer of x in X
    neg_q = False
    try:
        # Stabilizer in X U Y
        if x in X:
            stab_XY = [g for g in G_list if action_X(g, x) == x]
        elif x in Y:
            stab_XY = [g for g in G_list if action_Y(g, x) == x]
        else:
            stab_XY = None
            
        # Stabilizer in X
        if x in X:
            stab_X = [g for g in G_list if action_X(g, x) == x]
        else:
            stab_X = None
            
        if stab_XY is None and stab_X is None:
            neg_q = False
        elif stab_XY is None or stab_X is None:
            neg_q = True
        else:
            neg_q = False
            for g in stab_XY:
                if g not in stab_X:
                    neg_q = True
                    break
            for g in stab_X:
                if g not in stab_XY:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X and Y are disjoint sets",
    "H_3: G acts on X and G acts on Y",
    "H_4: G acts on the disjoint union X U Y as defined",
    "¬Q: The stabilizer of x in X U Y is not equal to the stabilizer of x in X"
]

N_HYP = 4
NEG_Q_INDEX = 4