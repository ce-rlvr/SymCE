import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_attr(w, attr):
    if isinstance(w, dict):
        return w[attr]
    return getattr(w, attr)

def conditions(witness) -> list[bool]:
    try:
        G = get_attr(witness, 'G')
        X = get_attr(witness, 'X')
        action = get_attr(witness, 'action')
        N = get_attr(witness, 'N')
        x = get_attr(witness, 'x')
    except Exception:
        return [False] * 5

    # H1: G is a group acting on a set X
    h1_ok = False
    try:
        if hasattr(G, 'elements') and hasattr(G, 'identity') and isinstance(X, (set, list, tuple)) and callable(action):
            h1_ok = True
            for y in X:
                if action(G.identity, y) != y:
                    h1_ok = False
                    break
            if h1_ok:
                for g in G.elements:
                    for h in G.elements:
                        for y in X:
                            if action(g * h, y) != action(g, action(h, y)):
                                h1_ok = False
                                break
                        if not h1_ok: break
                    if not h1_ok: break
    except Exception:
        h1_ok = False

    # H2: N is a normal subgroup of G
    h2_ok = False
    try:
        if hasattr(N, 'is_subgroup') and hasattr(N, 'is_normal'):
            h2_ok = N.is_subgroup(G) and N.is_normal(G)
        else:
            h2_ok = True
            for n in N.elements:
                if n not in G.elements:
                    h2_ok = False
                    break
            if h2_ok:
                for g in G.elements:
                    for n in N.elements:
                        if g * n * g**-1 not in N.elements:
                            h2_ok = False
                            break
                    if not h2_ok: break
    except Exception:
        h2_ok = False

    # H3: N acts trivially on X
    h3_ok = False
    try:
        h3_ok = True
        for n in N.elements:
            for y in X:
                if action(n, y) != y:
                    h3_ok = False
                    break
            if not h3_ok: break
    except Exception:
        h3_ok = False

    # H4: x is an element of X
    h4_ok = False
    try:
        h4_ok = x in X
    except Exception:
        h4_ok = False

    # Conclusion: The stabilizer of x in G/N is the quotient group G_x/N
    # Negated Conclusion: The stabilizer of x in G/N is NOT the quotient group G_x/N
    neg_q_ok = False
    try:
        def get_coset(g, subgroup):
            return frozenset(g * n for n in subgroup.elements)

        # G/N
        G_mod_N = {get_coset(g, N) for g in G.elements}
        
        # Stabilizer of x in G/N
        stab_G_mod_N = set()
        for C in G_mod_N:
            g = next(iter(C))
            if action(g, x) == x:
                stab_G_mod_N.add(C)
                
        # G_x
        G_x = {g for g in G.elements if action(g, x) == x}
        
        # G_x/N
        G_x_mod_N = {get_coset(g, N) for g in G_x}
        
        neg_q_ok = stab_G_mod_N != G_x_mod_N
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: N is a normal subgroup of G",
    "H_3: N acts trivially on X",
    "H_4: x is an element of X",
    "¬Q: The stabilizer of x in G/N is not the quotient group G_x/N"
]

N_HYP = 4
NEG_Q_INDEX = 4