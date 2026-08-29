import sympy
from sympy import Symbol, QQ, RR, CC
from functools import reduce

CONDITION_LABELS = [
    "H_1: F is a field of characteristic zero",
    "¬Q: The polynomial x^n - 1 is not equal to the product of the cyclotomic polynomials Phi_d(x) over all positive integers d that divide n"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # The witness can be a tuple (F, n) or just n (in which case we assume F = QQ)
        if isinstance(witness, tuple) and len(witness) == 2:
            F, n = witness
        else:
            F, n = QQ, witness
    except Exception:
        return [False, False]

    h1 = False
    try:
        if F in (QQ, RR, CC):
            h1 = True
        elif hasattr(F, 'is_Field') and F.is_Field:
            char = getattr(F, 'characteristic', None)
            if callable(char):
                h1 = (char() == 0)
            elif char is not None:
                h1 = (char == 0)
    except Exception:
        pass

    neg_q = False
    try:
        x = Symbol('x')
        
        # Check if n is a real number and an integer
        try:
            n_float = float(n)
            is_int = (int(n_float) == n_float)
        except Exception:
            # If n cannot be evaluated as a real number, we cannot verify the conclusion fails
            return [h1, False]
            
        if not is_int:
            # If n is not an integer, the set of positive integer divisors is undefined/empty
            neg_q = True
        elif n_float == 0:
            # If n is 0, there are infinitely many positive integer divisors, product is undefined
            neg_q = True
        else:
            n_int = int(n_float)
            n_abs = abs(n_int)
            
            # Find all positive integers d that divide n
            divisors = [d for d in range(1, n_abs + 1) if n_abs % d == 0]
            
            if not divisors:
                poly_prod = 1
            else:
                poly_prod = reduce(lambda a, b: a * b, [sympy.cyclotomic_poly(d, x) for d in divisors])
                
            expr = x**n_int - 1
            
            # Check if x^n - 1 is equal to the product of the cyclotomic polynomials
            diff = sympy.expand(expr - poly_prod)
            if diff != 0:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]