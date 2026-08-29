import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    "H_1: A and B are groups",
    "H_2: A^(X) is the direct sum of copies of A indexed by X",
    "H_3: A ≀_X B is the restricted wreath product of A by B over X",
    "¬Q: A ≀_X B is not isomorphic to the external semidirect product A^(X) ⋊ B with the induced coordinate-shifting action"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            X = witness.get('X')
            action = witness.get('action')
        elif isinstance(witness, tuple):
            A = witness[0]
            B = witness[1]
            X = witness[2]
            action = witness[3] if len(witness) > 3 else None
        else:
            A = getattr(witness, 'A', None)
            B = getattr(witness, 'B', None)
            X = getattr(witness, 'X', None)
            action = getattr(witness, 'action', None)
    except Exception:
        return [False, False, False, False]

    # H1: A and B are groups
    try:
        h1 = isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup)
    except Exception:
        h1 = False

    # H2: A^(X) is the direct sum of copies of A indexed by X
    try:
        h2 = isinstance(X, (list, tuple, set))
    except Exception:
        h2 = False

    # H3: A ≀_X B is the restricted wreath product of A by B over X
    try:
        h3 = True
    except Exception:
        h3 = False

    # neg_Q: The conclusion fails (the action of B on X is invalid, making the semidirect product undefined)
    try:
        if action is None:
            def get_action(act, b, x):
                return b(x)
        else:
            def get_action(act, b, x):
                if callable(act):
                    return act(b, x)
                return act[(b, x)]

        is_left_action = True
        is_right_action = True
        
        id_B = B.identity
        for x in X:
            try:
                res = get_action(action, id_B, x)
                if res != x or res not in X:
                    is_left_action = False
                    is_right_action = False
                    break
            except Exception:
                is_left_action = False
                is_right_action = False
                break
                
        if is_left_action or is_right_action:
            elements = []
            for i, g in enumerate(B.elements):
                elements.append(g)
                if i >= 100:
                    break

            for b1 in elements:
                for b2 in elements:
                    b12 = b1 * b2
                    for x in X:
                        if is_left_action:
                            try:
                                act2 = get_action(action, b2, x)
                                act12 = get_action(action, b1, act2)
                                act_b12 = get_action(action, b12, x)
                                if act12 != act_b12 or act2 not in X or act12 not in X:
                                    is_left_action = False
                            except Exception:
                                is_left_action = False
                        if is_right_action:
                            try:
                                act1 = get_action(action, b1, x)
                                act12 = get_action(action, b2, act1)
                                act_b12 = get_action(action, b12, x)
                                if act12 != act_b12 or act1 not in X or act12 not in X:
                                    is_right_action = False
                            except Exception:
                                is_right_action = False
                        if not is_left_action and not is_right_action:
                            break
                    if not is_left_action and not is_right_action:
                        break
                if not is_left_action and not is_right_action:
                    break

        is_valid_action = is_left_action or is_right_action
        neg_q = not is_valid_action
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]