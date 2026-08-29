import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_dim_and_T(witness):
    """
    Attempts to extract the dimension and the transformation function T from the witness.
    Handles matrices, tuples of (dim, T), objects with .dim and .T, and raw callables.
    """
    if hasattr(witness, 'shape') and len(witness.shape) == 2:
        dim = witness.shape[0]
        def T(v, w=witness):
            v_mat = sp.Matrix(v)
            res = w * v_mat
            return list(res)
        return dim, T
        
    if isinstance(witness, tuple) and len(witness) == 2:
        if isinstance(witness[0], int) and callable(witness[1]):
            dim = witness[0]
            T_raw = witness[1]
            def T(v, w=T_raw):
                try:
                    res = w(tuple(v))
                    return list(res)
                except Exception:
                    try:
                        res = w(*tuple(v))
                        return list(res)
                    except Exception:
                        res = w(sp.Matrix(v))
                        return list(res)
            return dim, T
            
    if hasattr(witness, 'T') and callable(witness.T) and hasattr(witness, 'dim'):
        dim = witness.dim
        T_raw = witness.T
        def T(v, w=T_raw):
            try:
                res = w(tuple(v))
                return list(res)
            except Exception:
                try:
                    res = w(*tuple(v))
                    return list(res)
                except Exception:
                    res = w(sp.Matrix(v))
                    return list(res)
        return dim, T

    if callable(witness):
        for dim in [2, 3, 4, 5]:
            vars_sym = sp.symbols(f'x0:{dim}', real=True)
            try:
                res = witness(vars_sym)
                if len(list(res)) == dim:
                    def T(v, w=witness):
                        return list(w(tuple(v)))
                    return dim, T
            except Exception:
                try:
                    res = witness(*vars_sym)
                    if len(list(res)) == dim:
                        def T(v, w=witness):
                            return list(w(*tuple(v)))
                        return dim, T
                except Exception:
                    try:
                        res = witness(sp.Matrix(vars_sym))
                        if len(list(res)) == dim:
                            def T(v, w=witness):
                                return list(w(sp.Matrix(v)))
                            return dim, T
                    except Exception:
                        continue
                        
    return None, None

def check_subspace(eqs, vars_sym):
    """
    Checks if the algebraic set defined by eqs == 0 is a linear subspace.
    Returns (is_subspace: bool, dimension: int).
    """
    try:
        sols = sp.solve(eqs, vars_sym, dict=True)
    except Exception:
        return False, 0
    
    if not sols:
        return False, 0
        
    # A linear subspace should be a single irreducible component
    if len(sols) > 1:
        return False, 0
        
    sol = sols[0]
    free_vars = set(vars_sym) - set(sol.keys())
    c = sp.Symbol('c_scalar', real=True)
    
    for var, expr in sol.items():
        # Check if the origin is included
        if sp.simplify(sp.expand(expr.subs({fv: 0 for fv in free_vars}))) != 0:
            return False, 0
            
        # Check homogeneity of degree 1 (scalar multiplication closure)
        expr_c = expr.subs({fv: c * fv for fv in free_vars})
        if sp.simplify(sp.expand(expr_c - c * expr)) != 0:
            return False, 0
            
        # Check additivity (vector addition closure)
        fv1 = {fv: sp.Symbol(f"{fv.name}_1", real=True) for fv in free_vars}
        fv2 = {fv: sp.Symbol(f"{fv.name}_2", real=True) for fv in free_vars}
        
        expr_1 = expr.subs(fv1)
        expr_2 = expr.subs(fv2)
        expr_sum = expr.subs({fv: fv1[fv] + fv2[fv] for fv in free_vars})
        
        if sp.simplify(sp.expand(expr_sum - (expr_1 + expr_2))) != 0:
            return False, 0
            
    return True, len(free_vars)

def conditions(witness) -> list[bool]:
    dim, T_func = get_dim_and_T(witness)
    
    if dim is None or T_func is None:
        return [False, False, False]
        
    # H_1: V is a vector space over a field of characteristic not equal to 2
    try:
        h1 = True
        if hasattr(witness, 'char'):
            h1 = (witness.char != 2)
    except Exception:
        h1 = False
        
    # H_2: T^2 is equal to the identity operator I
    try:
        vars_sym = sp.symbols(f'x0:{dim}', real=True)
        Tv = T_func(vars_sym)
        TTv = T_func(Tv)
        h2 = True
        for i in range(dim):
            if sp.simplify(sp.expand(TTv[i] - vars_sym[i])) != 0:
                h2 = False
                break
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion fails
    try:
        vars_sym = sp.symbols(f'x0:{dim}', real=True)
        Tv = T_func(vars_sym)
        
        # W_1 = {v | T(v) = v}
        eqs1 = [Tv[i] - vars_sym[i] for i in range(dim)]
        is_sub1, dim1 = check_subspace(eqs1, vars_sym)
        
        # W_2 = {v | T(v) = -v}
        eqs2 = [Tv[i] + vars_sym[i] for i in range(dim)]
        is_sub2, dim2 = check_subspace(eqs2, vars_sym)
        
        if not is_sub1 or not is_sub2:
            neg_q = True
        elif dim1 + dim2 != dim:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field of characteristic not equal to 2",
    "H_2: T^2 is equal to the identity operator I",
    "¬Q: W_1 and W_2 are not both T-invariant subspaces, or V != W_1 \\oplus W_2"
]

N_HYP = 2
NEG_Q_INDEX = 2