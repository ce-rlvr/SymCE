import sympy
import math

x = sympy.Symbol('x')
alpha = sympy.sqrt(-5)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to Gauss's Lemma for Polynomial Content
    when the ring is not a UFD (e.g., Z[sqrt(-5)]).
    """
    try:
        if not (isinstance(witness, (tuple, list)) and len(witness) == 2):
            return [False, False]
            
        f_expr, g_expr = witness
        
        # We assume the ring is Z[sqrt(-5)]
        d = -5
        sq_d = sympy.sqrt(d)
        
        free_symbols = f_expr.free_symbols | g_expr.free_symbols
        var = x
        if free_symbols:
            if x in free_symbols:
                var = x
            else:
                var = list(free_symbols)[0]
                
        def extract_coeffs(expr):
            poly = sympy.Poly(expr, var)
            coeffs = poly.all_coeffs()
            parsed = []
            for c in coeffs:
                c = sympy.expand(c)
                a = c.subs(sq_d, 0)
                b = sympy.simplify((c - a) / sq_d)
                if not a.is_Integer or not b.is_Integer:
                    return None
                parsed.append((int(a), int(b)))
            return parsed[::-1] # lowest degree first
            
        f_coeffs = extract_coeffs(f_expr)
        g_coeffs = extract_coeffs(g_expr)
        
        if f_coeffs is None or g_coeffs is None:
            return [False, False]
            
        def is_zero_z(A): 
            return A[0] == 0 and A[1] == 0
            
        f_non_zero = any(not is_zero_z(c) for c in f_coeffs)
        g_non_zero = any(not is_zero_z(c) for c in g_coeffs)
        H1 = f_non_zero and g_non_zero
        
        if not H1:
            return [False, False]
            
        def norm(A): 
            return A[0]**2 - d * A[1]**2
        
        def mul_z(A, B):
            return (A[0]*B[0] + d*A[1]*B[1], A[0]*B[1] + A[1]*B[0])
            
        def divides_z(A, B):
            nA = norm(A)
            if nA == 0: 
                return is_zero_z(B)
            num_real = B[0]*A[0] - d*B[1]*A[1]
            num_imag = B[1]*A[0] - B[0]*A[1]
            return num_real % nA == 0 and num_imag % nA == 0
            
        def get_gcds_z(coeffs):
            non_zero = [c for c in coeffs if not is_zero_z(c)]
            if not non_zero: 
                return []
            min_c = min(non_zero, key=norm)
            min_norm = norm(min_c)
            
            divisors = []
            for i in range(1, int(math.isqrt(min_norm)) + 1):
                if min_norm % i == 0:
                    divisors.append(i)
                    if i * i != min_norm:
                        divisors.append(min_norm // i)
                        
            possible_A = []
            D = -d
            for n in divisors:
                max_b = int(math.isqrt(n // D))
                for b in range(-max_b - 1, max_b + 2):
                    rem = n - D * b**2
                    if rem >= 0:
                        a = int(math.isqrt(rem))
                        if a * a == rem:
                            possible_A.append((a, b))
                            if a != 0:
                                possible_A.append((-a, b))
                                
            cds = [A for A in possible_A if all(divides_z(A, c) for c in coeffs)]
            return [G for G in cds if all(divides_z(D, G) for D in cds)]
            
        gcds_f = get_gcds_z(f_coeffs)
        gcds_g = get_gcds_z(g_coeffs)
        
        deg_f = len(f_coeffs) - 1
        deg_g = len(g_coeffs) - 1
        fg = [(0, 0)] * (deg_f + deg_g + 1)
        for i in range(deg_f + 1):
            for j in range(deg_g + 1):
                term = mul_z(f_coeffs[i], g_coeffs[j])
                fg[i+j] = (fg[i+j][0] + term[0], fg[i+j][1] + term[1])
                
        gcds_fg = get_gcds_z(fg)
        
        units = [(1, 0), (-1, 0)]
        
        conclusion = False
        if gcds_f and gcds_g and gcds_fg:
            for c_f in gcds_f:
                for c_g in gcds_g:
                    prod = mul_z(c_f, c_g)
                    for c_fg in gcds_fg:
                        if any(mul_z(c_fg, U) == prod for U in units):
                            conclusion = True
                            break
                    if conclusion: break
                if conclusion: break
                
        return [H1, not conclusion]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: f and g are non-zero polynomials",
    "¬Q: The content of fg is not equal to the product of the contents of f and g (up to units)"
]

N_HYP = 1
NEG_Q_INDEX = 1