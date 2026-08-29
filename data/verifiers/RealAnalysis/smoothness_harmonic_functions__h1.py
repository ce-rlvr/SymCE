import sympy as sp
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = sp.symbols('x y z', real=True)

def is_well_defined_real(val):
    """Check if a sympy value evaluates to a finite real number."""
    try:
        if val.is_number and val.is_finite and val.is_real:
            return True
        val_f = val.evalf()
        if val_f.is_number and val_f.is_finite and val_f.is_real:
            return True
        return False
    except Exception:
        return False

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with:
      - 'u': a sympy expression for the function u
      - 'vars': a list or tuple of sympy symbols (the variables of u)
      - 'U_cond': a dict (or list of dicts/Eqs) defining the domain U (e.g., {y: 0})
      - 'point': a dict defining a point in U where C^\infty fails (e.g., {x: 0, y: 0})
    """
    try:
        u = witness['u']
        vars = witness['vars']
        U_cond = witness.get('U_cond', {})
        point = witness['point']
        if isinstance(point, (list, tuple)):
            point = dict(zip(vars, point))
    except Exception:
        return [False, False, False]

    # H_1: u is a twice continuously differentiable function
    # We verify this by checking that all partial derivatives up to order 3 
    # evaluate to finite real numbers at the given point.
    h1_ok = True
    try:
        for order in range(1, 4):
            for p in itertools.product(vars, repeat=order):
                deriv = u
                for v in p:
                    deriv = sp.diff(deriv, v)
                val = deriv.subs(point)
                if not is_well_defined_real(val):
                    h1_ok = False
                    break
            if not h1_ok:
                break
    except Exception:
        h1_ok = False

    # H_2: The Laplacian of u is 0 for all x in U
    h2_ok = False
    subs_dict = {}
    try:
        laplacian = sum(sp.diff(u, v, 2) for v in vars)
        if callable(U_cond):
            lap_on_U = U_cond(laplacian)
        else:
            if isinstance(U_cond, dict):
                subs_dict = U_cond
            elif isinstance(U_cond, sp.Eq):
                subs_dict = {U_cond.lhs: U_cond.rhs}
            elif isinstance(U_cond, list):
                for item in U_cond:
                    if isinstance(item, sp.Eq):
                        subs_dict[item.lhs] = item.rhs
                    elif isinstance(item, dict):
                        subs_dict.update(item)
            lap_on_U = laplacian.subs(subs_dict)
        
        if sp.simplify(lap_on_U) == 0:
            h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The function u is not infinitely differentiable on U
    # We verify this by finding at least one partial derivative up to order 6 
    # that fails to evaluate to a finite real number at the given point in U.
    neg_q = False
    try:
        # First, ensure the point is actually in U
        point_in_U = True
        if not callable(U_cond):
            for k, v in subs_dict.items():
                k_val = k.subs(point) if hasattr(k, 'subs') else k
                v_val = v.subs(point) if hasattr(v, 'subs') else v
                if sp.simplify(k_val - v_val) != 0:
                    point_in_U = False
                    break
        
        if point_in_U:
            for order in range(1, 7):
                for p in itertools.product(vars, repeat=order):
                    deriv = u
                    for v in p:
                        deriv = sp.diff(deriv, v)
                    val = deriv.subs(point)
                    if not is_well_defined_real(val):
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: u is a twice continuously differentiable function",
    "H_2: The Laplacian of u is 0 for all x in U",
    "¬Q: The function u is not infinitely differentiable on U"
]

N_HYP = 2
NEG_Q_INDEX = 2