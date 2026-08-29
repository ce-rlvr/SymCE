import sympy
from sympy import symbols, Matrix, eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import math
import functools

# Standard bindings
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

ZZ = sympy.ZZ
QQ = sympy.QQ
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False
    
    # 1. SymPy domains (e.g., ZZ[x], QQ[x, y])
    try:
        if hasattr(witness, 'is_Field'):
            is_field = witness.is_Field
            h1_ok = not is_field
            
            if hasattr(witness, 'domain') and hasattr(witness, 'gens'):
                domain = witness.domain
                gens = witness.gens
                
                if len(gens) >= 1:
                    if hasattr(domain, 'is_Field') and domain.is_Field:
                        if len(gens) == 1:
                            neg_q_ok = False  # F[x] is a Euclidean domain, so it has a USD
                        else:
                            neg_q_ok = True   # F[x, y] has no USD
                    else:
                        neg_q_ok = True       # R[x] has no USD if R is not a field
                return [bool(h1_ok), bool(neg_q_ok)]
            
            if witness == sympy.ZZ:
                neg_q_ok = False
                return [bool(h1_ok), bool(neg_q_ok)]
                
            if witness == sympy.QQ:
                neg_q_ok = False
                return [bool(h1_ok), bool(neg_q_ok)]
    except Exception:
        pass

    # 2. Custom class with explicit methods
    try:
        if hasattr(witness, 'is_field') and hasattr(witness, 'has_usd'):
            is_field = witness.is_field() if callable(witness.is_field) else witness.is_field
            has_usd = witness.has_usd() if callable(witness.has_usd) else witness.has_usd
            return [not is_field, not has_usd]
    except Exception:
        pass

    # 3. Tuple of (elements, add, mul, zero, one) for finite rings
    try:
        if isinstance(witness, tuple) and len(witness) == 5:
            elements, add, mul, zero, one = witness
            if isinstance(elements, (list, tuple, set)):
                elements = list(elements)
                units = []
                for a in elements:
                    for b in elements:
                        if mul(a, b) == one:
                            units.append(a)
                            break
                is_field = (len(units) == len(elements) - 1)
                h1_ok = not is_field
                
                has_usd = False
                for u in elements:
                    if u in units:
                        continue
                    u_is_usd = True
                    multiples = []
                    for r in elements:
                        multiples.append(mul(u, r))
                    for x_elem in elements:
                        if x_elem in multiples:
                            continue
                        found = False
                        for v in units:
                            for m in multiples:
                                if add(m, v) == x_elem:
                                    found = True
                                    break
                            if found:
                                break
                        if not found:
                            u_is_usd = False
                            break
                    if u_is_usd:
                        has_usd = True
                        break
                neg_q_ok = not has_usd
                return [bool(h1_ok), bool(neg_q_ok)]
    except Exception:
        pass

    # 4. List of objects with overloaded operators (+, *, ==) for finite rings
    try:
        if isinstance(witness, (list, tuple, set)) and len(witness) > 1:
            elements = list(witness)
            zero = None
            one = None
            for e in elements:
                if all(e + x_elem == x_elem for x_elem in elements):
                    zero = e
                    break
            for e in elements:
                if all(e * x_elem == x_elem for x_elem in elements):
                    one = e
                    break
            
            if zero is not None and one is not None:
                units = []
                for a in elements:
                    for b in elements:
                        if a * b == one:
                            units.append(a)
                            break
                is_field = (len(units) == len(elements) - 1)
                h1_ok = not is_field
                
                has_usd = False
                for u in elements:
                    if u in units:
                        continue
                    u_is_usd = True
                    multiples = []
                    for r in elements:
                        multiples.append(u * r)
                    for x_elem in elements:
                        if x_elem in multiples:
                            continue
                        found = False
                        for v in units:
                            for m in multiples:
                                if m + v == x_elem:
                                    found = True
                                    break
                            if found:
                                break
                        if not found:
                            u_is_usd = False
                            break
                    if u_is_usd:
                        has_usd = True
                        break
                neg_q_ok = not has_usd
                return [bool(h1_ok), bool(neg_q_ok)]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: R is not a field",
    "¬Q: R does not contain any universal side divisor"
]

N_HYP = 1
NEG_Q_INDEX = 1