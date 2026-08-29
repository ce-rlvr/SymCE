import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys import primitive_element

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
    "H_1: a is a rational number that is not the p-th power of any rational number",
    "¬Q: The splitting field of x^p - a over Q does not have degree p(p-1)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        p, a = witness
        p = int(p)
        a = sympy.Rational(a)
    except Exception:
        return [False, False]
        
    # Restrict p to reasonable values to ensure fast execution
    if p < 2 or p > 10:
        return [False, False]
        
    # H_1: a is not the p-th power of any rational number
    try:
        if a == 0:
            h1_ok = False
        else:
            if a < 0 and p % 2 == 0:
                is_pow = False
            else:
                num = abs(a.p)
                den = abs(a.q)
                num_root = sympy.integer_nthroot(num, p)
                den_root = sympy.integer_nthroot(den, p)
                is_pow = num_root[1] and den_root[1]
            h1_ok = not is_pow
    except Exception:
        h1_ok = False
        
    # ¬Q: The splitting field of x^p - a over Q does not have degree p(p-1)
    try:
        if a == 0:
            deg = 1
        elif a > 0:
            gen1 = sympy.root(a, p)
            gen2 = sympy.exp(2 * sympy.I * sympy.pi / p)
            elem, mp = primitive_element([gen1, gen2])
            deg = mp.degree()
        else:
            if p % 2 == 1:
                # For odd p and negative a, we can use the real root to simplify computation
                gen1 = -sympy.root(-a, p)
                gen2 = sympy.exp(2 * sympy.I * sympy.pi / p)
            else:
                # For even p and negative a, roots are complex
                gen1 = sympy.root(-a, p) * sympy.exp(sympy.I * sympy.pi / p)
                gen2 = sympy.exp(2 * sympy.I * sympy.pi / p)
            elem, mp = primitive_element([gen1, gen2])
            deg = mp.degree()
            
        neg_q_ok = bool(deg != p * (p - 1))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]