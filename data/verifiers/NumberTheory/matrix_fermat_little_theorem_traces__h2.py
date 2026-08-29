import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A, p = witness
        A = sympy.Matrix(A)
    except Exception:
        return [False, False]
        
    # H_1: p is a prime
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    # neg_Q: Tr(A^p) != Tr(A) mod p
    try:
        tr_A = A.trace()
        tr_Ap = (A**p).trace()
        diff = tr_Ap - tr_A
        
        quotient = sympy.simplify(diff / p)
        if quotient.is_integer is True:
            neg_q = False
        elif quotient.is_integer is False:
            neg_q = True
        else:
            try:
                neg_q = bool(diff % p != 0)
            except Exception:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime",
    "¬Q: Tr(A^p) is not congruent to Tr(A) mod p"
]

N_HYP = 1
NEG_Q_INDEX = 1