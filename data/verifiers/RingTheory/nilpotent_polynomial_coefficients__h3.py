import sympy
from sympy import Poly, Symbol
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

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
    "H_1: R is a commutative ring",
    "H_2: f(x) is a polynomial over R",
    "¬Q: Not every coefficient of f(x) is a nilpotent element in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            return [False, False, False]
            
        if isinstance(witness, Poly):
            poly = witness
        else:
            poly = Poly(witness)
            
        h1 = True
        h2 = True
        
        domain = poly.domain
        all_nilpotent = True
        
        is_integral = getattr(domain, 'is_IntegralDomain', False)
        if str(domain) in ['ZZ', 'QQ', 'RR', 'CC']:
            is_integral = True
            
        for c in poly.coeffs():
            if c == domain.zero:
                continue
                
            if is_integral:
                all_nilpotent = False
                break
                
            is_nilp = False
            p = c
            for _ in range(100):
                p = p * c
                if p == domain.zero:
                    is_nilp = True
                    break
            if not is_nilp:
                all_nilpotent = False
                break
                
        neg_q = not all_nilpotent
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]