import itertools
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: P(X) is the power set of X",
    "H_2: G acts on P(X) via the induced action g . S = {g . s | s in S} for all S subseteq X",
    "H_3: x is an element of X",
    "¬Q: The stabilizer of the singleton set {x} in the action on P(X) is not equal to the stabilizer of x in the action on X"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_attr(witness, name, default=None):
    if isinstance(witness, dict):
        return witness.get(name, default)
    return getattr(witness, name, default)

def conditions(witness):
    # Extract basic components
    try:
        X_obj = get_attr(witness, 'X')
        X_list = list(X_obj)
    except Exception:
        X_list = []

    try:
        x = get_attr(witness, 'x')
    except Exception:
        x = None

    try:
        P_X_obj = get_attr(witness, 'P_X')
        if P_X_obj is not None:
            actual_P_X = set(frozenset(S) for S in P_X_obj)
        else:
            actual_P_X = None
    except Exception:
        actual_P_X = None

    try:
        G_obj = get_attr(witness, 'G')
        if hasattr(G_obj, 'identity'):
            G = list(G_obj)
            identity = G_obj.identity
            op = lambda g, h: g * h
        else:
            G = list(G_obj)
            identity = get_attr(witness, 'identity')
            op = get_attr(witness, 'op')
    except Exception:
        G = []
        identity = None
        op = None

    action_P = get_attr(witness, 'action_P')
    action_X = get_attr(witness, 'action_X')

    # H_1: P(X) is the power set of X
    try:
        expected_P_X = set()
        for r in range(len(X_list) + 1):
            for combo in itertools.combinations(X_list, r):
                expected_P_X.add(frozenset(combo))
        
        if actual_P_X is None:
            actual_P_X = expected_P_X
            h1 = True
        else:
            h1 = (expected_P_X == actual_P_X)
    except Exception:
        h1 = False

    # H_2: G acts on P(X) via the induced action g . S = {g . s | s in S} for all S subseteq X
    try:
        if action_P is None and action_X is not None:
            action_P_eff = lambda g, S: frozenset(action_X(g, s) for s in S)
        else:
            action_P_eff = action_P

        is_action = True
        for S in actual_P_X:
            if frozenset(action_P_eff(identity, S)) != S:
                is_action = False
                break
        if is_action:
            for g in G:
                for h in G:
                    gh = op(g, h)
                    for S in actual_P_X:
                        step1 = frozenset(action_P_eff(h, S))
                        step2 = frozenset(action_P_eff(g, step1))
                        step3 = frozenset(action_P_eff(gh, S))
                        if step2 != step3:
                            is_action = False
                            break
                    if not is_action: break
                if not is_action: break

        induced_match = True
        if action_X is not None:
            for g in G:
                for S in actual_P_X:
                    induced = frozenset(action_X(g, s) for s in S)
                    if frozenset(action_P_eff(g, S)) != induced:
                        induced_match = False
                        break
                if not induced_match: break
        else:
            induced_match = False

        h2 = is_action and induced_match
    except Exception:
        h2 = False

    # H_3: x is an element of X
    try:
        h3 = x in X_list
    except Exception:
        h3 = False

    # ¬Q: The stabilizer of the singleton set {x} in the action on P(X) is not equal to the stabilizer of x in the action on X
    try:
        if action_P is None and action_X is not None:
            action_P_eff = lambda g, S: frozenset(action_X(g, s) for s in S)
        else:
            action_P_eff = action_P

        stab_P = set()
        for g in G:
            if frozenset(action_P_eff(g, frozenset([x]))) == frozenset([x]):
                stab_P.add(g)

        stab_X = set()
        for g in G:
            if action_X(g, x) == x:
                stab_X.add(g)

        neg_q = (stab_P != stab_X)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]