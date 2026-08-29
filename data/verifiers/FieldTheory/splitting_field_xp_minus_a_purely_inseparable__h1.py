import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, integer_nthroot, Poly
from sympy.abc import x

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

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        h2 = False
        neg_q = False
        
        if isinstance(witness, tuple):
            if len(witness) == 2:
                p, a = witness
            elif len(witness) == 3:
                _, p, a = witness
            else:
                return [False, False, False]
        else:
            poly = Poly(witness)
            gen = poly.gen
            p = poly.degree()
            if poly.coeff_monomial(gen**p) != 1:
                return [False, False, False]
            for i in range(1, p):
                if poly.coeff_monomial(gen**i) != 0:
                    return [False, False, False]
            a = -poly.coeff_monomial(1)
            
        p = int(p)
        if not sympy.isprime(p):
            return [False, False, False]
            
        a = Rational(a)
        
        num_root, num_exact = integer_nthroot(abs(a.p), p)
        den_root, den_exact = integer_nthroot(a.q, p)
        
        is_pth_power = False
        if num_exact and den_exact:
            if p % 2 == 1:
                is_pth_power = True
            else:
                if a.p >= 0:
                    is_pth_power = True
                    
        h1 = not is_pth_power
        
        # H2 is definitional for the witness context (L is the splitting field)
        h2 = True
        
        # Over Q (characteristic 0), no algebraic extension of degree > 1 is purely inseparable.
        # Since h1 ensures x^p - a has no root in Q, the splitting field has degree > 1.
        # Thus L/K is not purely inseparable.
        neg_q = True
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: a in K and there is no b in K with b^p = a",
    "H_2: L is the splitting field of x^p - a over K",
    "¬Q: L/K is not a purely inseparable extension of degree p"
]

N_HYP = 2
NEG_Q_INDEX = 2