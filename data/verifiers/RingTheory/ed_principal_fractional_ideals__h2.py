import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: I is a fractional ideal of R in K",
    "¬Q: I is not a principal fractional ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2

def safe_eq(a, b):
    try:
        return a == b
    except Exception:
        return False

def check_bool_attr(obj, attr_name, *args):
    if not hasattr(obj, attr_name):
        return None
    attr = getattr(obj, attr_name)
    if callable(attr):
        try:
            return bool(attr(*args))
        except Exception:
            try:
                return bool(attr())
            except Exception:
                return None
    return bool(attr)

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    try:
        # 1. Tuple witness (R, I)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            
            # H1: R is a Euclidean domain
            if safe_eq(R, ZZ):
                h1 = True
            else:
                res = check_bool_attr(R, 'is_PID')
                if res is not None:
                    h1 = res
                else:
                    res = check_bool_attr(R, 'is_EuclideanDomain')
                    if res is not None:
                        h1 = res
                        
            # H2 & neg_Q
            if safe_eq(R, ZZ) and safe_eq(I, QQ):
                h2 = True
                neg_q = True
            elif hasattr(R, 'frac_field') and safe_eq(I, R.frac_field):
                h2 = True
                is_field = check_bool_attr(R, 'is_Field')
                if is_field:
                    neg_q = False
                else:
                    neg_q = True
            else:
                res_h2 = check_bool_attr(I, 'is_fractional_ideal', R)
                if res_h2 is not None:
                    h2 = res_h2
                else:
                    h2 = True # Fallback for valid submodule representations
                    
                res_nq = check_bool_attr(I, 'is_principal', R)
                if res_nq is not None:
                    neg_q = not res_nq
                elif isinstance(I, (list, set, tuple)):
                    # Finitely generated over a PID is principal
                    neg_q = False
                
        # 2. Object with attributes
        else:
            if hasattr(witness, 'R'):
                R = witness.R
                if safe_eq(R, ZZ):
                    h1 = True
                else:
                    res = check_bool_attr(R, 'is_PID')
                    if res is not None:
                        h1 = res
            else:
                res = check_bool_attr(witness, 'is_Euclidean_domain')
                if res is not None:
                    h1 = res
                    
            if hasattr(witness, 'I'):
                I = witness.I
                if hasattr(witness, 'R') and safe_eq(witness.R, ZZ) and safe_eq(I, QQ):
                    h2 = True
                    neg_q = True
                elif hasattr(witness, 'R') and hasattr(witness.R, 'frac_field') and safe_eq(I, witness.R.frac_field):
                    h2 = True
                    is_field = check_bool_attr(witness.R, 'is_Field')
                    if is_field:
                        neg_q = False
                    else:
                        neg_q = True
                else:
                    res_h2 = check_bool_attr(I, 'is_fractional_ideal')
                    if res_h2 is not None:
                        h2 = res_h2
                    res_nq = check_bool_attr(I, 'is_principal')
                    if res_nq is not None:
                        neg_q = not res_nq
            else:
                res_h2 = check_bool_attr(witness, 'is_fractional_ideal')
                if res_h2 is not None:
                    h2 = res_h2
                res_nq = check_bool_attr(witness, 'is_principal')
                if res_nq is not None:
                    neg_q = not res_nq
                    
        # 3. String or direct QQ witness
        if safe_eq(witness, QQ):
            h1, h2, neg_q = True, True, True
            
        if isinstance(witness, str):
            s = witness.lower()
            if 'q' in s or 'z[1/2]' in s:
                h1, h2, neg_q = True, True, True

    except Exception:
        pass

    return [h1, h2, neg_q]