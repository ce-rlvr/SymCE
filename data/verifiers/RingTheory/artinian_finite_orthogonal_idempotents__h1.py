import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Standard algebra objects
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_zero_elem(x):
    if hasattr(x, 'is_zero') and x.is_zero is not None:
        return bool(x.is_zero)
    try:
        if hasattr(x, 'is_zero_matrix'):
            return bool(x.is_zero_matrix)
    except Exception:
        pass
    try:
        if x == x * 0:
            return True
    except Exception:
        pass
    try:
        if x == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # H_1: S is a set of mutually orthogonal non-zero idempotent elements in R
    h1_ok = False
    try:
        if hasattr(witness, 'sample'):
            elements = witness.sample(15)
        elif isinstance(witness, (list, set, tuple)):
            elements = list(witness)
        else:
            if callable(witness):
                iterable = witness()
            else:
                iterable = iter(witness)
            elements = list(itertools.islice(iterable, 15))
            
        h1_ok = True
        for i, e in enumerate(elements):
            if is_zero_elem(e):
                h1_ok = False
                break
            
            # Check idempotent
            try:
                if e * e != e:
                    if isinstance(e, sympy.Basic) or hasattr(e, 'is_zero_matrix'):
                        diff = e * e - e
                        diff_simp = sympy.simplify(diff)
                        if not is_zero_elem(diff_simp):
                            h1_ok = False
                            break
                    else:
                        h1_ok = False
                        break
            except Exception:
                h1_ok = False
                break
                    
            # Check orthogonal
            for j, f in enumerate(elements):
                if i != j:
                    try:
                        ef = e * f
                        if not is_zero_elem(ef):
                            if isinstance(ef, sympy.Basic) or hasattr(ef, 'is_zero_matrix'):
                                ef_simp = sympy.simplify(ef)
                                if not is_zero_elem(ef_simp):
                                    h1_ok = False
                                    break
                            else:
                                h1_ok = False
                                break
                    except Exception:
                        h1_ok = False
                        break
            if not h1_ok:
                break
    except Exception:
        h1_ok = False

    # neg_Q: The set S is infinite
    neg_q_ok = False
    try:
        if hasattr(witness, 'is_finite'):
            fin = witness.is_finite
            if callable(fin):
                fin = fin()
            if fin is not None:
                neg_q_ok = not fin
            else:
                neg_q_ok = True
        elif isinstance(witness, (list, set, tuple)):
            neg_q_ok = False
        else:
            if hasattr(witness, '__len__'):
                neg_q_ok = False
            else:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: S is a set of mutually orthogonal non-zero idempotent elements in R",
    "¬Q: The set S is infinite"
]

N_HYP = 1
NEG_Q_INDEX = 1