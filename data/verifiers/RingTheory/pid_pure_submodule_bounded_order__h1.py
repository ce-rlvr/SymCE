import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z, t

# Standard bindings for potential witness expressions
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
    """
    Checks whether the witness is a valid counterexample to the false conjecture:
    "If M is an R-module, N is a pure submodule of M, and N has bounded order, 
    then N is a direct summand of M."
    """
    h1 = False
    h2 = False
    h3 = False
    neg_q = False

    def check_prop(obj, prop_names, default=False):
        if isinstance(obj, dict):
            for prop in prop_names:
                if prop in obj:
                    return bool(obj[prop])
        for prop in prop_names:
            if hasattr(obj, prop):
                val = getattr(obj, prop)
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        pass
                else:
                    return bool(val)
        return default

    # 1. Try to unpack as a tuple (R, M, N)
    try:
        if isinstance(witness, (list, tuple)) and len(witness) == 3:
            R, M, N = witness
            
            def safe_call(func, *args):
                if callable(func):
                    try:
                        return func(*args)
                    except TypeError:
                        try:
                            return func()
                        except Exception:
                            return False
                return func

            h1_val = False
            if hasattr(M, 'is_module'):
                h1_val = safe_call(M.is_module, R)
            elif hasattr(M, 'is_R_module'):
                h1_val = safe_call(M.is_R_module)
                
            h2_val = False
            if hasattr(N, 'is_pure_submodule'):
                h2_val = safe_call(N.is_pure_submodule, M)
            elif hasattr(N, 'is_pure'):
                h2_val = safe_call(N.is_pure, M)
                
            h3_val = False
            if hasattr(N, 'has_bounded_order'):
                h3_val = safe_call(N.has_bounded_order, R)
            elif hasattr(N, 'is_bounded_order'):
                h3_val = safe_call(N.is_bounded_order)
                
            is_ds = True
            if hasattr(N, 'is_direct_summand'):
                is_ds = safe_call(N.is_direct_summand, M)
                
            h1 = bool(h1_val)
            h2 = bool(h2_val)
            h3 = bool(h3_val)
            neg_q = not bool(is_ds)
            
            if h1 or h2 or h3 or not is_ds:
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 2. Fallback to checking properties directly on the witness object
    try:
        h1 = check_prop(witness, ['is_R_module', 'is_module'])
        h2 = check_prop(witness, ['is_pure_submodule', 'is_pure'])
        h3 = check_prop(witness, ['has_bounded_order', 'is_bounded_order', 'bounded_order'])
        is_ds = check_prop(witness, ['is_direct_summand', 'direct_summand'], default=True)
        neg_q = not is_ds
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "H_2: N is a pure submodule of M",
    "H_3: There exists a non-zero element r in R such that r x = 0 for all x in N",
    "¬Q: N is not a direct summand of M"
]

N_HYP = 3
NEG_Q_INDEX = 3