import sympy
from sympy.abc import x, y

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12
Z15 = 15

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) < 2:
            return [False, False, False]
            
        F_obj = witness[0]
        c_obj = witness[1]
        
        n = None
        if isinstance(F_obj, int):
            n = F_obj
        elif hasattr(F_obj, 'is_Integer') and F_obj.is_Integer:
            n = int(F_obj)
        elif hasattr(F_obj, 'characteristic'):
            char = F_obj.characteristic
            if callable(char):
                char = char()
            n = int(char)
        elif hasattr(F_obj, 'mod'):
            n = int(F_obj.mod)
        else:
            try:
                n = int(F_obj)
            except Exception:
                pass
                
        c = None
        try:
            if n == 0:
                c = float(c_obj)
            else:
                c = int(c_obj)
        except Exception:
            pass
            
        if n is None or c is None or n < 0 or n == 1:
            return [False, False, False]
            
        h1 = bool(n != 2)
        
        if n == 0:
            h2 = bool(c != 0)
        else:
            h2 = bool(c % n != 0)
            
        neg_q = False
        if len(witness) >= 4:
            A = sympy.sympify(witness[2])
            B = sympy.sympify(witness[3])
            diff = sympy.expand(A * B - (x**2 + y**2 - c))
            if n == 0:
                is_equal = (diff == 0)
            else:
                poly_diff = sympy.Poly(diff, x, y)
                is_equal = all(int(coeff) % n == 0 for coeff in poly_diff.coeffs())
                
            def is_unit(P):
                P_poly = sympy.Poly(P, x, y)
                if P_poly.is_zero:
                    return False
                
                const_term = sympy.sympify(P).subs({x: 0, y: 0})
                
                if n == 0:
                    if sum(P_poly.degree_list()) > 0:
                        return False
                    return const_term != 0
                else:
                    const_term = int(const_term)
                    if sympy.gcd(const_term, n) != 1:
                        return False
                    
                    primes = sympy.primefactors(n)
                    for monom, coeff in zip(P_poly.monoms(), P_poly.coeffs()):
                        if sum(monom) > 0:
                            if any(int(coeff) % p != 0 for p in primes):
                                return False
                    return True
                    
            if is_equal and not is_unit(A) and not is_unit(B):
                neg_q = True
        else:
            if n > 0:
                neg_q = bool(len(sympy.primefactors(n)) >= 2)
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: The characteristic of F is not equal to 2",
    "H_2: c in F is a non-zero element",
    "¬Q: The polynomial x^2 + y^2 - c is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2