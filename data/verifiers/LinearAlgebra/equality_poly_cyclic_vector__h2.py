import sympy
from sympy import Matrix, Poly, Symbol, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok].
    """
    if isinstance(witness, tuple):
        T = witness[0]
        v = witness[1] if len(witness) > 1 else None
    else:
        T = witness
        v = None

    def format_v(vec):
        if vec is None: 
            return None
        m = Matrix(vec)
        if m.shape[1] != 1:
            m = m.T
        return m

    # H_1: V is an n-dimensional vector space over a field F
    try:
        if hasattr(T, 'is_square'):
            h1 = bool(T.is_square)
        elif hasattr(T, 'shape'):
            h1 = len(T.shape) == 2 and T.shape[0] == T.shape[1]
        elif callable(T) and v is not None:
            v_mat = format_v(v)
            Tv = T(v_mat)
            Tv_mat = format_v(Tv)
            h1 = v_mat.shape[0] == Tv_mat.shape[0]
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: There exists a vector v in V such that {v, T(v), T^2(v), ..., T^{n-1}(v)} is a basis for V
    try:
        x = Symbol('x')
        if v is not None:
            v_mat = format_v(v)
            n = v_mat.shape[0]
            vecs = [v_mat]
            curr = v_mat
            for _ in range(n - 1):
                if callable(T):
                    curr = T(curr)
                else:
                    curr = T * curr
                curr = format_v(curr)
                vecs.append(curr)
            M = Matrix.hstack(*vecs)
            h2 = bool(M.is_square and M.det() != 0)
        else:
            if hasattr(T, 'shape'):
                n = T.shape[0]
            else:
                n = None
            
            if hasattr(T, 'minpoly'):
                if callable(T.minpoly):
                    try:
                        mp = T.minpoly(x)
                    except TypeError:
                        mp = T.minpoly()
                else:
                    mp = T.minpoly
            else:
                mp = None
            
            if n is not None and mp is not None:
                from sympy.polys.polytools import degree
                if hasattr(mp, 'as_expr'):
                    mp = mp.as_expr()
                mp_expr = sympy.sympify(mp)
                if mp_expr.free_symbols and x not in mp_expr.free_symbols:
                    mp_expr = mp_expr.subs(list(mp_expr.free_symbols)[0], x)
                h2 = bool(degree(mp_expr, x) == n)
            else:
                h2 = False
    except Exception:
        h2 = False

    # ¬Q: The minimal polynomial of T is NOT equal to the characteristic polynomial of T
    try:
        x = Symbol('x')
        
        if hasattr(T, 'minpoly'):
            if callable(T.minpoly):
                try:
                    mp = T.minpoly(x)
                except TypeError:
                    mp = T.minpoly()
            else:
                mp = T.minpoly
        else:
            mp = None
            
        if hasattr(T, 'charpoly'):
            if callable(T.charpoly):
                try:
                    cp = T.charpoly(x)
                except TypeError:
                    cp = T.charpoly()
            else:
                cp = T.charpoly
        else:
            cp = None

        if mp is not None and cp is not None:
            if hasattr(mp, 'as_expr'):
                mp = mp.as_expr()
            mp = sympy.sympify(mp)
            if mp.free_symbols and x not in mp.free_symbols:
                mp = mp.subs(list(mp.free_symbols)[0], x)
            
            if hasattr(cp, 'as_expr'):
                cp = cp.as_expr()
            cp = sympy.sympify(cp)
            if cp.free_symbols and x not in cp.free_symbols:
                cp = cp.subs(list(cp.free_symbols)[0], x)
                
            mp_poly = Poly(mp, x)
            cp_poly = Poly(cp, x)
            mp_monic = mp_poly.monic().as_expr()
            cp_monic = cp_poly.monic().as_expr()
            neg_q = bool(sympy.simplify(mp_monic - cp_monic) != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is an n-dimensional vector space over a field F",
    "H_2: There exists a vector v in V such that {v, T(v), T^2(v), ..., T^{n-1}(v)} is a basis for V",
    "¬Q: The minimal polynomial of T is not equal to the characteristic polynomial of T"
]

N_HYP = 2
NEG_Q_INDEX = 2