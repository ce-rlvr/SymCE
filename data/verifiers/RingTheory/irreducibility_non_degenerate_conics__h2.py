import sympy as sp
from sympy import Matrix
from sympy.ntheory import isprime

x, y = sp.symbols('x y')

def conditions(witness) -> list[bool]:
    char = 0
    f = None
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                char_info, f = witness
                if isinstance(char_info, int):
                    char = char_info
                elif hasattr(char_info, 'characteristic'):
                    char = char_info.characteristic()
        else:
            f = witness
            if hasattr(f, 'domain'):
                char = f.domain.characteristic()
                f = f.as_expr()
        
        if isinstance(f, str):
            f = sp.sympify(f)
    except Exception:
        pass

    try:
        if char == 0:
            h1 = True
        else:
            h1 = isprime(char) and char != 2
    except Exception:
        h1 = False

    try:
        poly = sp.Poly(f, x, y)
        a = poly.coeff_monomial(x**2)
        b = poly.coeff_monomial(x*y)
        c = poly.coeff_monomial(y**2)
        d = poly.coeff_monomial(x)
        e = poly.coeff_monomial(y)
        g = poly.coeff_monomial(1)
        
        if char > 0:
            half = (char + 1) // 2
        else:
            half = sp.S.Half
            
        M = Matrix([
            [a, b * half, d * half],
            [b * half, c, e * half],
            [d * half, e * half, g]
        ])
        det = M.det()
        
        if not det.is_number:
            h2 = False
        else:
            if char > 0:
                h2 = bool(det % char != 0)
            else:
                h2 = bool(det != 0)
    except Exception:
        h2 = False

    try:
        if char > 0:
            facs = sp.factor_list(f, modulus=char)
        else:
            facs = sp.factor_list(f)
            
        non_const_mults = 0
        for factor, mult in facs[1]:
            if sp.Poly(factor, x, y).degree() > 0:
                non_const_mults += mult
                
        neg_q = (non_const_mults > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic not equal to 2",
    "H_2: The determinant of the symmetric matrix is non-zero",
    "not Q: f is reducible over K"
]

N_HYP = 2
NEG_Q_INDEX = 2