import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard groups and matrices
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should represent a monoid action on a set that violates the Orbit-Stabilizer formula.
    Expected witness formats:
      - dict with keys: 'G', 'op_G', 'id_G', 'X', 'action', 'x'
      - object with attributes: G, op_G, id_G, X, action, x
      - tuple of length 6: (G, op_G, id_G, X, action, x)
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 6:
            G, op_G, id_G, X, action, x = witness
        elif isinstance(witness, dict):
            G = witness['G']
            op_G = witness['op_G']
            id_G = witness['id_G']
            X = witness['X']
            action = witness['action']
            x = witness['x']
        elif hasattr(witness, 'G') and hasattr(witness, 'op_G') and hasattr(witness, 'X'):
            G = witness.G
            op_G = witness.op_G
            id_G = witness.id_G
            X = witness.X
            action = witness.action
            x = witness.x
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def apply2(f, a, b):
        if callable(f):
            return f(a, b)
        try:
            return f[(a, b)]
        except (KeyError, TypeError):
            pass
        return f[a][b]

    # H1: X is a set
    try:
        if hasattr(X, '__iter__') and not isinstance(X, str):
            X_list = list(X)
            h1 = len(X_list) == len(set(X_list))
            X = X_list
        elif isinstance(X, str):
            X_list = list(X)
            h1 = len(X_list) == len(set(X_list))
            X = X_list
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: G acts on X
    try:
        h2 = True
        if hasattr(G, '__iter__') and not isinstance(G, str):
            G_list = list(G)
            if len(G_list) != len(set(G_list)):
                h2 = False
            G = G_list
        elif isinstance(G, str):
            G_list = list(G)
            if len(G_list) != len(set(G_list)):
                h2 = False
            G = G_list
        else:
            h2 = False
        
        if h2:
            if id_G not in G:
                h2 = False
            
            # Check monoid axioms
            if h2:
                for g in G:
                    if apply2(op_G, id_G, g) != g:
                        h2 = False
                        break
                    if apply2(op_G, g, id_G) != g:
                        h2 = False
                        break
                    for h in G:
                        gh = apply2(op_G, g, h)
                        if gh not in G:
                            h2 = False
                            break
                        for k in G:
                            if apply2(op_G, gh, k) != apply2(op_G, g, apply2(op_G, h, k)):
                                h2 = False
                                break
                        if not h2: break
                    if not h2: break
            
            # Check action axioms
            if h2:
                for y in X:
                    if apply2(action, id_G, y) != y:
                        h2 = False
                        break
                    for g in G:
                        gy = apply2(action, g, y)
                        if gy not in X:
                            h2 = False
                            break
                        for h in G:
                            h_y = apply2(action, h, y)
                            if apply2(action, g, h_y) != apply2(action, apply2(op_G, g, h), y):
                                h2 = False
                                break
                        if not h2: break
                    if not h2: break
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # Conclusion: |G| = |Orb_G(x)| * |Stab_G(x)|
    try:
        orb = set()
        stab = set()
        for g in G:
            gx = apply2(action, g, x)
            orb.add(gx)
            if gx == x:
                stab.add(g)
        
        q = (len(G) == len(orb) * len(stab))
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts on X",
    "H_3: x is an element of X",
    "¬Q: |G| != |Orb_G(x)| * |Stab_G(x)|"
]

N_HYP = 3
NEG_Q_INDEX = 3