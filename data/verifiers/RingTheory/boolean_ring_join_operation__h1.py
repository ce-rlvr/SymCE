import sympy
from sympy import Matrix, eye, zeros
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        elements = list(witness)
        if len(elements) == 0:
            return [False, False]
            
        # H_1: For any x, y in R, define a binary operation vee by x vee y = x + y + xy
        # We check that R is closed under this operation, meaning it is a valid binary operation on R.
        h1 = True
        for a in elements:
            for b in elements:
                val = a + b + a * b
                found = False
                for e in elements:
                    if val == e:
                        found = True
                        break
                if not found:
                    h1 = False
                    break
            if not h1:
                break
                
        # Conclusion: vee is associative, commutative, and idempotent
        associative = True
        commutative = True
        idempotent = True
        
        for a in elements:
            if (a + a + a * a) != a:
                idempotent = False
                break
                
        for a in elements:
            for b in elements:
                if (a + b + a * b) != (b + a + b * a):
                    commutative = False
                    break
            if not commutative:
                break
                
        for a in elements:
            for b in elements:
                for c in elements:
                    ab = a + b + a * b
                    bc = b + c + b * c
                    left = ab + c + ab * c
                    right = a + bc + a * bc
                    if left != right:
                        associative = False
                        break
                if not associative:
                    break
            if not associative:
                break
                
        neg_q = not (associative and commutative and idempotent)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: For any x, y in R, define a binary operation vee by x vee y = x + y + xy",
    "¬Q: The operation vee is not associative, commutative, and idempotent on R"
]

N_HYP = 1
NEG_Q_INDEX = 1