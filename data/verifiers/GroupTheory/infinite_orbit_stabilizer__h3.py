import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                G, X, action, x = witness
            elif len(witness) == 3:
                G, X, x = witness
                action = lambda g, y: g(y)
            else:
                return [False, False, False, False]
        else:
            G = witness.G
            X = witness.X
            x = witness.x
            if hasattr(witness, 'action'):
                action = witness.action
            else:
                action = lambda g, y: g(y)
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) or (hasattr(G, 'elements') and hasattr(G, 'identity'))
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple, sympy.Set))
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        if isinstance(X, sympy.Set):
            h3 = (X.contains(x) == sympy.true) or (x in X)
        else:
            h3 = x in X
    except Exception:
        h3 = False

    # neg_Q: The cardinality of the orbit G \cdot x is equal to the index of the stabilizer subgroup G_x in G.
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
            identity = G.identity
        else:
            elements = G.elements() if callable(G.elements) else list(G.elements)
            identity = G.identity
            
        orbit = []
        for g in elements:
            res = action(g, x)
            found = False
            for item in orbit:
                if res == item:
                    found = True
                    break
            if not found:
                orbit.append(res)
        orbit_size = len(orbit)
        
        stab_elements = []
        for g in elements:
            if action(g, x) == x:
                stab_elements.append(g)
                
        is_subgroup = True
        if identity not in stab_elements:
            is_subgroup = False
        else:
            for g1 in stab_elements:
                for g2 in stab_elements:
                    if (g1 * g2) not in stab_elements:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
                    
        if not is_subgroup:
            neg_q = True
        else:
            # Check if orbit_size == index of stabilizer
            # Using multiplication to avoid floating point issues: orbit_size * |G_x| == |G|
            neg_q = (orbit_size * len(stab_elements) != len(elements))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: x is an element of X",
    "¬Q: Cardinality of orbit G.x is not equal to the index of stabilizer G_x in G"
]

N_HYP = 3
NEG_Q_INDEX = 3