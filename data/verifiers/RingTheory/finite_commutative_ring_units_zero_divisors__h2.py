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

def conditions(witness):
    try:
        R, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: R is a finite ring
    h1 = False
    try:
        if hasattr(R, 'is_finite'):
            h1 = bool(R.is_finite() if callable(R.is_finite) else R.is_finite)
        elif hasattr(R, 'is_FiniteField'):
            h1 = bool(R.is_FiniteField() if callable(R.is_FiniteField) else R.is_FiniteField)
        elif hasattr(R, 'elements'):
            count = 0
            for _ in R.elements:
                count += 1
                if count > 10000:
                    h1 = False
                    break
            else:
                h1 = True
        elif hasattr(R, '__iter__'):
            count = 0
            for _ in R:
                count += 1
                if count > 10000:
                    h1 = False
                    break
            else:
                h1 = True
    except Exception:
        pass

    # H2: R has a multiplicative identity
    h2 = False
    one = None
    try:
        if hasattr(R, 'has_identity'):
            h2 = bool(R.has_identity() if callable(R.has_identity) else R.has_identity)
            if hasattr(R, 'one'):
                one = R.one() if callable(R.one) else R.one
        elif hasattr(R, 'one'):
            one = R.one() if callable(R.one) else R.one
            h2 = (one is not None)
        elif hasattr(R, 'multiplicative_identity'):
            one = R.multiplicative_identity() if callable(R.multiplicative_identity) else R.multiplicative_identity
            h2 = (one is not None)
    except Exception:
        pass

    # H3: x is a non-zero element of R
    h3 = False
    zero = None
    try:
        if hasattr(R, 'zero'):
            zero = R.zero() if callable(R.zero) else R.zero
        elif hasattr(R, 'additive_identity'):
            zero = R.additive_identity() if callable(R.additive_identity) else R.additive_identity
        
        if zero is not None:
            h3 = (x != zero)
            if hasattr(R, 'contains'):
                h3 = h3 and bool(R.contains(x))
            elif hasattr(R, '__contains__'):
                h3 = h3 and bool(x in R)
    except Exception:
        pass

    # Negated Conclusion: x is NEITHER a unit NOR a zero divisor in R
    neg_q = False
    try:
        is_unit = False
        is_zd = False
        
        elements = None
        try:
            if hasattr(R, 'elements'):
                iterator = R.elements
            elif hasattr(R, '__iter__'):
                iterator = R
            else:
                iterator = None
                
            if iterator is not None:
                temp_elements = []
                for i, e in enumerate(iterator):
                    if i > 10000:
                        temp_elements = None
                        break
                    temp_elements.append(e)
                elements = temp_elements
        except Exception:
            pass
            
        def mul(a, b):
            if hasattr(R, 'mul'):
                return R.mul(a, b)
            return a * b

        is_unit_determined = False
        if hasattr(R, 'is_unit'):
            try:
                is_unit = bool(R.is_unit(x) if callable(R.is_unit) else R.is_unit)
                is_unit_determined = True
            except Exception:
                pass
        
        if not is_unit_determined and elements is not None and one is not None:
            for y in elements:
                try:
                    if mul(x, y) == one and mul(y, x) == one:
                        is_unit = True
                        break
                except Exception:
                    pass

        is_zd_determined = False
        if hasattr(R, 'is_zero_divisor'):
            try:
                is_zd = bool(R.is_zero_divisor(x) if callable(R.is_zero_divisor) else R.is_zero_divisor)
                is_zd_determined = True
            except Exception:
                pass
                
        if not is_zd_determined and elements is not None and zero is not None:
            for y in elements:
                if y != zero:
                    try:
                        if mul(x, y) == zero or mul(y, x) == zero:
                            is_zd = True
                            break
                    except Exception:
                        pass
                        
        neg_q = not (is_unit or is_zd)
    except Exception:
        pass

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a finite ring",
    "H_2: R has a multiplicative identity",
    "H_3: x is a non-zero element of R",
    "¬Q: x is neither a unit nor a zero divisor in R"
]

N_HYP = 3
NEG_Q_INDEX = 3