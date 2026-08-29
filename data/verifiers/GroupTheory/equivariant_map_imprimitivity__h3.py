import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G = witness['G']
        Y = list(witness['Y'])
        action_Y = witness['action_Y']
        phi = witness['phi']
    except Exception:
        return [False, False, False]

    def eval_phi(x):
        if callable(phi): return phi(x)
        return phi[x]

    def eval_action_Y(g, y):
        if callable(action_Y): return action_Y(g, y)
        return action_Y[(g, y)]

    # H1: G is a group acting transitively on a set X
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        elif G.degree < 1:
            h1 = False
        else:
            trans = G.is_transitive
            if callable(trans):
                h1 = bool(trans())
            else:
                h1 = bool(trans)
    except Exception:
        h1 = False

    # H2: G acts on a set Y
    try:
        if not Y:
            h2 = False
        else:
            elements = list(G.elements)
            id_g = next(g for g in elements if g * g == g)
            valid = True
            for y in Y:
                if eval_action_Y(id_g, y) != y:
                    valid = False
                    break
            
            if valid:
                is_left = True
                is_right = True
                for g in elements:
                    for h in elements:
                        gh = g * h
                        for y in Y:
                            res_gh = eval_action_Y(gh, y)
                            res_left = eval_action_Y(g, eval_action_Y(h, y))
                            res_right = eval_action_Y(h, eval_action_Y(g, y))
                            if res_gh != res_left:
                                is_left = False
                            if res_gh != res_right:
                                is_right = False
                            if not is_left and not is_right:
                                break
                        if not is_left and not is_right:
                            break
                    if not is_left and not is_right:
                        break
                h2 = is_left or is_right
            else:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: The set of non-empty fibers does NOT form a system of imprimitivity
    try:
        if not h1:
            neg_q = False
        else:
            X = list(range(G.degree))
            elements = list(G.elements)
            
            is_system = True
            for x1 in X:
                for x2 in X:
                    if eval_phi(x1) == eval_phi(x2):
                        for g in elements:
                            gx1 = g(x1)
                            gx2 = g(x2)
                            if eval_phi(gx1) != eval_phi(gx2):
                                is_system = False
                                break
                    if not is_system:
                        break
                if not is_system:
                    break
                    
            neg_q = not is_system
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting transitively on a set X",
    "H_2: G acts on a set Y",
    "¬Q: The set of non-empty fibers of phi does not form a system of imprimitivity for the action of G on X"
]

N_HYP = 2
NEG_Q_INDEX = 2