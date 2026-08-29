import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            op_G = witness.get('op_G')
            op_H = witness.get('op_H')
            f = witness.get('f')
            e_G = witness.get('e_G')
            e_H = witness.get('e_H')
        else:
            G = getattr(witness, 'G', None)
            H = getattr(witness, 'H', None)
            op_G = getattr(witness, 'op_G', None)
            op_H = getattr(witness, 'op_H', None)
            f = getattr(witness, 'f', None)
            e_G = getattr(witness, 'e_G', None)
            e_H = getattr(witness, 'e_H', None)

        if op_G is None:
            op_G = lambda x, y: x * y
        if op_H is None:
            op_H = lambda x, y: x * y
            
        if e_G is None and hasattr(G, 'identity'):
            e_G = G.identity
        if e_H is None and hasattr(H, 'identity'):
            e_H = H.identity
            
        def get_elements(group):
            if hasattr(group, 'elements'):
                return list(group.elements)
            return list(group)
            
        G_elements = get_elements(G)
        H_elements = get_elements(H)

        def eval_f(x):
            if isinstance(f, dict):
                for k, v in f.items():
                    if k == x:
                        return v
                raise KeyError(f"Key {x} not found in f")
            return f(x)
            
        def eval_op_G(x, y):
            if isinstance(op_G, dict):
                for k, v in op_G.items():
                    if k == (x, y) or (isinstance(k, tuple) and len(k) == 2 and k[0] == x and k[1] == y):
                        return v
                raise KeyError(f"Key {(x, y)} not found in op_G")
            return op_G(x, y)
            
        def eval_op_H(x, y):
            if isinstance(op_H, dict):
                for k, v in op_H.items():
                    if k == (x, y) or (isinstance(k, tuple) and len(k) == 2 and k[0] == x and k[1] == y):
                        return v
                raise KeyError(f"Key {(x, y)} not found in op_H")
            return op_H(x, y)
            
        h1 = True
        for x in G_elements:
            fx = eval_f(x)
            if not any(fx == h for h in H_elements):
                h1 = False
                break
            for y in G_elements:
                f_xy = eval_f(eval_op_G(x, y))
                fx_fy = eval_op_H(fx, eval_f(y))
                if not (f_xy == fx_fy):
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    try:
        neg_q = not (eval_f(e_G) == e_H)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism from G to H",
    "¬Q: f(e_G) != e_H"
]

N_HYP = 1
NEG_Q_INDEX = 1