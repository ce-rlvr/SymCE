import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, X, act = witness
        elif hasattr(witness, 'G') and hasattr(witness, 'X') and hasattr(witness, 'act'):
            G = witness.G
            X = witness.X
            act = witness.act
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: G is a group
    try:
        h1 = False
        if hasattr(G, 'is_group') and getattr(G, 'is_group'):
            h1 = True
            try:
                elements = list(G.elements)
            except Exception:
                elements = list(G.generate())
            identity = G.identity
        elif isinstance(G, PermutationGroup):
            h1 = True
            try:
                elements = list(G.elements)
            except Exception:
                elements = list(G.generate())
            identity = G.identity
        elif isinstance(G, (list, tuple, set)) and len(G) > 0:
            elements = list(G)
            identity = None
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
            if identity is not None:
                is_group = True
                for x in elements:
                    has_inv = False
                    for y in elements:
                        try:
                            if x * y == identity and y * x == identity:
                                has_inv = True
                                break
                        except Exception:
                            pass
                    if not has_inv:
                        is_group = False
                        break
                    for y in elements:
                        try:
                            if x * y not in elements:
                                is_group = False
                                break
                        except Exception:
                            is_group = False
                            break
                    if not is_group:
                        break
                h1 = is_group
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple))
        X_list = list(X)
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails.
    # The conclusion "The kernel of the action ... is equal to the intersection ..." 
    # is a mathematical tautology IF the operation is a valid group action.
    # The only way it fails (becomes undefined/false) is if the operation is NOT a valid action.
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            is_action = True
            try:
                # Check identity axiom
                for x in X_list:
                    val = act(identity, x) if callable(act) else act[(identity, x)]
                    if val != x or val not in X_list:
                        is_action = False
                        break
                
                # Check closure
                if is_action:
                    for g in elements:
                        for x in X_list:
                            val = act(g, x) if callable(act) else act[(g, x)]
                            if val not in X_list:
                                is_action = False
                                break
                        if not is_action:
                            break
                
                # Check compatibility axiom
                if is_action:
                    for g in elements:
                        for h in elements:
                            gh = g * h
                            for x in X_list:
                                if callable(act):
                                    hx = act(h, x)
                                    g_hx = act(g, hx)
                                    gh_x = act(gh, x)
                                else:
                                    hx = act[(h, x)]
                                    g_hx = act[(g, hx)]
                                    gh_x = act[(gh, x)]
                                if g_hx != gh_x:
                                    is_action = False
                                    break
                            if not is_action:
                                break
                        if not is_action:
                            break
            except Exception:
                # If calling the operation raises an error, it's not a valid action
                is_action = False
            
            neg_q = not is_action
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "¬Q: The kernel of the action of G on X is not equal to the intersection of Stab_G(x) over all x in X (fails because the operation is not a valid action)"
]

N_HYP = 2
NEG_Q_INDEX = 2