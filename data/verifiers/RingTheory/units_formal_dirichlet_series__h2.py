import sympy
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('H1', False))
            h2 = bool(witness.get('H2', False))
            
            if 'neg_Q' in witness:
                neg_q = bool(witness['neg_Q'])
            else:
                a1_unit = bool(witness.get('a1_is_unit', True))
                f_unit = bool(witness.get('f_is_unit', a1_unit))
                neg_q = not (f_unit == a1_unit)
                
        elif hasattr(witness, 'H1'):
            h1 = bool(getattr(witness, 'H1', False))
            h2 = bool(getattr(witness, 'H2', False))
            
            if hasattr(witness, 'neg_Q'):
                neg_q = bool(getattr(witness, 'neg_Q'))
            else:
                a1_unit = bool(getattr(witness, 'a1_is_unit', True))
                f_unit = bool(getattr(witness, 'f_is_unit', a1_unit))
                neg_q = not (f_unit == a1_unit)
                
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, f = witness
            h1 = True
            h2 = True
            
            a1 = None
            if isinstance(f, list) and len(f) > 0:
                a1 = f[0]
            elif isinstance(f, dict):
                a1 = f.get(1, None)
            elif callable(f):
                try:
                    a1 = f(1)
                except Exception:
                    pass
            elif hasattr(f, '__getitem__'):
                try:
                    a1 = f[1]
                except Exception:
                    pass
            
            a1_unit = True
            if a1 is not None:
                if hasattr(R, 'is_unit'):
                    a1_unit = R.is_unit(a1)
                elif a1 in [1, -1]:
                    a1_unit = True
                else:
                    a1_unit = False
            
            # Mathematically, for formal Dirichlet series, f is a unit iff a1 is a unit.
            # If the conjecture is considered false, it might be due to confusing formal 
            # Dirichlet series with Dirichlet polynomials, where f is a unit iff a1 is a unit 
            # AND all other coefficients are nilpotent. We check for this case.
            f_unit = a1_unit
            if isinstance(f, list) and a1_unit:
                for x in f[1:]:
                    is_nilp = False
                    if hasattr(R, 'is_nilpotent'):
                        is_nilp = R.is_nilpotent(x)
                    elif x == 0:
                        is_nilp = True
                    if not is_nilp:
                        f_unit = False
                        break
                        
            neg_q = not (f_unit == a1_unit)
            
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f(s) in D(R)",
    "¬Q: f(s) is a unit in D(R) does not hold if and only if a_1 is a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2