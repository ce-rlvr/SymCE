import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2) # Klein four-group is isomorphic to D2
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
    try:
        G = None
        y = None
        action = None
        
        # Unpack witness
        if isinstance(witness, dict):
            G = witness.get('G')
            y = witness.get('y')
            # Fallback to conjugation if action is missing
            action = witness.get('action', lambda g, x: g * x * (~g))
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                if callable(witness[1]) or isinstance(witness[1], dict):
                    G, action, y = witness
                elif callable(witness[2]) or isinstance(witness[2], dict):
                    G, y, action = witness
                else:
                    G, action, y = witness
            elif len(witness) == 2:
                G, y = witness
                action = lambda g, x: g * x * (~g)
            else:
                return [False, False, False]
        elif hasattr(witness, 'G') and hasattr(witness, 'y'):
            G = witness.G
            y = witness.y
            action = getattr(witness, 'action', lambda g, x: g * x * (~g))
        else:
            return [False, False, False]

        if G is None or y is None:
            return [False, False, False]

        # H1: G is a group
        h1 = False
        elements = []
        identity = None
        
        if isinstance(G, PermutationGroup):
            h1 = True
            elements = list(G.generate())
            identity = G.identity
        elif isinstance(G, list) and len(G) > 0:
            elements = G
            # Find identity
            for e in elements:
                is_id = True
                for x in elements:
                    try:
                        if e * x != x or x * e != x:
                            is_id = False
                            break
                    except Exception:
                        is_id = False
                        break
                if is_id:
                    identity = e
                    break
            
            # Check inverses
            if identity is not None:
                h1 = True
                for x in elements:
                    has_inv = False
                    for y_inv in elements:
                        try:
                            if x * y_inv == identity and y_inv * x == identity:
                                has_inv = True
                                break
                        except Exception:
                            pass
                    if not has_inv:
                        h1 = False
                        break

        # H2: y is an element of G
        h2 = False
        if h1:
            h2 = y in elements

        # neg_Q: The stabilizer of y under this action is not the trivial subgroup {e}
        neg_q = False
        if h1 and h2 and identity is not None:
            for g in elements:
                if g != identity:
                    try:
                        if callable(action):
                            res = action(g, y)
                        elif isinstance(action, dict):
                            res = action.get((g, y), None)
                        else:
                            res = None
                        
                        if res == y:
                            neg_q = True
                            break
                    except Exception:
                        pass

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: y is an element of G",
    "not Q: The stabilizer of y under this action is not the trivial subgroup {e}"
]

N_HYP = 2
NEG_Q_INDEX = 2