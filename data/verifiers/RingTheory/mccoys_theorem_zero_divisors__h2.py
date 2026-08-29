import sympy
from sympy import Poly, Expr, Symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer

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

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (int, float)):
            witness = sympy.sympify(witness)
            
        if isinstance(witness, Poly):
            f = witness
        elif isinstance(witness, Expr):
            if not witness.free_symbols:
                f = Poly(witness, x)
            else:
                f = Poly(witness)
        else:
            return [False, False, False]
            
        # H1: R is a commutative ring
        # SymPy's Poly domains are inherently commutative rings.
        h1_ok = True
        
        # H2: f(x) is not the zero polynomial
        h2_ok = not f.is_zero
        
        # neg_Q: There does NOT exist a non-zero c in R such that c f(x) = 0
        domain = f.domain
        is_integral_domain = (
            getattr(domain, 'is_ZZ', False) or
            getattr(domain, 'is_QQ', False) or
            getattr(domain, 'is_RR', False) or
            getattr(domain, 'is_CC', False) or
            getattr(domain, 'is_Field', False)
        )
        
        if is_integral_domain:
            # In an integral domain, c * f(x) == 0 implies c == 0 or f(x) == 0.
            # If f(x) != 0, c must be 0. So no non-zero c exists -> neg_Q is True.
            # If f(x) == 0, any non-zero c works -> neg_Q is False.
            neg_q_ok = not f.is_zero
        else:
            # For finite rings or other domains with zero divisors, we would need 
            # to check for elements that annihilate all coefficients of f.
            # As a safe fallback for unknown domains, we return False.
            neg_q_ok = False
            
        return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f(x) is not the zero polynomial",
    "¬Q: There does not exist a non-zero element c in R such that c f(x) = 0"
]

N_HYP = 2
NEG_Q_INDEX = 2