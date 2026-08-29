import sympy
from sympy import Matrix

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, Matrix):
            vars = sympy.symbols(f'x1:{witness.shape[1]+1}')
            V = Matrix(vars)
            M = witness * V
            a = [0] * len(vars)
        elif isinstance(witness, dict):
            exprs = witness['exprs']
            vars = witness['vars']
            if not isinstance(vars, (list, tuple, Matrix)):
                vars = [vars]
            a = witness.get('a', [0] * len(vars))
            if not isinstance(exprs, (list, tuple, Matrix)):
                exprs = [exprs]
            if not isinstance(a, (list, tuple, Matrix)):
                a = [a]
            M = Matrix(exprs)
            V = Matrix(vars)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                exprs, vars, a = witness
            elif len(witness) == 2:
                exprs, vars = witness
                a = [0] * (len(vars) if isinstance(vars, (list, tuple, Matrix)) else 1)
            else:
                return [False, False]
            
            if not isinstance(exprs, (list, tuple, Matrix)):
                exprs = [exprs]
            if not isinstance(vars, (list, tuple, Matrix)):
                vars = [vars]
            if not isinstance(a, (list, tuple, Matrix)):
                a = [a]
            M = Matrix(exprs)
            V = Matrix(vars)
        else:
            return [False, False]

        if M.shape[1] != 1:
            M = M.reshape(M.shape[0] * M.shape[1], 1)
        if V.shape[1] != 1:
            V = V.reshape(V.shape[0] * V.shape[1], 1)

        zero_subs = {v: 0 for v in vars}
        is_zero_at_origin = M.subs(zero_subs).is_zero_matrix
        
        J = M.jacobian(V)
        is_constant_jacobian = True
        for v in vars:
            if not J.diff(v).is_zero_matrix:
                is_constant_jacobian = False
                break
                
        h1 = bool(is_zero_at_origin and is_constant_jacobian)
    except Exception:
        h1 = False

    try:
        a_subs = {v: val for v, val in zip(vars, a)}
        J_at_a = J.subs(a_subs)
        
        is_differentiable = True
        for item in J_at_a:
            if item.has(sympy.nan) or item.has(sympy.zoo) or item.has(sympy.oo) or item.has(-sympy.oo):
                is_differentiable = False
                break
                
        if not is_differentiable:
            neg_q = True
        else:
            diff_expr = J_at_a * V
            diff_matrix = sympy.simplify(M - diff_expr)
            is_equal = diff_matrix.is_zero_matrix
            neg_q = not bool(is_equal)
            
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: L is a linear transformation from R^n to R^m",
    "¬Q: L is not differentiable at a, or its total derivative at a is not L itself"
]

N_HYP = 1
NEG_Q_INDEX = 1