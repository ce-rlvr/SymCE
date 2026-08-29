import sympy as sp
import itertools
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # Check if witness is a dictionary of properties (e.g., for infinite-dimensional counterexamples)
    if isinstance(witness, dict) and 'is_C2' in witness:
        try:
            h1 = bool(witness.get('is_C2', False))
            h2 = bool(witness.get('is_critical_point', False))
            h3 = bool(witness.get('is_hessian_positive_definite', False))
            neg_q = not bool(witness.get('is_strict_local_minimum', True))
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # Check if witness is an object with methods
    if hasattr(witness, 'is_C2') and callable(getattr(witness, 'is_C2')):
        try:
            h1 = bool(witness.is_C2())
            h2 = bool(witness.is_critical_point())
            h3 = bool(witness.is_hessian_positive_definite())
            neg_q = not bool(witness.is_strict_local_minimum())
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # Extract f, a, U from tuple or object for finite-dimensional SymPy expressions
    f = None
    a = None
    U = None
    if isinstance(witness, tuple) and len(witness) >= 2:
        f = witness[0]
        a = witness[1]
        if len(witness) > 2:
            U = witness[2]
    elif hasattr(witness, 'f') and hasattr(witness, 'a'):
        f = witness.f
        a = witness.a
        if hasattr(witness, 'U'):
            U = witness.U

    if f is not None and a is not None:
        try:
            if isinstance(a, dict):
                vars = list(a.keys())
                a_dict = a
            else:
                vars = list(f.free_symbols)
                vars.sort(key=lambda x: x.name)
                a_dict = dict(zip(vars, a))
                
            # H1: f is C^2
            try:
                hess = sp.hessian(f, vars)
                h1 = True
            except Exception:
                h1 = False
                
            # H2: grad f(a) = 0
            try:
                grad = [sp.diff(f, v) for v in vars]
                grad_val = [g.subs(a_dict).evalf() for g in grad]
                h2 = True
                for gv in grad_val:
                    if not bool(sp.Abs(gv) < 1e-9):
                        h2 = False
                        break
            except Exception:
                h2 = False
                
            # H3: Hessian is positive definite
            try:
                hess_val = hess.subs(a_dict)
                if hasattr(hess_val, 'is_positive_definite') and hess_val.is_positive_definite:
                    h3 = True
                else:
                    eigenvals = hess_val.eigenvals()
                    h3 = True
                    for ev in eigenvals:
                        if not bool(sp.re(ev) > 0):
                            h3 = False
                            break
            except Exception:
                h3 = False
                
            # ¬Q: f does not have a strict local minimum at a
            try:
                is_strict_min = True
                val_a = f.subs(a_dict).evalf()
                deltas = [-1e-3, -1e-4, 1e-4, 1e-3]
                for d in itertools.product(deltas + [0], repeat=len(vars)):
                    if all(x == 0 for x in d):
                        continue
                    pt = {v: a_dict[v] + d[i] for i, v in enumerate(vars)}
                    if U is not None and hasattr(U, 'contains'):
                        if not U.contains(pt):
                            continue
                    val_pt = f.subs(pt).evalf()
                    if bool(val_pt <= val_a):
                        is_strict_min = False
                        break
                neg_q = not is_strict_min
            except Exception:
                neg_q = False
                
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: f is a twice continuously differentiable (C^2) function",
    "H_2: a is a critical point of f (grad f(a) = 0)",
    "H_3: The Hessian matrix H_f(a) is positive definite",
    "¬Q: f does not have a strict local minimum at a"
]

N_HYP = 3
NEG_Q_INDEX = 3