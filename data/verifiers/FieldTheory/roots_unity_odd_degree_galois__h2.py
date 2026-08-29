import sympy as sp
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: n >= 1 is an integer",
    "H_3: K does not contain a primitive 2^n-th root of unity",
    "¬Q: L contains a primitive 2^n-th root of unity"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                L_expr, n_val = witness
                K_expr = x - 1
            elif len(witness) == 3:
                K_expr, L_expr, n_val = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        L_expr = sp.sympify(L_expr)
        K_expr = sp.sympify(K_expr)
        
        if float(n_val) != int(n_val):
            return [False, False, False, False]
        n = int(n_val)
        
        # Prevent timeouts for unreasonably large n
        if n > 5:
            return [False, False, False, False]
            
        L_poly = sp.Poly(L_expr, x, domain='QQ')
        K_poly = sp.Poly(K_expr, x, domain='QQ')
        
    except Exception:
        return [False, False, False, False]

    # H1: L/K is a finite Galois extension
    h1 = False
    try:
        deg_L = L_poly.degree()
        deg_K = K_poly.degree()
        if deg_L >= 1 and deg_K >= 1:
            if L_poly.is_irreducible and K_poly.is_irreducible:
                r_L = sp.RootOf(L_poly.as_expr(), 0)
                coeff, factors = sp.factor_list(L_poly.as_expr(), extension=r_L)
                l_galois = all(sp.degree(fac, x) == 1 for fac, mult in factors)
                
                if l_galois:
                    if deg_K == 1:
                        k_in_l = True
                    else:
                        coeff_k, factors_k = sp.factor_list(K_poly.as_expr(), extension=r_L)
                        k_in_l = any(sp.degree(fac, x) == 1 for fac, mult in factors_k)
                    
                    if k_in_l:
                        h1 = True
    except Exception:
        h1 = False

    # H2: n >= 1 is an integer
    h2 = False
    try:
        if isinstance(n, int) and n >= 1:
            h2 = True
    except Exception:
        h2 = False

    # H3: K does not contain a primitive 2^n-th root of unity
    h3 = False
    try:
        if h2:
            k_val = 2**n
            cyclo = sp.cyclotomic_poly(k_val, x)
            if K_poly.degree() == 1:
                # Q contains a primitive 2^n-th root of unity iff n = 1
                h3 = (n >= 2)
            else:
                r_K = sp.RootOf(K_poly.as_expr(), 0)
                coeff_c, factors_c = sp.factor_list(cyclo, extension=r_K)
                has_root = any(sp.degree(fac, x) == 1 for fac, mult in factors_c)
                h3 = not has_root
    except Exception:
        h3 = False

    # neg_Q: L DOES contain a primitive 2^n-th root of unity
    neg_q = False
    try:
        if h2:
            k_val = 2**n
            cyclo = sp.cyclotomic_poly(k_val, x)
            r_L = sp.RootOf(L_poly.as_expr(), 0)
            coeff_c, factors_c = sp.factor_list(cyclo, extension=r_L)
            has_root = any(sp.degree(fac, x) == 1 for fac, mult in factors_c)
            neg_q = has_root
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]