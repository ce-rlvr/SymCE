import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f is a polynomial over F",
    "H_2: K is the splitting field of f over F",
    "H_3: sigma is a field automorphism of K fixing F",
    "H_4: alpha in K is a root of f",
    "¬Q: sigma applied to alpha is NOT a root of f"
]

N_HYP = 4
NEG_Q_INDEX = 4

def get_attr_or_key(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
    if hasattr(obj, key):
        return getattr(obj, key)
    return None

def evaluate_poly(f_expr, val):
    if isinstance(f_expr, sp.Poly):
        expr = f_expr.as_expr()
    else:
        expr = f_expr
    free_syms = list(expr.free_symbols)
    x = free_syms[0] if free_syms else sp.Symbol('x')
    
    if isinstance(val, sp.MatrixBase):
        if not isinstance(f_expr, sp.Poly):
            f_poly = sp.Poly(f_expr, x)
        else:
            f_poly = f_expr
        coeffs = f_poly.all_coeffs()
        degree = len(coeffs) - 1
        res = sp.zeros(val.rows, val.cols)
        for i, c in enumerate(coeffs):
            power = degree - i
            if power == 0:
                res += c * sp.eye(val.rows)
            else:
                res += c * (val ** power)
        return res
    else:
        res = expr.subs(x, val)
        if hasattr(res, 'doit'):
            res = res.doit()
        return res

def conditions(witness):
    f_expr = get_attr_or_key(witness, 'f')
    F = get_attr_or_key(witness, 'F')
    K = get_attr_or_key(witness, 'K')
    sigma = get_attr_or_key(witness, 'sigma')
    alpha = get_attr_or_key(witness, 'alpha')

    # H_1: f is a polynomial over F
    try:
        if f_expr is None or F is None:
            h1 = False
        else:
            if isinstance(f_expr, sp.Poly):
                f_poly = f_expr
            else:
                free_syms = list(f_expr.free_symbols)
                x = free_syms[0] if free_syms else sp.Symbol('x')
                f_poly = sp.Poly(f_expr, x)
            coeffs = f_poly.coeffs()
            
            if hasattr(F, '__contains__'):
                h1 = all(c in F for c in coeffs)
            else:
                h1 = True
    except Exception:
        h1 = False

    # H_2: K is the splitting field of f over F
    try:
        if K is None:
            h2 = False
        else:
            is_split = get_attr_or_key(witness, 'is_splitting_field')
            if is_split is not None:
                h2 = bool(is_split)
            else:
                h2 = True
    except Exception:
        h2 = False

    # H_3: sigma is a field automorphism of K fixing F
    try:
        if sigma is None:
            h3 = False
        else:
            fixes_F = True
            if F is not None and hasattr(F, '__iter__') and not isinstance(F, sp.Domain):
                elements_to_check = F
            else:
                if isinstance(f_expr, sp.Poly):
                    coeffs_to_check = f_expr.coeffs()
                else:
                    free_syms = list(f_expr.free_symbols)
                    x = free_syms[0] if free_syms else sp.Symbol('x')
                    coeffs_to_check = sp.Poly(f_expr, x).coeffs()
                elements_to_check = coeffs_to_check
                
            for a in elements_to_check:
                if callable(sigma):
                    val = sigma(a)
                elif isinstance(sigma, dict):
                    val = sigma.get(a, a)
                else:
                    val = a
                
                diff = val - a
                if hasattr(diff, 'simplify'):
                    diff = sp.simplify(diff)
                if isinstance(diff, sp.MatrixBase):
                    if not diff.is_zero_matrix:
                        fixes_F = False
                        break
                elif diff != 0:
                    fixes_F = False
                    break
            
            is_auto = True
            if K is not None and hasattr(K, '__iter__') and not isinstance(K, sp.Domain):
                mapped_K = []
                for k in K:
                    if callable(sigma):
                        mapped_K.append(sigma(k))
                    elif isinstance(sigma, dict):
                        mapped_K.append(sigma.get(k, k))
                    else:
                        mapped_K.append(k)
                try:
                    if len(set(mapped_K)) != len(list(K)):
                        is_auto = False
                except TypeError:
                    pass
            
            h3 = fixes_F and is_auto
    except Exception:
        h3 = False

    # H_4: alpha in K is a root of f
    try:
        if alpha is None or f_expr is None:
            h4 = False
        else:
            in_K = True
            if K is not None and hasattr(K, '__contains__') and not isinstance(K, sp.Domain):
                in_K = alpha in K
                
            val = evaluate_poly(f_expr, alpha)
            if hasattr(val, 'simplify'):
                val = sp.simplify(sp.expand(val))
            if isinstance(val, sp.MatrixBase):
                is_root = val.is_zero_matrix
            else:
                is_root = (val == 0)
            
            h4 = in_K and is_root
    except Exception:
        h4 = False

    # ¬Q: sigma applied to alpha is NOT a root of f
    try:
        if alpha is None or sigma is None or f_expr is None:
            neg_q = False
        else:
            if callable(sigma):
                sigma_alpha = sigma(alpha)
            elif isinstance(sigma, dict):
                sigma_alpha = sigma.get(alpha, alpha)
            else:
                sigma_alpha = alpha
                
            val_sigma = evaluate_poly(f_expr, sigma_alpha)
            if hasattr(val_sigma, 'simplify'):
                val_sigma = sp.simplify(sp.expand(val_sigma))
            if isinstance(val_sigma, sp.MatrixBase):
                neg_q = not val_sigma.is_zero_matrix
            else:
                neg_q = (val_sigma != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]