import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

def conditions(witness):
    try:
        q, m, n = witness
    except Exception:
        return [False, False, False]
        
    # H1: F_q is a finite field with q elements
    try:
        if not isinstance(q, (int, sympy.Integer)):
            h1 = False
        else:
            q_int = int(q)
            if q_int < 2:
                h1 = False
            else:
                factors = sympy.factorint(q_int)
                h1 = (len(factors) == 1)
    except Exception:
        h1 = False

    # H2: F_{q^m} and F_{q^n} are subfields of a common algebraic closure of F_q
    try:
        if not h1:
            h2 = False
        else:
            p = list(sympy.factorint(int(q)).keys())[0]
            
            qm = q**m
            qn = q**n
            
            def is_valid_field_size(val, char):
                if isinstance(val, (int, sympy.Integer)):
                    v = int(val)
                elif isinstance(val, float):
                    v = round(val)
                    if abs(val - v) > 1e-9:
                        return False
                elif isinstance(val, sympy.Rational):
                    if val.q == 1:
                        v = int(val.p)
                    else:
                        return False
                else:
                    try:
                        val_f = float(val)
                        v = round(val_f)
                        if abs(val_f - v) > 1e-9:
                            return False
                    except Exception:
                        return False
                if v < 2:
                    return False
                facs = sympy.factorint(v)
                return len(facs) == 1 and list(facs.keys())[0] == char

            h2 = is_valid_field_size(qm, p) and is_valid_field_size(qn, p)
    except Exception:
        h2 = False

    # Conclusion: The compositum field F_{q^m} F_{q^n} is exactly the field F_{q^{lcm(m,n)}}
    try:
        if not h2:
            q_concl = False
        else:
            p = list(sympy.factorint(int(q)).keys())[0]
            qm = q**m
            qn = q**n
            qm_v = round(float(qm))
            qn_v = round(float(qn))
            
            A = round(math.log(qm_v, p))
            B = round(math.log(qn_v, p))
            compositum_size = p**math.lcm(A, B)
            
            def is_integer(x):
                if isinstance(x, (int, sympy.Integer)):
                    return True
                if isinstance(x, float) and x.is_integer():
                    return True
                if isinstance(x, sympy.Rational) and x.q == 1:
                    return True
                try:
                    if float(x).is_integer():
                        return True
                except Exception:
                    pass
                return False
            
            if not (is_integer(m) and is_integer(n)):
                q_concl = False
            else:
                m_val = int(float(m))
                n_val = int(float(n))
                lcm_mn = math.lcm(m_val, n_val)
                claimed_size = q**lcm_mn
                q_concl = (compositum_size == claimed_size)
    except Exception:
        q_concl = False

    neg_q = not q_concl

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: F_{q^m} and F_{q^n} are subfields of a common algebraic closure of F_q",
    "¬Q: The compositum field F_{q^m} F_{q^n} is not exactly the field F_{q^{lcm(m,n)}}"
]

N_HYP = 2
NEG_Q_INDEX = 2