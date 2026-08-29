import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    # H_1: Witness provides a group G, a set X, and an operation star(g, x)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, X, star = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, X = witness
            star = lambda g, x: g * x
        else:
            return [False, False]
            
        elements = list(G.elements)
        identity = G.identity
        X_list = list(X)
        
        # Limit size to prevent timeouts
        if len(X_list) > 12:
            h1 = False
        else:
            set(X_list) # Check hashability of elements
            h1 = callable(star)
    except Exception:
        h1 = False

    # neg_Q: The mapping g * A does NOT define a valid group action of G on P(X)
    try:
        if not h1:
            neg_q = False
        else:
            # Generate P(X)
            P_X = []
            for r in range(len(X_list) + 1):
                for combo in itertools.combinations(X_list, r):
                    P_X.append(frozenset(combo))
            
            is_valid_action = True
            
            # Check closure: g * A must be in P(X) (i.e., a subset of X)
            for g in elements:
                for A in P_X:
                    gA = frozenset(star(g, a) for a in A)
                    if not gA.issubset(X_list):
                        is_valid_action = False
                        break
                if not is_valid_action:
                    break
                    
            # Check identity axiom: e * A = A
            if is_valid_action:
                for A in P_X:
                    gA = frozenset(star(identity, a) for a in A)
                    if gA != A:
                        is_valid_action = False
                        break
                        
            # Check compatibility axiom: g * (h * A) = (g * h) * A
            if is_valid_action:
                for g in elements:
                    for h in elements:
                        gh = g * h
                        for A in P_X:
                            hA = frozenset(star(h, a) for a in A)
                            g_hA = frozenset(star(g, a) for a in hA)
                            gh_A = frozenset(star(gh, a) for a in A)
                            if g_hA != gh_A:
                                is_valid_action = False
                                break
                        if not is_valid_action:
                            break
                    if not is_valid_action:
                        break
                        
            neg_q = not is_valid_action
    except Exception:
        # If evaluating the action raises an error, it is not a valid action
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let P(X) be the power set of X (witness provides G, X, and operation)",
    "¬Q: The mapping g * A does not define a valid group action of G on P(X)"
]

N_HYP = 1
NEG_Q_INDEX = 1