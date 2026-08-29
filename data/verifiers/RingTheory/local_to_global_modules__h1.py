import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

x, y, z = sympy.symbols('x y z')
QQ = sympy.QQ
ZZ = sympy.ZZ

def _check_attr(witness, names, default=False):
    """Helper to extract boolean properties from mock objects or dicts."""
    if isinstance(witness, dict):
        for name in names:
            if name in witness:
                return bool(witness[name])
    else:
        for name in names:
            if hasattr(witness, name):
                val = getattr(witness, name)
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        pass
                else:
                    return bool(val)
    return default

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    
    Hypotheses:
      H_1: M is an R-module
      H_2: For every maximal ideal m of R, the localized module M_m is the zero module
    Conclusion to falsify:
      Q: M is the zero module
    """
    try:
        # H_1: M is an R-module
        h1 = _check_attr(witness, ['is_R_module', 'is_module', 'is_R_mod'], False)
        
        # H_2: For every maximal ideal m of R, the localized module M_m is the zero module
        h2 = _check_attr(witness, ['localized_zero', 'is_localized_zero', 'all_localized_zero', 'Mm_is_zero', 'localizes_to_zero'], False)
        
        # Q: M is the zero module (we want this to be False, so neg_q is True)
        q = _check_attr(witness, ['is_zero', 'is_zero_module', 'is_trivial'], True)
        neg_q = not q
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "H_2: For every maximal ideal m of R, the localized module M_m is the zero module",
    "¬Q: M is not the zero module"
]

N_HYP = 2
NEG_Q_INDEX = 2