import sympy
from sympy import MatrixBase, Poly, Expr, Symbol, eye, zeros, I
from sympy.matrices import Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
x = Symbol('x')

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        T, p = witness
    except Exception:
        return [False, False, False]
    
    # H1: T is a linear operator (represented as a square matrix)
    try:
        h1 = isinstance(T, MatrixBase) and T.is_square
    except Exception:
        h1 = False
        
    # H2: p(x) is a polynomial
    try:
        p_sym = sympy.sympify(p)
        if isinstance(p_sym, Poly):
            h2 = len(p_sym.free_symbols) <= 1
        elif isinstance(p_sym, Expr):
            free = p_sym.free_symbols
            if len(free) > 1:
                h2 = False
            else:
                sym = list(free)[0] if free else Symbol('x')
                Poly(p_sym, sym)
                h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: (p(T))* != p(T*)
    try:
        p_sym = sympy.sympify(p)
        if isinstance(p_sym, Poly):
            poly = p_sym
        else:
            free = p_sym.free_symbols
            sym = list(free)[0] if free else Symbol('x')
            poly = Poly(p_sym, sym)
            
        coeffs = poly.all_coeffs()
        n = T.shape[0]
        
        p_T = zeros(n, n)
        p_Tadj = zeros(n, n)
        deg = len(coeffs) - 1
        
        T_adj = T.adjoint()
        
        for i, c in enumerate(coeffs):
            if deg - i == 0:
                p_T += c * eye(n)
                p_Tadj += c * eye(n)
            else:
                p_T += c * (T ** (deg - i))
                p_Tadj += c * (T_adj ** (deg - i))
                
        p_T_adj = p_T.adjoint()
        
        diff = p_T_adj - p_Tadj
        neg_q = False
        for i in range(n):
            for j in range(n):
                if diff[i, j].simplify() != 0:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator",
    "H_2: p(x) is a polynomial",
    "¬Q: (p(T))* != p(T*)"
]

N_HYP = 2
NEG_Q_INDEX = 2