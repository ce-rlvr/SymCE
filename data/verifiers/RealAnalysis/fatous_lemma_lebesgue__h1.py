import sympy
from sympy import oo, limit, integrate, Sum
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: {f_n} is a sequence of measurable functions on X",
    "H_2: f_n(x) >= 0 for all n and for mu-almost all x in X",
    "¬Q: int_X (liminf f_n) dmu > liminf int_X f_n dmu"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_val(witness, key, default=None):
    if isinstance(witness, dict):
        if key in witness:
            return witness[key]
        if default is not None:
            return default
        raise KeyError(key)
    if hasattr(witness, key):
        return getattr(witness, key)
    if default is not None:
        return default
    raise AttributeError(key)

def conditions(witness):
    try:
        f = get_val(witness, 'f')
        x = get_val(witness, 'x')
        n = get_val(witness, 'n')
        domain = get_val(witness, 'domain')
        measure = get_val(witness, 'measure', 'lebesgue')
        
        a, b = domain
        
        # H1: {f_n} is a sequence of measurable functions
        # Any valid sympy expression provided as a witness is measurable.
        h1 = True
        
        # H2: f_n(x) >= 0 for all n and for mu-almost all x in X
        h2 = True
        try:
            if measure == 'discrete':
                try:
                    if b == oo:
                        a_f = int(float(a))
                        x_vals = [a_f, a_f+1, a_f+2, a_f+10, a_f+100]
                    else:
                        a_f = int(float(a))
                        b_f = int(float(b))
                        x_vals = list(range(a_f, b_f + 1))
                except Exception:
                    x_vals = [1, 2, 3, 10, 100]
            else:
                if a == oo or a == -oo or b == oo or b == -oo:
                    if a == -oo and b == oo:
                        x_vals = [-100, -10, -1, -0.5, 0, 0.5, 1, 10, 100]
                    elif a == -oo:
                        try:
                            b_f = float(b)
                            x_vals = [b_f-100, b_f-10, b_f-1, b_f-0.5, b_f]
                        except Exception:
                            x_vals = [-100, -10, -1, 0]
                    elif b == oo:
                        try:
                            a_f = float(a)
                            x_vals = [a_f, a_f+0.5, a_f+1, a_f+10, a_f+100]
                        except Exception:
                            x_vals = [0, 1, 10, 100]
                else:
                    try:
                        a_f = float(a)
                        b_f = float(b)
                        x_vals = [a_f + (b_f - a_f) * i / 10.0 for i in range(11)]
                    except Exception:
                        x_vals = [0, 1]
                        
            for n_val in [1, 2, 5, 10, 100]:
                for x_val in x_vals:
                    val = f.subs({n: n_val, x: x_val}).evalf()
                    if val.is_real and val < -1e-7:
                        h2 = False
                        break
                if not h2:
                    break
        except Exception:
            h2 = False

        # neg_Q: int_X (liminf f_n) dmu > liminf int_X f_n dmu
        try:
            lim_f = limit(f, n, oo)
            
            if measure == 'discrete':
                lhs_val = Sum(lim_f, (x, a, b)).doit()
                int_f = Sum(f, (x, a, b)).doit()
            else:
                lhs_val = integrate(lim_f, (x, a, b))
                int_f = integrate(f, (x, a, b))
                
            rhs_val = limit(int_f, n, oo)
            
            def to_extended_float(val):
                if val == oo:
                    return float('inf')
                elif val == -oo:
                    return float('-inf')
                else:
                    return float(val.evalf())

            lhs_f = to_extended_float(lhs_val)
            rhs_f = to_extended_float(rhs_val)
            
            neg_q = lhs_f > rhs_f + 1e-7
        except Exception:
            neg_q = False
            
    except Exception:
        return [False, False, False]
        
    return [h1, h2, neg_q]