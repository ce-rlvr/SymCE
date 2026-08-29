import sympy as sp
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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

def is_linear(witness):
    """
    Checks if the given witness represents a linear operator.
    """
    if isinstance(witness, sp.MatrixBase) and not witness.free_symbols:
        return True
        
    if callable(witness):
        for dim in range(1, 5):
            try:
                v1 = sp.Matrix([sp.Symbol(f'v1_{i}') for i in range(dim)])
                v2 = sp.Matrix([sp.Symbol(f'v2_{i}') for i in range(dim)])
                c = sp.Symbol('c_lin')
                
                res1 = witness(c * v1 + v2)
                res2 = c * witness(v1) + witness(v2)
                
                if isinstance(res1, (list, tuple)): res1 = sp.Matrix(res1)
                if isinstance(res2, (list, tuple)): res2 = sp.Matrix(res2)
                
                diff = res1 - res2
                if hasattr(diff, 'applyfunc'):
                    diff = diff.applyfunc(sp.simplify)
                else:
                    diff = sp.simplify(diff)
                    
                if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix:
                    return True
                elif diff == 0 or diff == sp.zeros(*diff.shape if hasattr(diff, 'shape') else (1, 1)):
                    return True
                else:
                    return False
            except Exception:
                continue
        return False

    if hasattr(witness, 'free_symbols') and witness.free_symbols:
        syms = list(witness.free_symbols)
        c = sp.Symbol('c_lin')
        v1 = {s: sp.Symbol(f'{s.name}_1') for s in syms}
        v2 = {s: sp.Symbol(f'{s.name}_2') for s in syms}
        
        try:
            expr1 = witness.subs({s: c * v1[s] + v2[s] for s in syms})
            expr2 = c * witness.subs(v1) + witness.subs(v2)
            
            diff = expr1 - expr2
            if hasattr(diff, 'applyfunc'):
                diff = diff.applyfunc(sp.simplify)
            else:
                diff = sp.simplify(diff)
                
            if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix:
                return True
            if diff == 0:
                return True
            return False
        except Exception:
            return False

    if isinstance(witness, sp.Expr) and not witness.free_symbols:
        return witness == 0

    return False

def conditions(witness) -> list[bool]:
    operator = witness
    h1_ok = False
    
    if isinstance(witness, tuple):
        if len(witness) == 2 and isinstance(witness[0], sp.MatrixBase):
            G, T = witness
            operator = T
            try:
                if G.adjoint() != G or G.det() == 0:
                    return [False, False]
            except Exception:
                pass
        else:
            for item in witness:
                if callable(item) or hasattr(item, 'free_symbols') or isinstance(item, sp.MatrixBase):
                    operator = item
                    break
            else:
                try:
                    operator = sp.Matrix(witness)
                except Exception:
                    operator = witness[0] if witness else witness
    elif isinstance(witness, list):
        try:
            operator = sp.Matrix(witness)
        except Exception:
            operator = witness

    try:
        h1_ok = isinstance(operator, sp.MatrixBase) or callable(operator) or hasattr(operator, 'free_symbols')
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q = False
        else:
            linear = is_linear(operator)
            neg_q = not linear
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "¬Q: The adjoint operator (T*)* is not equal to T"
]

N_HYP = 1
NEG_Q_INDEX = 1