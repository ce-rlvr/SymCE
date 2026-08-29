import sympy
from sympy import ZZ, QQ

x = sympy.Symbol('x')

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: K is the fraction field of R",
    "H_3: p and q are coprime elements of R",
    "H_4: The element p/q in K is a root of f(x)",
    "¬Q: The element q does not divide a_n or p does not divide a_0 in R"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        R, K, p, q, f = witness
    except Exception:
        return [False] * 5

    # H1: R is a Unique Factorization Domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    # H2: K is the fraction field of R
    try:
        h2 = bool(K == R.frac_field())
    except Exception:
        h2 = False

    # H3: p and q are coprime elements of R
    try:
        if p in R and q in R:
            gcd_pq = R.gcd(p, q)
            try:
                R.exquo(R.one, gcd_pq)
                h3 = True
            except Exception:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: The element p/q in K is a root of f(x)
    try:
        if hasattr(f, 'as_expr'):
            f_expr = f.as_expr()
        else:
            f_expr = sympy.sympify(f)
            
        free_syms = f_expr.free_symbols
        if len(free_syms) == 1:
            x_sym = list(free_syms)[0]
        else:
            x_sym = sympy.Symbol('x')
            
        p_sym = R.to_sympy(p)
        q_sym = R.to_sympy(q)
        val = f_expr.subs(x_sym, p_sym / q_sym)
        h4 = bool(sympy.simplify(val) == 0)
    except Exception:
        h4 = False

    # neg_Q: The element q does not divide a_n or p does not divide a_0 in R
    try:
        if hasattr(f, 'as_expr'):
            f_expr = f.as_expr()
        else:
            f_expr = sympy.sympify(f)
            
        free_syms = f_expr.free_symbols
        if len(free_syms) == 1:
            x_sym = list(free_syms)[0]
        else:
            x_sym = sympy.Symbol('x')
            
        f_poly = sympy.Poly(f_expr, x_sym)
        coeffs = f_poly.all_coeffs()
        
        if not coeffs:
            conclusion = True
        else:
            a_n = coeffs[0]
            a_0 = coeffs[-1]
            
            try:
                a_n_R = R.from_sympy(a_n)
                a_0_R = R.from_sympy(a_0)
                
                if a_n_R == R.zero:
                    q_div_an = True
                else:
                    try:
                        R.exquo(a_n_R, q)
                        q_div_an = True
                    except Exception:
                        q_div_an = False
                        
                if a_0_R == R.zero:
                    p_div_a0 = True
                else:
                    try:
                        R.exquo(a_0_R, p)
                        p_div_a0 = True
                    except Exception:
                        p_div_a0 = False
                        
                conclusion = q_div_an and p_div_a0
            except Exception:
                # Coercion to R failed, meaning coefficients are not in R
                conclusion = False
                
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]