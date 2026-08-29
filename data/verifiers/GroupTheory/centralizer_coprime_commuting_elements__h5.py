import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros, Matrix
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

def get_order(e):
    if hasattr(e, 'order'):
        if callable(e.order):
            return e.order()
        return e.order
    if hasattr(e, 'det'):
        try:
            I = e.__class__.eye(e.shape[0])
            curr = e
            for i in range(1, 1000):
                if curr == I:
                    return i
                curr = curr * e
            return 0
        except Exception:
            return 0
    return 0

def are_coprime(ox, oy):
    # If an element has infinite order (0), it shares no prime factors with finite numbers,
    # satisfying the coprime condition in the context of the dropped finite-order hypothesis.
    if ox == 0 or oy == 0:
        return True
    return math.gcd(ox, oy) == 1

def conditions(witness):
    try:
        G = None
        g = None
        
        # Unpack witness
        if len(witness) == 2:
            x, y = witness
        elif len(witness) == 3:
            if hasattr(witness[0], 'generators') or hasattr(witness[0], 'elements'):
                G, x, y = witness
            else:
                x, y, g = witness
        else:
            return [False] * 7

        # H_1: G is a group
        if G is not None:
            h1 = hasattr(G, 'elements') or hasattr(G, 'generators')
        else:
            # Implicit General Linear Group for matrices
            h1 = hasattr(x, 'det') and x.det() != 0 and hasattr(y, 'det') and y.det() != 0
            if g is not None:
                h1 = h1 and hasattr(g, 'det') and g.det() != 0

        # H_2: x is an element of G
        # H_3: y is an element of G
        if G is not None:
            try:
                h2 = x in G.elements if hasattr(G, 'elements') else True
                h3 = y in G.elements if hasattr(G, 'elements') else True
            except Exception:
                h2 = h3 = False
        else:
            h2 = hasattr(x, 'det') and x.det() != 0
            h3 = hasattr(y, 'det') and y.det() != 0

        # H_4: x and y commute
        try:
            h4 = bool(x * y == y * x)
        except Exception:
            h4 = False

        # H_5: y has finite order
        try:
            oy = get_order(y)
            h5 = (oy > 0)
        except Exception:
            h5 = False

        # H_6: The orders of x and y are coprime
        try:
            ox = get_order(x)
            h6 = are_coprime(ox, oy)
        except Exception:
            h6 = False

        # ¬Q: The centralizer of xy in G is NOT equal to the intersection of C_G(x) and C_G(y)
        neg_q = False
        try:
            xy = x * y
            if G is not None and hasattr(G, 'elements'):
                C_xy = set(elem for elem in G.elements if elem * xy == xy * elem)
                C_x = set(elem for elem in G.elements if elem * x == x * elem)
                C_y = set(elem for elem in G.elements if elem * y == y * elem)
                C_x_cap_y = C_x.intersection(C_y)
                neg_q = (C_xy != C_x_cap_y)
                
            elif g is not None:
                g_in_Cxy = bool(g * xy == xy * g)
                g_in_Cx = bool(g * x == x * g)
                g_in_Cy = bool(g * y == y * g)
                g_in_Cx_cap_Cy = g_in_Cx and g_in_Cy
                neg_q = (g_in_Cxy != g_in_Cx_cap_Cy)
                
            elif hasattr(x, 'shape'):
                n = x.shape[0]
                A_mat = sympy.Matrix(sympy.MatrixSymbol('A', n, n))
                vars_A = list(A_mat)
                
                # Dimension of C(xy) algebra
                eqs_xy = list(A_mat * xy - xy * A_mat)
                sol_xy = sympy.solve(eqs_xy, vars_A, dict=True)
                dim_xy = len([v for v in vars_A if v not in sol_xy[0]]) if sol_xy else 0
                
                # Dimension of C(x) \cap C(y) algebra
                eqs_x_y = list(A_mat * x - x * A_mat) + list(A_mat * y - y * A_mat)
                sol_x_y = sympy.solve(eqs_x_y, vars_A, dict=True)
                dim_x_y = len([v for v in vars_A if v not in sol_x_y[0]]) if sol_x_y else 0
                
                neg_q = (dim_xy != dim_x_y)
        except Exception:
            neg_q = False

        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(h6), bool(neg_q)]
        
    except Exception:
        return [False] * 7

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "H_3: y is an element of G",
    "H_4: x and y commute",
    "H_5: y has finite order",
    "H_6: The orders of x and y are coprime",
    "¬Q: The centralizer of xy in G is NOT equal to the intersection of the centralizer of x in G and the centralizer of y in G"
]

N_HYP = 6
NEG_Q_INDEX = 6