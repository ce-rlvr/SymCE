import sympy
from sympy.abc import x, y

QQ = sympy.QQ
ZZ = sympy.ZZ

CONDITION_LABELS = [
    "H_1: There is no element a in K such that a^2 + 1 = 0",
    "not Q: The polynomial x^2 + y^2 is reducible"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        n = None
        if isinstance(witness, int):
            n = abs(witness)
        elif isinstance(witness, sympy.Integer):
            n = abs(int(witness))
        elif hasattr(witness, 'mod') and isinstance(witness.mod, (int, sympy.Integer)):
            n = abs(int(witness.mod))
        elif hasattr(witness, 'n') and isinstance(witness.n, (int, sympy.Integer)):
            n = abs(int(witness.n))
            
        if n is not None:
            if n <= 1:
                return [False, False]
            
            try:
                factors = sympy.factorint(n)
            except Exception:
                return [False, False]
                
            has_solution = (n % 4 != 0) and all(p % 4 == 1 for p in factors if p != 2)
            h1 = not has_solution
            
            if len(factors) > 1:
                neg_q = True
            else:
                p = list(factors.keys())[0]
                if p % 4 == 1 or n == 2:
                    neg_q = True
                else:
                    neg_q = False
                    
            return [h1, neg_q]
            
        if isinstance(witness, sympy.polys.domains.Domain):
            try:
                if witness in (sympy.QQ, sympy.ZZ):
                    return [True, False]
                roots = sympy.roots(x**2 + 1, x, domain=witness)
                h1 = len(roots) == 0
                neg_q = len(roots) > 0
                return [h1, neg_q]
            except Exception:
                pass
                
        return [False, False]
    except Exception:
        return [False, False]