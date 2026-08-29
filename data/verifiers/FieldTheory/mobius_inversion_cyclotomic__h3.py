import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from sympy.ntheory import divisors, mobius
from sympy.polys.specialpolys import cyclotomic_poly

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
        if isinstance(witness, tuple) and len(witness) >= 1:
            n = witness[0]
        else:
            n = witness
        h1 = isinstance(n, int) and n >= 1
    except Exception:
        h1 = False

    h2 = True

    try:
        if not h1:
            neg_q = False
        else:
            x = sympy.Symbol('x')
            phi_n = cyclotomic_poly(n, x)
            
            if isinstance(witness, tuple) and len(witness) == 2:
                _, x_val = witness
                
                if hasattr(x_val, 'is_Matrix') and x_val.is_Matrix:
                    I = sympy.eye(x_val.shape[0])
                    coeffs = phi_n.all_coeffs()
                    lhs = sympy.zeros(*x_val.shape)
                    degree = len(coeffs) - 1
                    for i, c in enumerate(coeffs):
                        if degree - i == 0:
                            lhs += c * I
                        else:
                            lhs += c * (x_val**(degree - i))
                    
                    num = I
                    den = I
                    for d in divisors(n):
                        mu = mobius(d)
                        term = x_val**(n // d) - I
                        if mu == 1:
                            num = num * term
                        elif mu == -1:
                            den = den * term
                    
                    if den.det() == 0:
                        neg_q = True
                    else:
                        rhs = den.inv() * num
                        neg_q = bool(lhs != rhs)
                else:
                    lhs = phi_n.subs(x, x_val)
                    
                    num = 1
                    den = 1
                    for d in divisors(n):
                        mu = mobius(d)
                        term = x_val**(n // d) - 1
                        if mu == 1:
                            num *= term
                        elif mu == -1:
                            den *= term
                    
                    try:
                        is_zero = bool(sympy.simplify(den) == 0)
                    except Exception:
                        is_zero = (den == 0)
                        
                    if is_zero:
                        neg_q = True
                    else:
                        rhs = num / den
                        diff = sympy.simplify(lhs - rhs)
                        neg_q = bool(diff != 0)
            else:
                num = 1
                den = 1
                for d in divisors(n):
                    mu = mobius(d)
                    term = x**(n // d) - 1
                    if mu == 1:
                        num *= term
                    elif mu == -1:
                        den *= term
                
                diff = sympy.cancel(phi_n * den - num)
                neg_q = diff != 0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: Phi_n(x) is the n-th cyclotomic polynomial",
    "¬Q: Phi_n(x) != prod_{d|n} (x^{n/d} - 1)^{mu(d)}"
]

N_HYP = 2
NEG_Q_INDEX = 2