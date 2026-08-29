import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            if 'is_transcendental' in witness:
                h1 = bool(witness['is_transcendental'])
            elif 'transcendental' in witness:
                h1 = bool(witness['transcendental'])
                
            if 'degree' in witness:
                neg_q = (witness['degree'] < float('inf'))
            elif 'is_infinite_degree' in witness:
                neg_q = not bool(witness['is_infinite_degree'])
            elif 'is_finite_degree' in witness:
                neg_q = bool(witness['is_finite_degree'])
            return [h1, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_transcendental'):
            h1 = bool(witness.is_transcendental)
        elif hasattr(witness, 'transcendental'):
            h1 = bool(witness.transcendental)
        elif hasattr(witness, 'is_algebraic'):
            h1 = not bool(witness.is_algebraic)
    except Exception:
        pass

    try:
        if hasattr(witness, 'degree'):
            deg = witness.degree
            if callable(deg):
                deg = deg()
            neg_q = (deg < float('inf'))
        elif hasattr(witness, 'is_infinite_degree'):
            is_inf = witness.is_infinite_degree
            if callable(is_inf):
                is_inf = is_inf()
            neg_q = not is_inf
        elif hasattr(witness, 'is_finite_degree'):
            is_fin = witness.is_finite_degree
            if callable(is_fin):
                is_fin = is_fin()
            neg_q = bool(is_fin)
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: t in L is an element that is transcendental over K",
    "¬Q: The simple extension K(t) is of finite degree over K"
]

N_HYP = 1
NEG_Q_INDEX = 1