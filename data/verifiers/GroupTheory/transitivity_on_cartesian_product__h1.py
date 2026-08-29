import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def extract(witness):
    """Extracts G, X, Y, action_X, action_Y, x from the witness."""
    if isinstance(witness, tuple):
        G, X, Y, aX, aY, x = witness[0], witness[1], witness[2], witness[3], witness[4], witness[5]
    elif isinstance(witness, dict):
        G, X, Y, aX, aY, x = witness['G'], witness['X'], witness['Y'], witness['action_X'], witness['action_Y'], witness['x']
    else:
        G, X, Y, aX, aY, x = witness.G, witness.X, witness.Y, witness.action_X, witness.action_Y, witness.x
    return list(G), list(X), list(Y), aX, aY, x

def apply_action(action, g, pt):
    """Applies the action of g on pt."""
    if callable(action):
        return action(g, pt)
    else:
        act_g = action[g]
        if callable(act_g):
            return act_g(pt)
        else:
            return act_g[pt]

def conditions(witness) -> list[bool]:
    try:
        G, X, Y, action_X, action_Y, x = extract(witness)
    except Exception:
        return [False, False, False, False]
    
    # H_1: G acts transitively on X
    try:
        h1 = True
        if X:
            for a in X:
                for b in X:
                    if not any(apply_action(action_X, g, a) == b for g in G):
                        h1 = False
                        break
                if not h1:
                    break
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: G acts transitively on Y
    try:
        h2 = True
        if Y:
            for a in Y:
                for b in Y:
                    if not any(apply_action(action_Y, g, a) == b for g in G):
                        h2 = False
                        break
                if not h2:
                    break
        else:
            h2 = True
    except Exception:
        h2 = False

    # H_3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # ¬Q: The diagonal action of G on X \times Y is transitive iff G_x acts transitively on Y is FALSE
    try:
        # Check if diagonal action is transitive
        diag_trans = True
        if X and Y:
            for x1 in X:
                for y1 in Y:
                    for x2 in X:
                        for y2 in Y:
                            if not any(apply_action(action_X, g, x1) == x2 and apply_action(action_Y, g, y1) == y2 for g in G):
                                diag_trans = False
                                break
                        if not diag_trans: break
                    if not diag_trans: break
                if not diag_trans: break
        else:
            diag_trans = True

        # Find the stabilizer G_x
        Gx = []
        for g in G:
            if apply_action(action_X, g, x) == x:
                Gx.append(g)
        
        # Check if G_x acts transitively on Y
        gx_trans = True
        if Y:
            for y1 in Y:
                for y2 in Y:
                    if not any(apply_action(action_Y, g, y1) == y2 for g in Gx):
                        gx_trans = False
                        break
                if not gx_trans:
                    break
        else:
            gx_trans = True

        # The conclusion fails if the two transitivity conditions are not equivalent
        neg_q = (diag_trans != gx_trans)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G acts transitively on X",
    "H_2: G acts transitively on Y",
    "H_3: x is an element of X",
    "¬Q: The equivalence between diagonal transitivity and stabilizer transitivity fails"
]

N_HYP = 3
NEG_Q_INDEX = 3