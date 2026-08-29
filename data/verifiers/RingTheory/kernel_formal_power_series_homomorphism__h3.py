import sympy
from sympy import symbols, Rational, Integer
from sympy.matrices import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        if isinstance(witness, dict) and 'H1' in witness:
            H1 = bool(witness.get('H1', False))
            H2 = bool(witness.get('H2', False))
            neg_Q = bool(witness.get('neg_Q', False))
            return [H1, H2, neg_Q]
            
        if hasattr(witness, 'H1'):
            H1 = bool(getattr(witness, 'H1', False))
            H2 = bool(getattr(witness, 'H2', False))
            neg_Q = bool(getattr(witness, 'neg_Q', False))
            return [H1, H2, neg_Q]
            
        if isinstance(witness, dict):
            elems_R = witness.get('R_elems', [])
            add_R = witness.get('add_R')
            mul_R = witness.get('mul_R')
            elems_S = witness.get('S_elems', [])
            add_S = witness.get('add_S')
            mul_S = witness.get('mul_S')
            f = witness.get('f')
        else:
            elems_R = getattr(witness, 'R_elems', [])
            add_R = getattr(witness, 'add_R', None)
            mul_R = getattr(witness, 'mul_R', None)
            elems_S = getattr(witness, 'S_elems', [])
            add_S = getattr(witness, 'add_S', None)
            mul_S = getattr(witness, 'mul_S', None)
            f = getattr(witness, 'f', None)
            
        if elems_R and elems_S and add_R and mul_R and add_S and mul_S and f:
            H1 = True
            for a in elems_R:
                for b in elems_R:
                    if add_R(a, b) != add_R(b, a): H1 = False
                    if mul_R(a, b) != mul_R(b, a): H1 = False
            for a in elems_S:
                for b in elems_S:
                    if add_S(a, b) != add_S(b, a): H1 = False
                    if mul_S(a, b) != mul_S(b, a): H1 = False
                    
            H2 = True
            for a in elems_R:
                for b in elems_R:
                    if f(add_R(a, b)) != add_S(f(a), f(b)): H2 = False
                    if f(mul_R(a, b)) != mul_S(f(a), f(b)): H2 = False
                    
        neg_Q = False
    except Exception:
        pass

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: f: R to S is a ring homomorphism",
    "not Q: The kernel of the induced formal power series ring homomorphism is not the ideal of formal power series with coefficients in ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2