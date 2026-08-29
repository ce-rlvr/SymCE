import math
import itertools
import functools
import z3
import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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

CONDITION_LABELS = [
    "H_1: P is an orthogonal projection operator on V (i.e., P^2 = P and P = P*)",
    "¬Q: The trace of P is not an integer exactly equal to the dimension of the range of P"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    P = witness
    
    # H_1: P^2 == P and P == P*
    h1 = False
    try:
        try:
            is_idempotent = (P**2 == P)
            if not isinstance(is_idempotent, bool):
                is_idempotent = bool(is_idempotent)
        except Exception:
            is_idempotent = False
            
        try:
            is_self_adjoint = (P == P.H)
            if not isinstance(is_self_adjoint, bool):
                is_self_adjoint = bool(is_self_adjoint)
        except Exception:
            try:
                is_self_adjoint = (P == P.T)
                if not isinstance(is_self_adjoint, bool):
                    is_self_adjoint = bool(is_self_adjoint)
            except Exception:
                is_self_adjoint = False
                
        h1 = is_idempotent and is_self_adjoint
    except Exception:
        h1 = False

    # neg_Q: The trace of P is NOT an integer exactly equal to the dimension of the range of P
    neg_q = False
    try:
        try:
            trace_val = P.trace()
        except Exception:
            trace_val = P.trace
            
        try:
            rank_val = P.rank()
        except Exception:
            rank_val = P.rank
            
        is_int = False
        if isinstance(trace_val, int):
            is_int = True
        elif hasattr(trace_val, 'is_integer') and trace_val.is_integer:
            is_int = True
        else:
            try:
                if int(trace_val) == trace_val:
                    is_int = True
            except Exception:
                pass
            if not is_int:
                try:
                    if complex(trace_val).imag == 0 and int(complex(trace_val).real) == trace_val:
                        is_int = True
                except Exception:
                    pass
                
        if is_int:
            try:
                q = (trace_val == rank_val)
                if not isinstance(q, bool):
                    q = bool(q)
            except Exception:
                q = False
        else:
            q = False
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]