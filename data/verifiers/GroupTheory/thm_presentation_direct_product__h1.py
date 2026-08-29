import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings for witness expressions
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

def conditions(witness) -> list[bool]:
    """
    Expects witness to be a tuple:
    (G, H, X_str, R_func, Y_str, S_func)
    where:
      - G, H are SymPy PermutationGroups
      - X_str, Y_str are lists of strings (generator names, e.g., ['x'])
      - R_func, S_func are functions taking the generators and returning a list of relator words
    """
    try:
        G, H, X_str, R_func, Y_str, S_func = witness
    except Exception:
        return [False, False, False]
    
    # H_1: H is a group with presentation < Y | S >
    try:
        if not Y_str:
            h1_ok = bool(H.order() == 1)
        else:
            F_Y = free_group(",".join(Y_str))[0]
            S = S_func(*F_Y.generators)
            if not isinstance(S, (list, tuple)):
                S = [S]
            # In SymPy, FreeGroup / relators returns an FpGroup
            H_pres = F_Y / S
            h1_ok = bool(H.order() == H_pres.order())
    except Exception:
        h1_ok = False

    # H_2: The sets X and Y are disjoint
    try:
        h2_ok = bool(set(X_str).isdisjoint(set(Y_str)))
    except Exception:
        h2_ok = False

    # neg_Q: G x H does not have the presentation < X U Y | R U S U { [x, y] = 1 } >
    try:
        XY_str = list(X_str) + list(Y_str)
        if not XY_str:
            GH_pres_order = 1
        else:
            F_XY = free_group(",".join(XY_str))[0]
            x_gens = F_XY.generators[:len(X_str)]
            y_gens = F_XY.generators[len(X_str):]
            
            if not X_str:
                R = []
            else:
                R = R_func(*x_gens)
                if not isinstance(R, (list, tuple)):
                    R = [R]
                    
            if not Y_str:
                S = []
            else:
                S = S_func(*y_gens)
                if not isinstance(S, (list, tuple)):
                    S = [S]
                    
            commutators = [x * y * x**-1 * y**-1 for x in x_gens for y in y_gens]
            GH_pres = F_XY / (list(R) + list(S) + commutators)
            GH_pres_order = GH_pres.order()
            
        gh_order = G.order() * H.order()
        # If the orders differ, they are definitely not isomorphic
        neg_q = bool(gh_order != GH_pres_order)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H is a group with presentation < Y | S >",
    "H_2: The sets X and Y are disjoint",
    "¬Q: G x H does not have the presentation < X U Y | R U S U commutators >"
]

N_HYP = 2
NEG_Q_INDEX = 2