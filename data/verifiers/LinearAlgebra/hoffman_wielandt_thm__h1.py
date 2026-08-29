import sympy
import itertools

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def check_roots(M, roots_list):
    try:
        x = sympy.Symbol('x')
        char_M = M.charpoly(x).as_expr()
        if not roots_list:
            poly_M = sympy.Integer(1)
        else:
            poly_M = sympy.Mul(*[x - e for e in roots_list])
        diff_expr = sympy.expand(char_M - poly_M)
        diff_M = sympy.Poly(diff_expr, x)
        for c in diff_M.coeffs():
            c_simp = sympy.simplify(c)
            if c_simp == 0:
                continue
            try:
                if abs(complex(c_simp)) > 1e-9:
                    return False
            except Exception:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) == 4:
            A, B, lambdas, mus = witness
            
            if not isinstance(A, sympy.MatrixBase) or not isinstance(B, sympy.MatrixBase):
                return [False, False, False]
            if A.shape[0] != A.shape[1] or A.shape != B.shape:
                return [False, False, False]
            
            n = A.shape[0]
            if n > 5:
                return [False, False, False]
                
            if len(lambdas) != n or len(mus) != n:
                return [False, False, False]
            
            h1 = check_roots(A, lambdas)
            h2 = check_roots(B, mus)
            
        elif len(witness) == 2:
            A, B = witness
            if not isinstance(A, sympy.MatrixBase) or not isinstance(B, sympy.MatrixBase):
                return [False, False, False]
            if A.shape[0] != A.shape[1] or A.shape != B.shape:
                return [False, False, False]
            
            n = A.shape[0]
            if n > 5:
                return [False, False, False]
                
            lambdas = []
            for val, mult in A.eigenvals().items():
                lambdas.extend([val] * mult)
            mus = []
            for val, mult in B.eigenvals().items():
                mus.extend([val] * mult)
                
            if len(lambdas) != n or len(mus) != n:
                return [False, False, False]
                
            h1 = True
            h2 = True
        else:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    try:
        diff_matrix = A - B
        F_sq = sum(sympy.Abs(c)**2 for c in diff_matrix)
        
        neg_q = True
        for sigma in itertools.permutations(mus):
            current_sum = sum(sympy.Abs(lambdas[i] - sigma[i])**2 for i in range(n))
            diff = current_sum - F_sq
            
            is_leq = False
            try:
                diff_simp = sympy.simplify(diff)
                if diff_simp.is_number and diff_simp.is_real:
                    if diff_simp <= 1e-9:
                        is_leq = True
                else:
                    if float(sympy.re(diff_simp.evalf())) <= 1e-9:
                        is_leq = True
            except Exception:
                try:
                    if float(sympy.re(diff.evalf())) <= 1e-9:
                        is_leq = True
                except Exception:
                    is_leq = True # conservative fallback
                    
            if is_leq:
                neg_q = False
                break
                
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: lambda_1, ..., lambda_n are the eigenvalues of A",
    "H_2: mu_1, ..., mu_n are the eigenvalues of B",
    "¬Q: For all permutations sigma, sum |lambda_i - mu_{sigma(i)}|^2 > ||A - B||_F^2"
]

N_HYP = 2
NEG_Q_INDEX = 2