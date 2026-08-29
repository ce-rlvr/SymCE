import sympy
from sympy import symbols
import z3
import functools

# Top-level setup
# The witness will be evaluated in this namespace.
# We define common symbols that might be used in the witness.
x, y, z, t, u, v, w = symbols('x y z t u v w')

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for Tsen's Theorem (false conjecture).
    The witness is expected to be a tuple: (f, vars, t)
    where:
      - f is a sympy expression representing the polynomial
      - vars is a list or tuple of sympy symbols representing the variables
      - t is a sympy symbol representing the transcendental element of L over K
    Example witness: (x**2 + y**2 + z**2, (x, y, z), t)
    """
    
    # H_1: L is a field extension of K of transcendence degree 1
    def check_h1():
        try:
            f, v_list, t_sym = witness
            if not isinstance(t_sym, sympy.Symbol): 
                return False
            if not isinstance(v_list, (list, tuple)): 
                return False
            if not all(isinstance(var, sympy.Symbol) for var in v_list): 
                return False
            if t_sym in v_list: 
                return False
            
            # The polynomial f should be defined over K(t), so its free symbols 
            # must be contained in the variables + {t}
            free_syms = f.free_symbols
            allowed_syms = set(v_list) | {t_sym}
            if not free_syms.issubset(allowed_syms): 
                return False
            
            return True
        except Exception:
            return False

    # H_2: f is a homogeneous polynomial of degree d in n variables over L
    def check_h2():
        try:
            f, v_list, t_sym = witness
            poly = sympy.Poly(f, *v_list)
            return bool(poly.is_homogeneous)
        except Exception:
            return False

    # H_3: n > d
    def check_h3():
        try:
            f, v_list, t_sym = witness
            poly = sympy.Poly(f, *v_list)
            d = poly.homogeneous_order()
            if d <= 0:
                return False
            n = len(v_list)
            return bool(n > d)
        except Exception:
            return False

    # ¬Q: f has NO non-trivial zero in L
    def check_neg_q():
        try:
            f, v_list, t_sym = witness
            
            # To prove f has no non-trivial zero in Q(t), it is sufficient to find 
            # at least one real value for t where f(vars, t) has no non-trivial real zero.
            test_values = [1, 0, -1, 2, -2, 3, -3]
            
            for t_val in test_values:
                solver = z3.Solver()
                z3_vars_dict = {var.name: z3.Real(var.name) for var in v_list}
                
                def sympy_to_z3(expr):
                    if expr.is_Integer:
                        return z3.RealVal(int(expr))
                    elif expr.is_Rational:
                        return z3.RealVal(expr.p) / z3.RealVal(expr.q)
                    elif expr.is_Float:
                        return z3.RealVal(float(expr))
                    elif expr.is_Symbol:
                        if expr == t_sym:
                            return z3.RealVal(t_val)
                        if expr.name in z3_vars_dict:
                            return z3_vars_dict[expr.name]
                        raise ValueError(f"Unknown symbol: {expr}")
                    elif expr.is_Add:
                        return functools.reduce(lambda a, b: a + b, [sympy_to_z3(arg) for arg in expr.args])
                    elif expr.is_Mul:
                        return functools.reduce(lambda a, b: a * b, [sympy_to_z3(arg) for arg in expr.args])
                    elif expr.is_Pow:
                        base = sympy_to_z3(expr.args[0])
                        # Use Python int for exponents to avoid z3 issues with real powers of negative bases
                        if expr.args[1].is_Integer:
                            exp = int(expr.args[1])
                        else:
                            exp = sympy_to_z3(expr.args[1])
                        return base ** exp
                    else:
                        raise ValueError(f"Unsupported sympy expression: {expr}")
                
                try:
                    z3_f = sympy_to_z3(f)
                except Exception:
                    continue
                    
                solver.add(z3_f == 0)
                # Non-trivial zero means at least one variable is non-zero
                solver.add(z3.Or([z3_vars_dict[var.name] != 0 for var in v_list]))
                
                # If unsat, there is no real solution for this t_val, hence no solution in Q(t)
                if solver.check() == z3.unsat:
                    return True
                    
            return False
        except Exception:
            return False

    return [check_h1(), check_h2(), check_h3(), check_neg_q()]

CONDITION_LABELS = [
    "H_1: L is a field extension of K of transcendence degree 1",
    "H_2: f is a homogeneous polynomial of degree d in n variables over L",
    "H_3: n > d",
    "¬Q: f has no non-trivial zero in L"
]

N_HYP = 3
NEG_Q_INDEX = 3