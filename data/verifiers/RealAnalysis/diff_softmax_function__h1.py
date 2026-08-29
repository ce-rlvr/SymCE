import sympy
from sympy import Matrix, Symbol
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = sympy.symbols('x y z', real=True)
x1, x2, x3, x4, x5 = sympy.symbols('x1 x2 x3 x4 x5', real=True)

def conditions(witness) -> list[bool]:
    try:
        # Extract the function as a sympy Matrix and determine the variables
        if callable(witness):
            vars_list = [x1, x2, x3, x4, x5]
            f_val = None
            for n in range(1, 6):
                try:
                    res = witness(vars_list[:n])
                    if isinstance(res, (list, tuple, sympy.Matrix)):
                        f_val = sympy.Matrix(res)
                        used_vars = vars_list[:n]
                        break
                except Exception:
                    try:
                        res = witness(*vars_list[:n])
                        if isinstance(res, (list, tuple, sympy.Matrix)):
                            f_val = sympy.Matrix(res)
                            used_vars = vars_list[:n]
                            break
                    except Exception:
                        pass
            if f_val is None:
                return [False]
        else:
            if isinstance(witness, (list, tuple)):
                f_val = sympy.Matrix(witness)
            elif isinstance(witness, sympy.Matrix):
                f_val = witness
            elif isinstance(witness, sympy.Expr):
                f_val = sympy.Matrix([witness])
            else:
                return [False]
            
            used_vars = list(f_val.free_symbols)
            
            # Prioritize standard variable names as the differentiation variables
            def var_priority(v):
                name = v.name
                if name in ['x', 'y', 'z']:
                    return 0
                if name.startswith('x') and name[1:].isdigit():
                    return 1
                return 2
            used_vars.sort(key=lambda v: (var_priority(v), v.name))
            
            if not used_vars:
                used_vars = [sympy.Symbol('x', real=True)]
                
        n = len(f_val)
        f_val = f_val.reshape(n, 1)
        
        # Ensure we have exactly n variables for a function R^n -> R^n
        if len(used_vars) < n:
            extra_vars = sympy.symbols(f'v1:{n - len(used_vars) + 1}', real=True)
            used_vars.extend(extra_vars)
        elif len(used_vars) > n:
            used_vars = used_vars[:n]
            
        # Compute the Jacobian matrix
        J = f_val.jacobian(used_vars)
        
        # Compute the expected Jacobian matrix based on the formula
        M = sympy.zeros(n, n)
        for i in range(n):
            for j in range(n):
                if i == j:
                    M[i, j] = f_val[i] * (1 - f_val[j])
                else:
                    M[i, j] = -f_val[i] * f_val[j]
                    
        diff_matrix = J - M
        
        # Check if the difference is the zero matrix
        if diff_matrix.is_zero_matrix:
            neg_q = False
        else:
            diff_matrix_expanded = diff_matrix.expand()
            if diff_matrix_expanded.is_zero_matrix:
                neg_q = False
            else:
                # Fallback to numerical evaluation to robustly check for zero equivalence
                is_zero = False
                for offset in [1.234, 2.718, 3.141]:
                    subs_dict = {v: i + offset for i, v in enumerate(used_vars)}
                    val = diff_matrix.subs(subs_dict).evalf()
                    current_is_zero = True
                    for i in range(n):
                        for j in range(n):
                            try:
                                c_val = complex(val[i, j])
                                if math.isnan(c_val.real) or math.isnan(c_val.imag):
                                    current_is_zero = False
                                    break
                                if abs(c_val) > 1e-7:
                                    current_is_zero = False
                                    break
                            except TypeError:
                                current_is_zero = False
                                break
                        if not current_is_zero:
                            break
                    if current_is_zero:
                        is_zero = True
                        break
                neg_q = not is_zero
                
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The Jacobian of f does not match the Softmax Jacobian formula or f is not continuously differentiable"
]

N_HYP = 0
NEG_Q_INDEX = 0