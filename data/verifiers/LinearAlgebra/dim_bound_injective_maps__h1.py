import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import z3
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
    "H_1: T is a linear map",
    "H_2: T is injective",
    "¬Q: dim(V) > dim(W)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def _get_prop(obj, names, default=None):
    """Helper to safely extract properties from dictionaries or objects."""
    if isinstance(obj, dict):
        for name in names:
            if name in obj:
                return obj[name]
    else:
        for name in names:
            if hasattr(obj, name):
                val = getattr(obj, name)
                return val() if callable(val) else val
    return default

def conditions(witness):
    h1, h2, neg_q = False, False, False

    try:
        # 1. Try tuple representation: (T, V, W)
        if isinstance(witness, tuple) and len(witness) == 3:
            T, V, W = witness
            
            # Check T
            if hasattr(T, 'cols') and hasattr(T, 'rows') and hasattr(T, 'nullspace'):
                h1 = True
                h2 = len(T.nullspace()) == 0
            else:
                h1 = bool(_get_prop(T, ['is_linear_map', 'is_linear'], True))
                h2 = bool(_get_prop(T, ['is_injective', 'injective'], True))
                
            # Check V and W dimensions
            dim_v = _get_prop(V, ['dim', 'finrank', 'dimension', 'dim_V', 'dim_v'])
            if dim_v is None and hasattr(T, 'cols'): 
                dim_v = T.cols
            
            dim_w = _get_prop(W, ['dim', 'finrank', 'dimension', 'dim_W', 'dim_w'])
            if dim_w is None and hasattr(T, 'rows'): 
                dim_w = T.rows
            
            if dim_v is not None and dim_w is not None:
                neg_q = bool(dim_v > dim_w)
            return [h1, h2, neg_q]

        # 2. Try sympy Matrix directly
        if hasattr(witness, 'cols') and hasattr(witness, 'rows') and hasattr(witness, 'nullspace'):
            h1 = True
            h2 = len(witness.nullspace()) == 0
            neg_q = bool(witness.cols > witness.rows)
            return [h1, h2, neg_q]

        # 3. Try single object or dictionary representation
        h1 = bool(_get_prop(witness, ['is_linear_map', 'is_linear'], False))
        h2 = bool(_get_prop(witness, ['is_injective', 'injective'], False))
        
        dim_v = _get_prop(witness, ['dim_V', 'finrank_V', 'dim_v'])
        if dim_v is None:
            domain = _get_prop(witness, ['domain', 'V'])
            if domain is not None:
                dim_v = _get_prop(domain, ['dim', 'finrank', 'dimension'])

        dim_w = _get_prop(witness, ['dim_W', 'finrank_W', 'dim_w'])
        if dim_w is None:
            codomain = _get_prop(witness, ['codomain', 'W'])
            if codomain is not None:
                dim_w = _get_prop(codomain, ['dim', 'finrank', 'dimension'])
                
        if dim_v is not None and dim_w is not None:
            neg_q = bool(dim_v > dim_w)

    except Exception:
        pass

    return [h1, h2, neg_q]