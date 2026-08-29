import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def inv(g):
    try:
        return g**-1
    except Exception:
        pass
    try:
        return ~g
    except Exception:
        pass
    try:
        return g.inv()
    except Exception:
        pass
    raise ValueError("No inverse found")

def comm(a, b):
    return inv(a) * inv(b) * a * b

def conditions(witness):
    try:
        witness = tuple(witness)
        if len(witness) == 4:
            G, x, y, z = witness
        elif len(witness) == 3:
            x, y, z = witness
            G = None
        else:
            return [False, False]
    except Exception:
        return [False, False]
    
    try:
        _ = inv(x)
        _ = inv(y)
        _ = inv(z)
        _ = x * y * z
        if G is not None:
            if hasattr(G, 'contains'):
                h1 = bool(G.contains(x) and G.contains(y) and G.contains(z))
            elif hasattr(G, '__contains__'):
                h1 = bool(x in G and y in G and z in G)
            else:
                h1 = True
        else:
            h1 = True
    except Exception:
        h1 = False

    try:
        z_inv = inv(z)
        lhs = z_inv * comm(x, y) * z
        zx = z_inv * x * z
        zy = z_inv * y * z
        rhs = comm(zx, zy)
        
        if isinstance(lhs, sympy.Expr) and isinstance(rhs, sympy.Expr):
            neg_q = bool(sympy.simplify(lhs - rhs) != 0)
        else:
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: x, y, and z are elements of G", "¬Q: conjugate of commutator is not equal to commutator of conjugates"]
N_HYP = 1
NEG_Q_INDEX = 1