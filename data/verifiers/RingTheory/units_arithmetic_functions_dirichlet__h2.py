import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for potential witness elements
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
    "H_1: K is a field",
    "H_2: f in A",
    "not Q: f is a unit in A iff f(1) != 0 fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Extract K, A, f from the witness
    if isinstance(witness, dict):
        K = witness.get('K')
        A = witness.get('A')
        f = witness.get('f')
    elif isinstance(witness, tuple) and len(witness) == 3:
        K, A, f = witness
    else:
        K = getattr(witness, 'K', None)
        A = getattr(witness, 'A', None)
        f = getattr(witness, 'f', None)

    # H_1: K is a field
    try:
        h1 = False
        if hasattr(K, 'is_Field') and K.is_Field:
            h1 = True
        elif hasattr(K, 'is_field') and K.is_field:
            h1 = True
    except Exception:
        h1 = False

    # H_2: f \in A
    try:
        h2 = False
        if hasattr(A, '__contains__'):
            h2 = bool(f in A)
        elif hasattr(A, 'has'):
            h2 = True
    except Exception:
        h2 = False

    # Negated Conclusion: It is NOT the case that (f is a unit in A iff f(1) != 0)
    try:
        f1 = None
        evaluated = False
        
        # Attempt to evaluate f(1)
        try:
            f1 = f(1)
            evaluated = True
        except Exception:
            pass
            
        if not evaluated:
            try:
                f1 = f[1]
                evaluated = True
            except Exception:
                pass
                
        if not evaluated:
            try:
                syms = list(f.free_symbols)
                if len(syms) >= 1:
                    f1 = f.subs(syms[0], 1)
                else:
                    f1 = f
                evaluated = True
            except Exception:
                pass
                
        if not evaluated:
            neg_q = False
        else:
            # Check if f(1) != 0
            try:
                if hasattr(f1, 'is_zero') and f1.is_zero is not None:
                    f1_not_zero = not f1.is_zero
                else:
                    f1_not_zero = bool(f1 != 0)
            except Exception:
                f1_not_zero = True

            # Check if f is a unit in A
            is_unit = False
            if hasattr(A, 'is_unit'):
                is_unit = bool(A.is_unit(f))
            elif hasattr(f, 'is_unit'):
                if callable(f.is_unit):
                    is_unit = bool(f.is_unit())
                else:
                    is_unit = bool(f.is_unit)
            else:
                try:
                    inv = A.exquo(A.one, f)
                    is_unit = True
                except Exception:
                    try:
                        inv = 1 / f
                        if hasattr(A, '__contains__'):
                            is_unit = bool(inv in A)
                    except Exception:
                        pass
            
            # The conclusion fails if the equivalence does not hold (XOR)
            neg_q = (is_unit != f1_not_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]