import sympy
from sympy import Symbol, limit, oo, Abs

# Top-level setup: named object bindings that the witness expression may reference.
n = Symbol('n', integer=True, nonnegative=True)

CONDITION_LABELS = [
    "H_1: sum a_n x^n has radius of convergence R with 0 < R < oo",
    "¬Q: sum |a_n|^(1/k) x^n does not have radius of convergence R^(1/k)"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample.
    The witness should be a tuple: (exprs, k)
    where `exprs` is a list of sympy expressions in `n` representing the coefficients a_n
    on residue classes modulo M (i.e., a_{m*M + j} = exprs[j](m*M + j)),
    and `k` is a non-zero real number.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            exprs, k = witness
        else:
            return [False, False]
            
        if not isinstance(exprs, (list, tuple)):
            exprs = [exprs]
            
        if len(exprs) == 0:
            return [False, False]
            
        k = sympy.sympify(k)
        if not k.is_real or k == 0:
            return [False, False]
            
        L_j_list = []
        for expr in exprs:
            expr = sympy.sympify(expr)
            if expr == 0:
                L_j = sympy.S.Zero
            else:
                term = Abs(expr)**(1/n)
                L_j = limit(term, n, oo)
            L_j_list.append(L_j)
            
        if any(L == oo for L in L_j_list):
            L = oo
        elif any(L == sympy.nan for L in L_j_list):
            return [False, False]
        else:
            L = max(L_j_list, key=lambda x: float(x))
            
        if L == 0:
            R = oo
            h1 = False
        elif L == oo:
            R = sympy.S.Zero
            h1 = False
        else:
            R = 1 / L
            h1 = True
            
    except Exception:
        return [False, False]

    try:
        L_prime_list = []
        for L_j in L_j_list:
            if L_j == 0:
                if k < 0:
                    L_prime = oo
                else:
                    L_prime = sympy.S.Zero
            elif L_j == oo:
                if k < 0:
                    L_prime = sympy.S.Zero
                else:
                    L_prime = oo
            else:
                L_prime = L_j**(1/k)
            L_prime_list.append(L_prime)
            
        if any(L == oo for L in L_prime_list):
            L_prime_max = oo
        elif any(L == sympy.nan for L in L_prime_list):
            return [h1, False]
        else:
            L_prime_max = max(L_prime_list, key=lambda x: float(x))
            
        if L_prime_max == 0:
            R2 = oo
        elif L_prime_max == oo:
            R2 = sympy.S.Zero
        else:
            R2 = 1 / L_prime_max
            
        R_expected = R**(1/k)
        
        if R2 == oo and R_expected == oo:
            neg_q = False
        elif R2 == oo or R_expected == oo:
            neg_q = True
        else:
            diff = sympy.simplify(R2 - R_expected)
            try:
                neg_q = abs(float(diff)) > 1e-9
            except Exception:
                neg_q = (diff != 0)
                
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]