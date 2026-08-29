import sympy
from sympy import Matrix, Symbol, expand, simplify, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        T, B = witness
        h1 = isinstance(T, Matrix) and callable(B)
    except Exception:
        h1 = False

    try:
        T, B = witness
        h2 = isinstance(T, Matrix) and callable(B)
    except Exception:
        h2 = False

    try:
        T, B = witness
        n = T.cols
        u = Matrix([Symbol(f'u_{i}') for i in range(n)])
        v = Matrix([Symbol(f'v_{i}') for i in range(n)])
        w = Matrix([Symbol(f'w_{i}') for i in range(n)])
        c = Symbol('c')
        
        def T_star_B(x, y):
            res = B(T*x, T*y)
            if isinstance(res, Matrix) and res.shape == (1, 1):
                return res[0, 0]
            return res
        
        is_bilinear = True
        
        # Check linearity in first argument
        diff1 = expand(T_star_B(u+v, w) - (T_star_B(u, w) + T_star_B(v, w)))
        if diff1 != 0 and simplify(diff1) != 0:
            is_bilinear = False
            
        if is_bilinear:
            diff2 = expand(T_star_B(c*u, w) - c*T_star_B(u, w))
            if diff2 != 0 and simplify(diff2) != 0:
                is_bilinear = False
                
        # Check linearity in second argument
        if is_bilinear:
            diff3 = expand(T_star_B(u, v+w) - (T_star_B(u, v) + T_star_B(u, w)))
            if diff3 != 0 and simplify(diff3) != 0:
                is_bilinear = False
                
        if is_bilinear:
            diff4 = expand(T_star_B(u, c*v) - c*T_star_B(u, v))
            if diff4 != 0 and simplify(diff4) != 0:
                is_bilinear = False
                
        neg_q = not is_bilinear
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: T: V \\to W is a linear transformation",
    "¬Q: T^*B is not a bilinear form on V"
]

N_HYP = 2
NEG_Q_INDEX = 2