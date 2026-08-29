import sympy
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices
import math
import itertools
import functools

# Top-level setup
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
V4 = named_groups.DihedralGroup(2)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    # Handle SymPy algebraic fields over QQ as a special case
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, E = witness
            if F == sympy.QQ and isinstance(E, sympy.polys.domains.AlgebraicField):
                return [True, True, False]
    except Exception:
        pass

    # H_1: F is a subfield of E.
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_subfield', True))
        else:
            h1 = bool(getattr(witness, 'is_subfield', True))
    except Exception:
        h1 = False

    # H_2: The degree of the field extension E over F is finite.
    try:
        if isinstance(witness, dict):
            if 'is_finite_degree' in witness:
                h2 = bool(witness['is_finite_degree'])
            elif 'degree' in witness:
                h2 = witness['degree'] < float('inf')
            else:
                h2 = True
        else:
            if hasattr(witness, 'is_finite_degree'):
                h2 = bool(witness.is_finite_degree)
            elif hasattr(witness, 'degree'):
                h2 = witness.degree < float('inf')
            else:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: E is simple iff the number of intermediate fields is finite (Negated)
    # The conclusion fails if the truth values of "is_simple" and "finite_intermediate_fields" differ.
    try:
        if isinstance(witness, dict):
            is_simple = bool(witness['is_simple'])
            fin_int = bool(witness['finite_intermediate_fields'])
            neg_q = (is_simple != fin_int)
        else:
            is_simple = bool(witness.is_simple)
            fin_int = bool(witness.finite_intermediate_fields)
            neg_q = (is_simple != fin_int)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a subfield of E",
    "H_2: The degree of the field extension E over F is finite",
    "¬Q: E is simple XOR there are finitely many intermediate fields"
]

N_HYP = 2
NEG_Q_INDEX = 2