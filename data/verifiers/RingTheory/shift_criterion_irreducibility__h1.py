import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

# Top-level setup for potential witness expressions
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

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "f(x) is irreducible in R[x] if and only if f(x+c) is irreducible in R[x]"
    """
    try:
        # 1. Check for M2(Z2) dictionary format
        if isinstance(witness, dict) and witness.get('ring') == 'M2(Z2)':
            U = sp.Matrix(witness['U']) % 2
            V = sp.Matrix(witness['V']) % 2
            c = sp.Matrix(witness['c']) % 2
            
            matrices = [sp.Matrix([[a, b], [c_val, d]]) for a, b, c_val, d in itertools.product([0, 1], repeat=4)]
            def is_reducible(U_m, V_m):
                for C in matrices:
                    if (C**2 + C*U_m + V_m) % 2 == sp.zeros(2, 2):
                        return True
                return False
                
            f_red = is_reducible(U, V)
            W = (c**2 + U*c + V) % 2
            fc_red = is_reducible(U, W)
            
            return [True, True, f_red != fc_red]
            
        # 2. Check for tuple of 3 matrices (U, V, c) over Z2
        if isinstance(witness, tuple) and len(witness) == 3:
            if all(isinstance(m, sp.MatrixBase) and m.shape == (2, 2) for m in witness):
                if all(entry in [0, 1] for m in witness for entry in m):
                    U, V, c = witness
                    U_mat = U % 2
                    V_mat = V % 2
                    c_mat = c % 2
                    
                    matrices = [sp.Matrix([[a, b], [c_val, d]]) for a, b, c_val, d in itertools.product([0, 1], repeat=4)]
                    def is_reducible(U_m, V_m):
                        for C in matrices:
                            if (C**2 + C*U_m + V_m) % 2 == sp.zeros(2, 2):
                                return True
                        return False
                        
                    f_red = is_reducible(U_mat, V_mat)
                    W_mat = (c_mat**2 + U_mat*c_mat + V_mat) % 2
                    fc_red = is_reducible(U_mat, W_mat)
                    
                    return [True, True, f_red != fc_red]

        # 3. General format: dict or tuple with f, c, x, and optionally g, h
        f, c, x, g, h = None, None, None, None, None
        if isinstance(witness, dict):
            f = witness.get('f')
            c = witness.get('c')
            x = witness.get('x')
            g = witness.get('g')
            h = witness.get('h')
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                f, c, x = witness
            elif len(witness) == 5:
                f, c, g, h, x = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if f is None or c is None or x is None:
            return [False, False, False]
            
        # H_1: f is a polynomial over R
        h1 = isinstance(f, (sp.Expr, sp.MatrixBase))
        
        # H_2: c is an element of R
        if isinstance(c, sp.MatrixBase):
            h2 = not any(x in entry.free_symbols for entry in c)
        else:
            h2 = isinstance(c, sp.Expr) and x not in c.free_symbols
            
        neg_q = False
        
        # If f and c are matrices
        if isinstance(f, sp.MatrixBase) and isinstance(c, sp.MatrixBase):
            n = f.shape[0]
            if c.shape != (n, n):
                return [h1, h2, False]
                
            I = sp.eye(n)
            
            def eval_mat_poly(poly, shift):
                max_deg = 0
                for i in range(n):
                    for j in range(n):
                        try:
                            d = sp.Poly(poly[i, j], x).degree()
                            if d > max_deg: max_deg = d
                        except Exception:
                            pass
                res = sp.zeros(n, n)
                for k in range(max_deg + 1):
                    mat_k = sp.Matrix(n, n, lambda i, j: sp.Poly(poly[i, j], x).nth(k))
                    res += mat_k * (x*I + shift)**k
                return sp.expand(res)
                
            f_shifted = eval_mat_poly(f, c)
            
            def is_unit(mat):
                d = sp.expand(mat.det())
                return x not in d.free_symbols and d != 0
                
            def is_irreducible_det(mat):
                d = sp.expand(mat.det())
                if x not in d.free_symbols: return False
                try:
                    factors = sp.factor_list(d)
                    return len(factors[1]) == 1 and factors[1][0][1] == 1
                except Exception:
                    return False
                    
            f_irred = is_irreducible_det(f)
            f_shifted_irred = is_irreducible_det(f_shifted)
            
            def check_factorization(target, g_fac, h_fac):
                if g_fac is None or h_fac is None: return False
                if sp.expand(g_fac * h_fac - target) != sp.zeros(n, n): return False
                if is_unit(g_fac) or is_unit(h_fac): return False
                return True
                
            if g is not None and h is not None:
                f_shifted_reducible = check_factorization(f_shifted, g, h)
                f_reducible = check_factorization(f, g, h)
                
                if (f_irred and f_shifted_reducible) or (f_shifted_irred and f_reducible):
                    neg_q = True
                    
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f is a polynomial over R",
    "H_2: c is an element of R",
    "¬Q: f is irreducible iff f shifted by c is irreducible is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2