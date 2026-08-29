import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x')
            y = witness.get('y')
            g = witness.get('g')
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            G, x, y, g = witness
        else:
            return [False, False]
            
        try:
            if hasattr(G, '__contains__'):
                h1 = (x in G) and (y in G) and (g in G)
            else:
                h1 = False
        except TypeError:
            try:
                h1 = isinstance(x, G) and isinstance(y, G) and isinstance(g, G)
            except Exception:
                h1 = False
    except Exception:
        h1 = False

    def get_inv(elem):
        try:
            return elem**-1
        except Exception:
            return ~elem

    try:
        x_inv = get_inv(x)
        y_inv = get_inv(y)
        g_inv = get_inv(g)
        
        c1_xy = x * y * x_inv * y_inv
        gxg1 = g * x * g_inv
        gyg1 = g * y * g_inv
        gxg1_inv = get_inv(gxg1)
        gyg1_inv = get_inv(gyg1)
        
        rhs1 = gxg1 * gyg1 * gxg1_inv * gyg1_inv
        lhs1 = g * c1_xy * g_inv
        if lhs1 == rhs1:
            q_eval1 = True
        else:
            try:
                if hasattr(lhs1, 'equals') and lhs1.equals(rhs1):
                    q_eval1 = True
                else:
                    q_eval1 = bool(sympy.simplify(lhs1 - rhs1) == 0)
            except Exception:
                q_eval1 = False
    except Exception:
        q_eval1 = False

    try:
        x_inv = get_inv(x)
        y_inv = get_inv(y)
        g_inv = get_inv(g)
        
        c2_xy = x_inv * y_inv * x * y
        gxg2 = g * x * g_inv
        gyg2 = g * y * g_inv
        gxg2_inv = get_inv(gxg2)
        gyg2_inv = get_inv(gyg2)
        
        rhs2 = gxg2_inv * gyg2_inv * gxg2 * gyg2
        lhs2 = g * c2_xy * g_inv
        if lhs2 == rhs2:
            q_eval2 = True
        else:
            try:
                if hasattr(lhs2, 'equals') and lhs2.equals(rhs2):
                    q_eval2 = True
                else:
                    q_eval2 = bool(sympy.simplify(lhs2 - rhs2) == 0)
            except Exception:
                q_eval2 = False
    except Exception:
        q_eval2 = False
        
    try:
        g_inv = get_inv(g)
        c3_xy = x * y - y * x
        gxg3 = g * x * g_inv
        gyg3 = g * y * g_inv
        
        rhs3 = gxg3 * gyg3 - gyg3 * gxg3
        lhs3 = g * c3_xy * g_inv
        if lhs3 == rhs3:
            q_eval3 = True
        else:
            try:
                if hasattr(lhs3, 'equals') and lhs3.equals(rhs3):
                    q_eval3 = True
                else:
                    q_eval3 = bool(sympy.simplify(lhs3 - rhs3) == 0)
            except Exception:
                q_eval3 = False
    except Exception:
        q_eval3 = False

    q_eval = q_eval1 or q_eval2 or q_eval3
    neg_q = not q_eval

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: x, y, and g are elements of G", "¬Q: conjugate of commutator is not equal to commutator of conjugates"]
N_HYP = 1
NEG_Q_INDEX = 1