import sympy
import itertools

x = sympy.Symbol('x')

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            F_list = witness.get('F_list') or witness.get('f')
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            A, F_list = witness
        else:
            return [False, False, False]
            
        if isinstance(A, list):
            A = sympy.Matrix(A)
            
        if not isinstance(F_list, (list, tuple)):
            F_list = [F_list]
            
        clean_F_list = []
        for f in F_list:
            f_sym = sympy.sympify(f)
            # Normalize the variable to 'x' if there is exactly one free symbol
            if len(f_sym.free_symbols) == 1:
                var = list(f_sym.free_symbols)[0]
                f_sym = f_sym.subs(var, x)
            clean_F_list.append(f_sym)
        F_list = clean_F_list
    except Exception:
        return [False, False, False]

    # H1: A is an n x n matrix over a field F
    try:
        h1 = isinstance(A, sympy.MatrixBase) and A.is_square and A.shape[0] >= 1
    except Exception:
        h1 = False

    # H2: f_1(x), ..., f_k(x) are the invariant factors of A
    try:
        if not h1:
            h2 = False
        else:
            n = A.shape[0]
            if n > 5:  # Prevent timeout for large matrices
                h2 = False
            else:
                M = x * sympy.eye(n) - A
                D = [1]
                for k in range(1, n + 1):
                    minors = []
                    for row_indices in itertools.combinations(range(n), k):
                        for col_indices in itertools.combinations(range(n), k):
                            sub_M = M.extract(row_indices, col_indices)
                            minors.append(sub_M.det())
                    g = minors[0]
                    for m in minors[1:]:
                        g = sympy.gcd(g, m)
                    p = sympy.Poly(g, x)
                    if not p.is_zero:
                        g = sympy.cancel(g / p.LC())
                    D.append(g)
                    
                inv_factors = []
                for k in range(1, n + 1):
                    q = sympy.cancel(D[k] / D[k-1])
                    inv_factors.append(q)
                    
                non_unit_inv = [f for f in inv_factors if x in sympy.sympify(f).free_symbols]
                
                def match(L1, L2):
                    if len(L1) != len(L2): 
                        return False
                    for f1, f2 in zip(L1, L2):
                        ratio = sympy.cancel(f1 / f2)
                        if ratio == 0: 
                            return False
                        if x in ratio.free_symbols: 
                            return False
                    return True

                # F_list can be the full list of invariant factors (including 1s) or just the non-unit ones
                h2 = match(F_list, inv_factors) or match(F_list, non_unit_inv)
    except Exception:
        h2 = False

    # neg_Q: The characteristic polynomial of A is not the product of f_i(x)
    try:
        if not h1:
            neg_q = False
        else:
            prod = 1
            for f in F_list:
                prod = prod * f
            
            n = A.shape[0]
            char_poly_1 = A.charpoly(x).as_expr()
            char_poly_2 = ((-1)**n) * char_poly_1
            
            diff1 = sympy.cancel(prod - char_poly_1)
            diff2 = sympy.cancel(prod - char_poly_2)
            
            neg_q = (diff1 != 0) and (diff2 != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field F",
    "H_2: f_1(x), f_2(x), ..., f_k(x) are the invariant factors of A",
    "¬Q: The characteristic polynomial of A is not the product of f_i(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2