import sympy as sp
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference
x, y, z = sp.symbols('x y z')
Reals = sp.S.Reals

CONDITION_LABELS = [
    "H_1: f is a function defined on U and a in U",
    "H_2: f has a local maximum or local minimum at a",
    "H_3: f is differentiable at a",
    "¬Q: The gradient of f at a is not the zero vector"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            U = witness.get('U')
            a = witness.get('a')
            vars = witness.get('vars')
            if vars is None:
                f_sym = sp.sympify(f)
                vars = list(f_sym.free_symbols)
                if not vars:
                    vars = [x]
                vars = sorted(vars, key=lambda v: v.name)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 4:
                f, U, a, vars = witness
            elif len(witness) == 3:
                f, U, a = witness
                f_sym = sp.sympify(f)
                vars = list(f_sym.free_symbols)
                if not vars:
                    vars = [x]
                vars = sorted(vars, key=lambda v: v.name)
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if not isinstance(vars, (list, tuple)):
            vars = [vars]
            
        if not isinstance(a, (list, tuple)):
            a_tuple = (a,)
        else:
            a_tuple = tuple(a)
            
    except Exception:
        return [False, False, False, False]

    # H1: f is a function defined on U and a in U
    try:
        f = sp.sympify(f)
        if not isinstance(f, sp.Expr):
            H1 = False
        elif not isinstance(U, sp.Set):
            H1 = False
        else:
            if len(a_tuple) > 1:
                in_U = U.contains(sp.Tuple(*a_tuple)) == True
            else:
                in_U = U.contains(a_tuple[0]) == True
            H1 = in_U
    except Exception:
        H1 = False

    # H2: f has a local maximum or local minimum at a
    try:
        epsilons = [10**(-i) for i in range(2, 6)]
        pts = []
        if len(a_tuple) > 1:
            for eps in epsilons:
                for i in range(len(a_tuple)):
                    p1 = list(a_tuple)
                    p1[i] = float(p1[i]) - eps
                    if U.contains(sp.Tuple(*p1)) == True:
                        pts.append(p1)
                    p2 = list(a_tuple)
                    p2[i] = float(p2[i]) + eps
                    if U.contains(sp.Tuple(*p2)) == True:
                        pts.append(p2)
        else:
            for eps in epsilons:
                p1 = float(a_tuple[0]) - eps
                if U.contains(p1) == True:
                    pts.append((p1,))
                p2 = float(a_tuple[0]) + eps
                if U.contains(p2) == True:
                    pts.append((p2,))
                    
        val_a = float(f.subs(zip(vars, a_tuple)))
        is_max = True
        is_min = True
        for p in pts:
            val_p = float(f.subs(zip(vars, p)))
            if val_p > val_a + 1e-12:
                is_max = False
            if val_p < val_a - 1e-12:
                is_min = False
        H2 = is_max or is_min
    except Exception:
        H2 = False

    # H3: f is differentiable at a
    try:
        grads = []
        val_a = float(f.subs(zip(vars, a_tuple)))
        for i, v in enumerate(vars):
            df = sp.diff(f, v)
            df_a = df.subs(zip(vars, a_tuple))
            val = float(df_a)
            if math.isnan(val) or math.isinf(val):
                raise ValueError("Not differentiable")
            
            h = 1e-8
            p_plus = list(a_tuple)
            p_plus[i] = float(p_plus[i]) + h
            p_minus = list(a_tuple)
            p_minus[i] = float(p_minus[i]) - h
            
            if len(a_tuple) > 1:
                in_plus = U.contains(sp.Tuple(*p_plus)) == True
                in_minus = U.contains(sp.Tuple(*p_minus)) == True
            else:
                in_plus = U.contains(p_plus[0]) == True
                in_minus = U.contains(p_minus[0]) == True
                
            if in_plus and in_minus:
                v_plus = float(f.subs(zip(vars, p_plus)))
                v_minus = float(f.subs(zip(vars, p_minus)))
                grad_plus = (v_plus - val_a) / h
                grad_minus = (val_a - v_minus) / h
                if abs(grad_plus - grad_minus) > 1e-3:
                    raise ValueError("Not differentiable")
                grad_val = val
            elif in_plus:
                v_plus = float(f.subs(zip(vars, p_plus)))
                grad_plus = (v_plus - val_a) / h
                if abs(grad_plus - val) > 1e-3:
                    grad_val = grad_plus
                else:
                    grad_val = val
            elif in_minus:
                v_minus = float(f.subs(zip(vars, p_minus)))
                grad_minus = (val_a - v_minus) / h
                if abs(grad_minus - val) > 1e-3:
                    grad_val = grad_minus
                else:
                    grad_val = val
            else:
                grad_val = val
                
            grads.append(grad_val)
        H3 = True
    except Exception:
        H3 = False

    # neg_Q: The gradient of f at a is not the zero vector
    try:
        if H3:
            neg_Q = any(abs(g) > 1e-7 for g in grads)
        else:
            neg_Q = False
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]