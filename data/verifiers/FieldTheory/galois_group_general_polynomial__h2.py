import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Poly, sqrt, Symbol, Expr
from sympy.abc import x, y, z, t, u, v

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

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: E is the field of rational functions",
    "H_3: f(x) is a polynomial with coefficients in E",
    "H_4: L is the splitting field of f(x) over E",
    "not_Q: The Galois group is not isomorphic to S_n"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    from sympy.abc import x as default_x
    from sympy import Poly
    
    if isinstance(witness, (tuple, list)) and len(witness) >= 1:
        f_expr = witness[0]
        var = witness[1] if len(witness) > 1 and isinstance(witness[1], sympy.Symbol) else default_x
    else:
        f_expr = witness
        var = default_x
        
    try:
        p = Poly(f_expr, var)
        n = p.degree()
        is_poly = (n >= 1)
    except Exception:
        is_poly = False
        n = 0

    h1 = is_poly
    h2 = is_poly
    
    try:
        h3 = is_poly and p.LC() == 1
    except Exception:
        h3 = False
        
    h4 = is_poly
    
    neg_q = False
    if is_poly and h3:
        if n < 2:
            neg_q = False
        else:
            try:
                if not p.is_irreducible:
                    neg_q = True
                else:
                    disc = p.discriminant()
                    
                    def is_perfect_square(expr):
                        try:
                            if expr.is_number:
                                import sympy
                                return sympy.sqrt(expr).is_rational == True
                            
                            num, den = sympy.cancel(expr).as_numer_denom()
                            
                            def check_poly(p_expr):
                                if p_expr == 1: return True
                                import sympy
                                factors = sympy.sqf_list(p_expr)
                                const = factors[0]
                                if not (sympy.sqrt(const).is_rational == True):
                                    return False
                                for f, m in factors[1]:
                                    if m % 2 != 0:
                                        return False
                                return True
                                
                            return check_poly(num) and check_poly(den)
                        except Exception:
                            return False
                            
                    if is_perfect_square(disc):
                        neg_q = True
                    else:
                        non_zero_coeffs = [k for k in range(n) if p.nth(k) != 0]
                        if len(non_zero_coeffs) == 1 and non_zero_coeffs[0] == 0 and n >= 4:
                            neg_q = True
                        elif n == 4:
                            a = p.nth(3)
                            b = p.nth(2)
                            c = p.nth(1)
                            d = p.nth(0)
                            import sympy
                            y_sym = sympy.Symbol('y')
                            resolvent = y_sym**3 - b*y_sym**2 + (a*c - 4*d)*y_sym - a**2*d + 4*b*d - c**2
                            res_p = Poly(resolvent, y_sym, domain=p.domain)
                            if not res_p.is_irreducible:
                                neg_q = True
            except Exception:
                neg_q = False
                
    return [h1, h2, h3, h4, neg_q]