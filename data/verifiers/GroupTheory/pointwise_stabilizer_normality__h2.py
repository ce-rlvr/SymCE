import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
    """
    Given a witness, checks if it satisfies the hypotheses and FAILS the conclusion.
    The witness can be of the form (G, Y), (G, Y, action), or (G, X, Y, action).
    """
    try:
        if len(witness) == 2:
            G, Y = witness
            def action(g, y):
                try:
                    return g(y)
                except TypeError:
                    return g * y
        elif len(witness) == 3:
            if callable(witness[2]):
                G, Y, action = witness
            else:
                G, X, Y = witness
                def action(g, y):
                    try:
                        return g(y)
                    except TypeError:
                        return g * y
        elif len(witness) == 4:
            G, X, Y, action = witness
        else:
            return [False, False, False, False]
            
        try:
            iter(Y)
        except TypeError:
            Y = [Y]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group acting on a set X
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        elif hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
        h1 = len(elements) > 0
    except Exception:
        h1 = False

    # H2: G_{(Y)} is the pointwise stabilizer of Y
    try:
        G_pY = []
        for g in elements:
            if all(action(g, y) == y for y in Y):
                G_pY.append(g)
        h2 = True
    except Exception:
        h2 = False

    # H3: G_{Y} is the setwise stabilizer of Y
    try:
        G_Y = []
        for g in elements:
            gY = []
            for y in Y:
                gY.append(action(g, y))
            
            is_eq = True
            for y in Y:
                if y not in gY:
                    is_eq = False
                    break
            if is_eq:
                for gy in gY:
                    if gy not in Y:
                        is_eq = False
                        break
            if is_eq:
                G_Y.append(g)
        h3 = True
    except Exception:
        h3 = False

    # ¬Q: The pointwise stabilizer G_{(Y)} is NOT a normal subgroup of the setwise stabilizer G_{Y}
    try:
        is_normal = True
        
        # A subgroup must be non-empty (contains the identity)
        if not G_pY:
            is_normal = False
            
        # G_{(Y)} must be a subgroup of G_{Y}
        if is_normal:
            for h in G_pY:
                if h not in G_Y:
                    is_normal = False
                    break
        
        # Check normality condition: for all g in G_Y and h in G_pY, g * h * g^-1 is in G_pY
        if is_normal:
            for g in G_Y:
                try:
                    ginv = ~g
                except Exception:
                    try:
                        ginv = g**-1
                    except Exception:
                        ginv = g.inv()
                
                for h in G_pY:
                    conj = g * h * ginv
                    if conj not in G_pY:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
        neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: G_{(Y)} is the pointwise stabilizer of Y",
    "H_3: G_{Y} is the setwise stabilizer of Y",
    "¬Q: The pointwise stabilizer G_{(Y)} is NOT a normal subgroup of the setwise stabilizer G_{Y}"
]

N_HYP = 3
NEG_Q_INDEX = 3