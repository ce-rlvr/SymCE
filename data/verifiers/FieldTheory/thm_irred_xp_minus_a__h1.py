import sympy
from sympy import Symbol, Poly, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.domains import Domain

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: a is an element of F",
    "H_2: The element a is not a p-th power of any element in F",
    "¬Q: The polynomial x^p - a is reducible over F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Parse witness
        if len(witness) == 2:
            p, a = witness
            domain = 'QQ'
        elif len(witness) == 3:
            if isinstance(witness[2], (str, Domain)):
                p, a, domain = witness
            else:
                domain, p, a = witness
        else:
            return [False, False, False]
            
        if not (isinstance(p, (int, sympy.Integer)) and p > 0):
            return [False, False, False]
            
        p = int(p)
        a = sympy.S(a)
        x = Symbol('x')
        
        # H_1: a in F
        try:
            poly = Poly(x**p - a, x, domain=domain)
            if domain == 'QQ' or str(domain) == 'QQ':
                h1 = a.is_rational
                if h1 is None:
                    h1 = False
            else:
                h1 = True
        except Exception:
            h1 = False
            
        # H_2: a is not a p-th power in F
        # This is equivalent to x^p - a having no linear factor over F
        try:
            factors = poly.factor_list()[1]
            has_linear = any(f.degree() == 1 for f, mult in factors)
            h2 = not has_linear
        except Exception:
            h2 = False
            
        # ¬Q: x^p - a is reducible over F
        try:
            is_irreducible = (len(factors) == 1 and factors[0][1] == 1)
            neg_q = not is_irreducible
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]