import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
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
    h1 = False
    q = True
    
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_right_artinian', False))
            if 'center_of_quotient_is_product_of_fields' in witness:
                q = bool(witness['center_of_quotient_is_product_of_fields'])
            elif 'is_isomorphic_to_finite_direct_product_of_fields' in witness:
                q = bool(witness['is_isomorphic_to_finite_direct_product_of_fields'])
        except Exception:
            pass
        return [h1, not q]

    try:
        if hasattr(witness, 'is_right_artinian'):
            attr = getattr(witness, 'is_right_artinian')
            h1 = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'is_artinian'):
            attr = getattr(witness, 'is_artinian')
            h1 = bool(attr() if callable(attr) else attr)
    except Exception:
        pass

    try:
        if hasattr(witness, 'center_of_quotient_is_product_of_fields'):
            attr = getattr(witness, 'center_of_quotient_is_product_of_fields')
            q = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'center_of_semisimple_quotient_is_product_of_fields'):
            attr = getattr(witness, 'center_of_semisimple_quotient_is_product_of_fields')
            q = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'quotient_by_jacobson_radical'):
            quot = witness.quotient_by_jacobson_radical()
            if hasattr(quot, 'center'):
                cent = quot.center()
                if hasattr(cent, 'is_isomorphic_to_finite_direct_product_of_fields'):
                    attr = getattr(cent, 'is_isomorphic_to_finite_direct_product_of_fields')
                    q = bool(attr() if callable(attr) else attr)
                elif hasattr(cent, 'is_product_of_fields'):
                    attr = getattr(cent, 'is_product_of_fields')
                    q = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'quotient_ring'):
            quot = witness.quotient_ring() if callable(witness.quotient_ring) else witness.quotient_ring
            if hasattr(quot, 'center'):
                cent = quot.center() if callable(quot.center) else quot.center
                if hasattr(cent, 'is_isomorphic_to_finite_direct_product_of_fields'):
                    attr = getattr(cent, 'is_isomorphic_to_finite_direct_product_of_fields')
                    q = bool(attr() if callable(attr) else attr)
    except Exception:
        pass

    return [h1, not q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: The center of the quotient ring R/J(R) is NOT isomorphic to a finite direct product of fields"
]

N_HYP = 1
NEG_Q_INDEX = 1