import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, PermutationGroup
from sympy import eye, zeros

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
    x = sympy.Symbol('x')
    f_target = x**4 + x + 1
    
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            f, G = witness
            try:
                h1 = bool(sympy.simplify(f - f_target) == 0)
            except Exception:
                h1 = False
            try:
                neg_q = not G.is_isomorphic(S4)
            except Exception:
                neg_q = False
                
        elif hasattr(witness, 'is_isomorphic'):
            h1 = True
            try:
                neg_q = not witness.is_isomorphic(S4)
            except Exception:
                neg_q = False
                
        else:
            try:
                h1 = bool(sympy.simplify(witness - f_target) == 0)
            except Exception:
                h1 = False
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) = x^4+x+1 is a polynomial over Q",
    "¬Q: Gal(K/Q) is not isomorphic to S4"
]

N_HYP = 1
NEG_Q_INDEX = 1