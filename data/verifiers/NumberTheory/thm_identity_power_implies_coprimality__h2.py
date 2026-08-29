import sympy
from sympy import I, sqrt, Rational, Integer
from sympy.matrices import eye, zeros, Matrix
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            n = witness.get('n')
            k_search = [witness['k']] if 'k' in witness else range(1, 20)
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                a, n = witness
                k_search = range(1, 20)
            elif len(witness) == 3:
                a, n, k = witness
                k_search = [k]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: n is an integer greater than 1
    try:
        n_val = sympy.sympify(n)
        h1 = False
        if hasattr(n_val, 'is_Matrix') and n_val.is_Matrix:
            h1 = False
        elif isinstance(n_val, sympy.Integer) and n_val > 1:
            h1 = True
        elif hasattr(n_val, 'is_integer') and n_val.is_integer and n_val > 1:
            h1 = True
        else:
            try:
                if float(n_val).is_integer() and float(n_val) > 1:
                    h1 = True
            except Exception:
                pass
    except Exception:
        h1 = False

    # H_2: There exists a positive integer k such that a^k ≡ 1 (mod n)
    h2 = False
    try:
        a_val = sympy.sympify(a)
        for k_val in k_search:
            if not isinstance(k_val, int) or k_val < 1:
                continue
            try:
                if hasattr(a_val, 'is_Matrix') and a_val.is_Matrix:
                    diff = a_val**k_val - sympy.eye(a_val.shape[0])
                else:
                    diff = a_val**k_val - 1
                
                quotient = sympy.simplify(diff / n_val)
                
                if hasattr(quotient, 'is_Matrix') and quotient.is_Matrix:
                    is_int_mat = True
                    for e in quotient:
                        if isinstance(e, sympy.Integer):
                            continue
                        if hasattr(e, 'is_integer') and e.is_integer:
                            continue
                        try:
                            if float(e).is_integer():
                                continue
                        except Exception:
                            pass
                        is_int_mat = False
                        break
                    if is_int_mat:
                        h2 = True
                        break
                else:
                    if isinstance(quotient, sympy.Integer):
                        h2 = True
                        break
                    if hasattr(quotient, 'is_integer') and quotient.is_integer:
                        h2 = True
                        break
                    try:
                        if float(quotient).is_integer():
                            h2 = True
                            break
                    except Exception:
                        pass
            except Exception:
                pass
    except Exception:
        h2 = False

    # ¬Q: a and n are not coprime integers
    try:
        a_val = sympy.sympify(a)
        n_val = sympy.sympify(n)
        
        is_a_int = False
        if hasattr(a_val, 'is_Matrix') and a_val.is_Matrix:
            is_a_int = False
        elif isinstance(a_val, sympy.Integer):
            is_a_int = True
        elif hasattr(a_val, 'is_integer') and a_val.is_integer:
            is_a_int = True
        else:
            try:
                if float(a_val).is_integer():
                    is_a_int = True
            except Exception:
                pass
                
        is_n_int = False
        if hasattr(n_val, 'is_Matrix') and n_val.is_Matrix:
            is_n_int = False
        elif isinstance(n_val, sympy.Integer):
            is_n_int = True
        elif hasattr(n_val, 'is_integer') and n_val.is_integer:
            is_n_int = True
        else:
            try:
                if float(n_val).is_integer():
                    is_n_int = True
            except Exception:
                pass
                
        if is_a_int and is_n_int:
            try:
                g = sympy.gcd(int(a_val), int(n_val))
                q = (g == 1 or g == -1)
            except Exception:
                q = False
        else:
            q = False
            
        neg_q = not q
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "H_2: There exists a positive integer k such that a^k ≡ 1 (mod n)",
    "¬Q: a and n are not coprime integers"
]

N_HYP = 2
NEG_Q_INDEX = 2