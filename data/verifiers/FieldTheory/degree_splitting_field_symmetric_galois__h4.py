import sympy
from sympy import Poly
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

x = sympy.Symbol('x')

def is_square(val):
    if isinstance(val, sympy.Rational):
        p, q = val.p, val.q
        if p < 0 or q < 0:
            return False
        return math.isqrt(p)**2 == p and math.isqrt(q)**2 == q
    elif isinstance(val, (int, sympy.Integer)):
        val = int(val)
        if val < 0:
            return False
        return math.isqrt(val)**2 == val
    return False

def get_splitting_field_degree(f):
    n = f.degree()
    gen = f.gen
    
    if f.domain.is_FiniteField:
        factors = f.factor_list()[1]
        l = 1
        for fac, mult in factors:
            l = math.lcm(l, fac.degree())
        return l
        
    if f.domain.is_RationalField or f.domain.is_IntegerRing:
        factors = f.factor_list()[1]
        
        core_factors = []
        for fac, mult in factors:
            if fac.degree() > 1:
                core_factors.append(fac)
                
        if not core_factors:
            return 1
            
        if len(core_factors) == 1:
            core = core_factors[0]
            d = core.degree()
            if d == 2:
                return 2
            if d == 3:
                disc = core.discriminant()
                if is_square(disc):
                    return 3
                else:
                    return 6
            if d == 4:
                c_monic = core.monic().all_coeffs()
                a, b, c, d_coeff = c_monic[1], c_monic[2], c_monic[3], c_monic[4]
                y = sympy.Symbol('y')
                R = Poly(y**3 - b*y**2 + (a*c - 4*d_coeff)*y - a**2*d_coeff + 4*b*d_coeff - c**2, y, domain=core.domain)
                R_factors = R.factor_list()[1]
                if len(R_factors) == 3:
                    return 4
                elif len(R_factors) == 2:
                    return 8
                else:
                    disc = core.discriminant()
                    if is_square(disc):
                        return 12
                    else:
                        return 24
                        
        if len(core_factors) == 2:
            d1 = core_factors[0].degree()
            d2 = core_factors[1].degree()
            if d1 == 2 and d2 == 2:
                disc1 = core_factors[0].discriminant()
                disc2 = core_factors[1].discriminant()
                if is_square(disc1 * disc2):
                    return 2
                else:
                    return 4

        for k in range(1, 100):
            if f.monic() == Poly(sympy.cyclotomic_poly(k, gen), gen, domain=f.domain):
                return sympy.totient(k)

    return None

def conditions(witness):
    try:
        if isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness, x)
    except Exception:
        return [False, False, False, False]
        
    try:
        if f.domain.is_IntegerRing:
            f = f.set_domain(sympy.QQ)
        is_field = f.domain.is_Field
        h1_ok = bool(is_field)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = bool(f.is_sqf)
    except Exception:
        h2_ok = False
        
    h3_ok = True
    
    try:
        n = f.degree()
        deg_E_F = get_splitting_field_degree(f)
        if deg_E_F is None:
            neg_q_ok = False
        else:
            neg_q_ok = bool(deg_E_F != math.factorial(n))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a separable polynomial over F of degree n",
    "H_3: E is the splitting field of f over F",
    "not Q: The degree of the extension E over F is not equal to n!"
]

N_HYP = 3
NEG_Q_INDEX = 3