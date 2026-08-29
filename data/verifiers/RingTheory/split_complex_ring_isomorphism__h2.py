import sympy
from sympy import ZZ, QQ
import math

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, int):
            if witness >= 2:
                h1 = True
                neg_q = (witness % 2 == 0)
            elif witness == 0:
                h1 = True
                neg_q = True
        elif isinstance(witness, str):
            if witness == 'ZZ':
                h1 = True
                neg_q = True
            elif witness == 'QQ':
                h1 = True
                neg_q = False
        elif hasattr(witness, 'is_IntegerRing') and witness.is_IntegerRing:
            h1 = True
            neg_q = True
        elif hasattr(witness, 'is_RationalField') and witness.is_RationalField:
            h1 = True
            neg_q = False
        elif hasattr(witness, 'one') and hasattr(witness, 'zero'):
            h1 = True
            try:
                one = witness.one
                two = one + one
                if two == witness.zero:
                    neg_q = True
                elif hasattr(witness, 'exquo'):
                    witness.exquo(one, two)
                    neg_q = False
                else:
                    neg_q = True
            except Exception:
                neg_q = True
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "not Q: R polynomial ring modulo x^2 - 1 is not isomorphic as an R-algebra to R x R"
]

N_HYP = 1
NEG_Q_INDEX = 1