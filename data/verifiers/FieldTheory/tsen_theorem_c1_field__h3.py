import sympy
from sympy import Poly
from sympy.abc import x, y, z, t, u, v, w

# Top-level setup
C = 'C'
C_t = 'C(t)'

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The missing hypothesis from Tsen's Theorem is that f must be a *homogeneous* polynomial.
    A valid counterexample will be a non-homogeneous polynomial (e.g., f = x**2 - t) 
    that has no zeros in L.
    """
    # H_1: K is an algebraically closed field
    try:
        K = str(witness.get('K', ''))
        h1 = K in ['C', 'Complexes', 'AlgebraicallyClosedField']
    except Exception:
        h1 = False

    # H_2: L is a field extension of K of transcendence degree 1
    try:
        L = str(witness.get('L', ''))
        h2 = L in ['C(t)', 'Complexes(t)']
    except Exception:
        h2 = False

    # H_3: n > d
    try:
        n = int(witness.get('n', 0))
        d = int(witness.get('d', 0))
        f = witness.get('f')
        vars_list = witness.get('vars', [])
        
        if f is None or not vars_list:
            h3 = False
        else:
            poly_f = sympy.Poly(f, *vars_list)
            actual_d = poly_f.total_degree()
            h3 = (n > d) and (d == actual_d) and (n == len(vars_list))
    except Exception:
        h3 = False

    # ¬Q: The polynomial f has NO non-trivial zero in L
    try:
        f = witness.get('f')
        vars_list = witness.get('vars', [])
        t_var = witness.get('t')
        
        if f is None or not vars_list or t_var is None:
            neg_q = False
        else:
            # Solve the polynomial system over the variables
            sols = sympy.solve(f, vars_list, dict=True)
            has_zero = False
            
            if sols:
                for sol in sols:
                    possible = True
                    for var, expr in sol.items():
                        # Check if the solution for this variable depends on free variables
                        free = expr.free_symbols - {t_var}
                        if not free:
                            # If it strictly depends only on t, it must be a rational function in C(t)
                            if not expr.is_rational_function(t_var):
                                possible = False
                                break
                    if possible:
                        has_zero = True
                        break
            
            # If has_zero is False, the polynomial has no zeros at all in C(t), 
            # hence no non-trivial zeros.
            neg_q = not has_zero
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: L is a field extension of K of transcendence degree 1",
    "H_3: n > d",
    "¬Q: The polynomial f has no non-trivial zero in L"
]

N_HYP = 3
NEG_Q_INDEX = 3