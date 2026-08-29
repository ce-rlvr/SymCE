import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        f_coeffs, g_coeffs = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        def is_nonzero(c):
            if hasattr(c, 'is_Matrix') and c.is_Matrix:
                return not c.is_zero_matrix
            return c != 0

        H1 = len(f_coeffs) > 0 and len(g_coeffs) > 0 and any(is_nonzero(c) for c in f_coeffs) and any(is_nonzero(c) for c in g_coeffs)
    except Exception:
        H1 = False

    H2 = True
    
    try:
        m = len(g_coeffs) - 1
        H3 = m >= 0
    except Exception:
        H3 = False

    neg_Q = False
    try:
        fg_coeffs = []
        for _ in range(len(f_coeffs) + len(g_coeffs) - 1):
            fg_coeffs.append(None)
            
        for i, a in enumerate(f_coeffs):
            for j, b in enumerate(g_coeffs):
                prod = a * b
                if fg_coeffs[i+j] is None:
                    fg_coeffs[i+j] = prod
                else:
                    fg_coeffs[i+j] = fg_coeffs[i+j] + prod
                    
        for i in range(len(fg_coeffs)):
            if fg_coeffs[i] is None:
                fg_coeffs[i] = 0

        def ideal_mul(I, J):
            res = []
            for a in I:
                for b in J:
                    prod = a * b
                    is_new = True
                    for r in res:
                        if prod == r:
                            is_new = False
                            break
                    if is_new:
                        res.append(prod)
            return res

        def ideal_pow(I, k):
            if k <= 0:
                if I and hasattr(I[0], 'is_Matrix') and I[0].is_Matrix:
                    return [sympy.eye(I[0].rows)]
                return [1]
            res = I
            for _ in range(k - 1):
                res = ideal_mul(res, I)
            return res

        cf = f_coeffs
        cg = g_coeffs
        cfg = fg_coeffs

        cf_m1 = ideal_pow(cf, m + 1)
        lhs_gens = ideal_mul(cf_m1, cg)
        
        cf_m = ideal_pow(cf, m)
        rhs_gens = ideal_mul(cf_m, cfg)
        
        def check_equality(gens1, gens2):
            if not gens1 and not gens2:
                return True
            if not gens1 or not gens2:
                def all_zero(gens):
                    for g in gens:
                        if hasattr(g, 'is_Matrix') and g.is_Matrix:
                            if not g.is_zero_matrix:
                                return False
                        elif g != 0:
                            return False
                    return True
                return all_zero(gens1) and all_zero(gens2)
                
            is_mat = hasattr(gens1[0], 'is_Matrix') and gens1[0].is_Matrix
            if is_mat:
                def to_matrix(gens):
                    vecs = [g.vec() for g in gens if not g.is_zero_matrix]
                    if not vecs:
                        return sympy.Matrix()
                    return sympy.Matrix.hstack(*vecs)
                M1 = to_matrix(gens1)
                M2 = to_matrix(gens2)
                if M1.cols == 0 and M2.cols == 0:
                    return True
                if M1.cols == 0 or M2.cols == 0:
                    return False
                r1 = M1.rank()
                r2 = M2.rank()
                if r1 != r2:
                    return False
                M12 = sympy.Matrix.hstack(M1, M2)
                return M12.rank() == r1
            
            has_syms = any(hasattr(g, 'free_symbols') and g.free_symbols for g in gens1 + gens2)
            if has_syms:
                free_symbols = list(set().union(*(g.free_symbols for g in gens1 + gens2 if hasattr(g, 'free_symbols'))))
                if any(not s.is_commutative for s in free_symbols):
                    set1 = set(sympy.expand(g) for g in gens1 if sympy.expand(g) != 0)
                    set2 = set(sympy.expand(g) for g in gens2 if sympy.expand(g) != 0)
                    return set1 == set2
                
                gb1 = sympy.groebner(gens1, *free_symbols)
                gb2 = sympy.groebner(gens2, *free_symbols)
                in1 = all(sympy.reduced(g, gb2)[1] == 0 for g in gens1)
                in2 = all(sympy.reduced(g, gb1)[1] == 0 for g in gens2)
                return in1 and in2
                
            def gcd_list(lst):
                g = 0
                for x in lst:
                    g = sympy.gcd(g, x)
                return g
            return gcd_list(gens1) == gcd_list(gens2)

        ideals_equal = check_equality(lhs_gens, rhs_gens)
        neg_Q = not ideals_equal

    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = ["H_1: f and g are non-zero polynomials", "H_2: c(f) and c(g) are the content ideals of f and g", "H_3: m is the degree of the polynomial g", "not Q: c(f)**(m+1) c(g) != c(f)**m c(fg)"]
N_HYP = 3
NEG_Q_INDEX = 3