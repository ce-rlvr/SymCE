import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite p-group",
    "H_3: X is a finite set",
    "H_4: G acts on X",
    "¬Q: |X^G| is not congruent to |X| modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    p = None
    G = None
    X = None
    action = None
    
    try:
        if isinstance(witness, PermutationGroup):
            G = witness
            order = G.order()
            factors = sympy.factorint(order)
            if len(factors) == 1:
                p = list(factors.keys())[0]
            else:
                p = 2
            X = list(range(G.degree))
            action = lambda g, x: g(x)
        elif isinstance(witness, dict):
            p = witness.get('p')
            G = witness.get('G')
            X = witness.get('X')
            action = witness.get('action')
    except Exception:
        pass

    def apply_act(g, x):
        if callable(action):
            return action(g, x)
        else:
            return action[g][x]

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: G is a finite p-group
    try:
        if not isinstance(G, PermutationGroup):
            h2 = False
        else:
            order = G.order()
            if order == 1:
                h2 = True
            else:
                factors = sympy.factorint(order)
                h2 = (list(factors.keys()) == [p])
    except Exception:
        h2 = False

    # H_3: X is a finite set
    try:
        h3 = isinstance(X, (list, set, tuple))
        if h3:
            X_set = set(X)
            _ = len(X)
    except Exception:
        h3 = False

    # H_4: G acts on X
    try:
        h4 = True
        if not h2 or not h3:
            h4 = False
        elif G.order()**2 * len(X) > 2000000:
            # Prevent timeout for excessively large groups
            h4 = False
        else:
            id_g = G.identity
            for x in X:
                res = apply_act(id_g, x)
                if res != x or res not in X_set:
                    h4 = False
                    break
            if h4:
                elements = list(G.elements)
                for g in elements:
                    for h in elements:
                        gh = g * h
                        for x in X:
                            hx = apply_act(h, x)
                            if hx not in X_set:
                                h4 = False
                                break
                            g_hx = apply_act(g, hx)
                            gh_x = apply_act(gh, x)
                            if g_hx != gh_x:
                                h4 = False
                                break
                        if not h4: break
                    if not h4: break
    except Exception:
        h4 = False

    # ¬Q: |X^G| is not congruent to |X| modulo p
    try:
        if not isinstance(p, (int, sympy.Integer)):
            neg_q = False
        else:
            fixed_points = 0
            elements = list(G.elements)
            for x in X:
                is_fixed = True
                for g in elements:
                    if apply_act(g, x) != x:
                        is_fixed = False
                        break
                if is_fixed:
                    fixed_points += 1
            
            neg_q = bool((fixed_points % p) != (len(X) % p))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]