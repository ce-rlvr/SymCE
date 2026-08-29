import sympy
from sympy import Matrix, eye, zeros, gcd, Poly, Symbol, cancel, S
import itertools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, d_list = witness
    except Exception:
        return [False, False]
        
    try:
        symbols = set()
        for d in d_list:
            if hasattr(d, 'free_symbols'):
                symbols.update(d.free_symbols)
        
        if len(symbols) == 1:
            x = list(symbols)[0]
        elif len(symbols) > 1:
            x_sym = Symbol('x')
            if x_sym in symbols:
                x = x_sym
            else:
                x = list(symbols)[0]
        else:
            x = Symbol('x')
    except Exception:
        x = Symbol('x')

    h1_ok = False
    try:
        if not isinstance(A, Matrix) or A.rows != A.cols:
            h1_ok = False
        elif not isinstance(d_list, (list, tuple)) or len(d_list) == 0:
            h1_ok = False
        else:
            n = A.rows
            M = x * eye(n) - A
            D = [S.One]
            for j in range(1, n + 1):
                minors = []
                for row_indices in itertools.combinations(range(n), j):
                    for col_indices in itertools.combinations(range(n), j):
                        subM = M.extract(row_indices, col_indices)
                        minors.append(subM.det())
                g = minors[0]
                for m in minors[1:]:
                    g = gcd(g, m)
                if g != 0:
                    p = Poly(g, x)
                    g = cancel(g / p.LC())
                D.append(g)
            
            inv_factors = [cancel(D[j] / D[j-1]) for j in range(1, n + 1)]
            non_unit_inv_factors = [f for f in inv_factors if Poly(f, x).degree() > 0]
            
            if len(d_list) == len(inv_factors):
                target = inv_factors
            elif len(d_list) == len(non_unit_inv_factors):
                target = non_unit_inv_factors
            else:
                target = None
                
            if target is not None:
                match_ok = True
                for d, t in zip(d_list, target):
                    Poly(d, x)
                    ratio = cancel(d / t)
                    if x in ratio.free_symbols or ratio == 0:
                        match_ok = False
                        break
                
                if match_ok:
                    for i in range(len(d_list) - 1):
                        ratio = cancel(d_list[i+1] / d_list[i])
                        Poly(ratio, x)
                    h1_ok = True
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        p_A = A.charpoly(x).as_expr().expand()
        prod = S.One
        for d in d_list:
            prod = prod * d
        prod = prod.expand()
        
        if cancel(p_A - prod) != 0:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: d_1(x), ..., d_k(x) are the invariant factors of A such that d_i(x) divides d_{i+1}(x)",
    "¬Q: The characteristic polynomial of A is not the product of d_1(x), ..., d_k(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1