import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

def conditions(witness) -> list[bool]:
    # Extract components
    try:
        if isinstance(witness, dict):
            G = witness.get('G', [])
            X = witness.get('X', [])
            act = witness.get('act')
            op = witness.get('op')
            e = witness.get('e')
        else:
            G = getattr(witness, 'G', [])
            X = getattr(witness, 'X', [])
            act = getattr(witness, 'act', None)
            op = getattr(witness, 'op', None)
            e = getattr(witness, 'e', None)
            
        if op is None:
            op = lambda a, b: a * b
        elif not callable(op):
            _op = op
            op = lambda a, b: _op[(a, b)]
            
        if act is not None and not callable(act):
            _act = act
            act = lambda g, x: _act[(g, x)]
            
        G = list(G)
        X = list(X)
    except Exception:
        return [False, False, False]

    # H1: X is a set
    try:
        h1_ok = False
        unique_X = []
        for x in X:
            if x not in unique_X:
                unique_X.append(x)
        h1_ok = (len(unique_X) == len(X))
    except Exception:
        h1_ok = False

    # H2: G acts on X
    try:
        h2_ok = False
        unique_G = []
        for g in G:
            if g not in unique_G:
                unique_G.append(g)
        
        if len(unique_G) == len(G) and len(G) > 0:
            # Find identity if not provided
            if e is None:
                identities = []
                for cand in G:
                    try:
                        if all(op(cand, g) == g and op(g, cand) == g for g in G):
                            identities.append(cand)
                    except Exception:
                        pass
                if len(identities) == 1:
                    e = identities[0]
            
            if e is not None and e in G:
                # Check monoid properties
                is_monoid = True
                for g in G:
                    if op(e, g) != g or op(g, e) != g:
                        is_monoid = False
                        break
                
                if is_monoid:
                    # Check associativity
                    assoc = True
                    for g in G:
                        for h in G:
                            for k in G:
                                if op(g, op(h, k)) != op(op(g, h), k):
                                    assoc = False
                                    break
                            if not assoc: break
                        if not assoc: break
                    
                    if assoc:
                        # Check action properties
                        action_valid = True
                        for x in X:
                            if act(e, x) != x:
                                action_valid = False
                                break
                        
                        if action_valid:
                            for g in G:
                                for x in X:
                                    if act(g, x) not in X:
                                        action_valid = False
                                        break
                                if not action_valid: break
                                
                        if action_valid:
                            for g in G:
                                for h in G:
                                    for x in X:
                                        if act(g, act(h, x)) != act(op(g, h), x):
                                            action_valid = False
                                            break
                                    if not action_valid: break
                                if not action_valid: break
                                
                        h2_ok = action_valid
    except Exception:
        h2_ok = False

    # neg_Q: The action is faithful if and only if the intersection of Stab_G(x) over all x in X is {e}.
    try:
        neg_q = False
        if h2_ok:
            # Find intersection of stabilizers
            K = []
            for g in G:
                fixes_all = True
                for x in X:
                    if act(g, x) != x:
                        fixes_all = False
                        break
                if fixes_all:
                    K.append(g)
            
            intersection_is_e = (len(K) == 1 and K[0] == e)
            
            # Check if faithful
            faithful = True
            for i in range(len(G)):
                for j in range(i + 1, len(G)):
                    g = G[i]
                    h = G[j]
                    same_action = True
                    for x in X:
                        if act(g, x) != act(h, x):
                            same_action = False
                            break
                    if same_action:
                        faithful = False
                        break
                if not faithful:
                    break
                    
            # The conclusion fails if the equivalence does not hold
            neg_q = (faithful != intersection_is_e)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts on X",
    "¬Q: The equivalence (faithful iff intersection of stabilizers is {e}) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2