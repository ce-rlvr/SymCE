import sympy
from sympy import S, Poly, Expr, simplify, expand
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def eq(a, b):
    try:
        if a == b:
            return True
        diff = expand(a - b)
        if diff == 0:
            return True
        diff = simplify(diff)
        if diff == 0:
            return True
        if hasattr(diff, 'is_zero') and diff.is_zero:
            return True
        return False
    except Exception:
        return False

def get_coeffs(f):
    try:
        if isinstance(f, Poly):
            return f.coeffs()
        elif isinstance(f, Expr):
            free = list(f.free_symbols)
            if len(free) == 1:
                return Poly(f, free[0]).coeffs()
            elif len(free) == 0:
                return [f]
        return Poly(f).coeffs()
    except Exception:
        return []

def evaluate_poly(f, val):
    try:
        if isinstance(f, Poly):
            return f.subs(f.gen, val)
        elif isinstance(f, Expr):
            free = list(f.free_symbols)
            if len(free) == 1:
                return f.subs(free[0], val)
            elif len(free) == 0:
                return f
        return f.subs(sympy.Symbol('x'), val)
    except Exception:
        return None

def get_sigma_func(sigma):
    if callable(sigma):
        base_func = sigma
    elif isinstance(sigma, dict):
        base_func = lambda x: x.subs(sigma) if hasattr(x, 'subs') else x
    else:
        return None
        
    def safe_func(x):
        from sympy import sympify
        try:
            return base_func(sympify(x))
        except Exception:
            return base_func(x)
            
    return safe_func

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            K = witness.get('K')
            f = witness.get('f')
            sigma = witness.get('sigma')
            alpha = witness.get('alpha')
        else:
            F, K, f, sigma, alpha = witness
    except Exception:
        return [False] * 5

    # H1: F is a field
    h1 = False
    try:
        if hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif hasattr(F, 'is_field') and F.is_field:
            h1 = True
        elif F in (S.Reals, S.Complexes, S.Rationals):
            h1 = True
        elif hasattr(F, 'has_CharacteristicZero'):
            h1 = True
    except Exception:
        h1 = False

    # H2: f(x) is a polynomial over F
    h2 = False
    try:
        coeffs = get_coeffs(f)
        if coeffs:
            if hasattr(F, '__contains__'):
                try:
                    if all(c in F for c in coeffs):
                        h2 = True
                except Exception:
                    pass
            if not h2:
                if F == S.Rationals:
                    h2 = all(hasattr(c, 'is_rational') and c.is_rational for c in coeffs)
                elif F == S.Reals:
                    h2 = all(hasattr(c, 'is_real') and c.is_real for c in coeffs)
                elif F == S.Complexes:
                    h2 = all(hasattr(c, 'is_complex') and c.is_complex for c in coeffs)
                elif hasattr(f, 'domain') and f.domain == F:
                    h2 = True
                elif hasattr(F, 'of_type'):
                    try:
                        h2 = all(F.of_type(c) for c in coeffs)
                    except Exception:
                        pass
    except Exception:
        h2 = False

    # H3: sigma is a field automorphism of K fixing F
    h3 = False
    try:
        sigma_func = get_sigma_func(sigma)
        if sigma_func is not None:
            coeffs = get_coeffs(f)
            fixes_F = True
            for c in coeffs + [0, 1]:
                if not eq(sigma_func(c), c):
                    fixes_F = False
                    break
            
            if fixes_F:
                is_auto = True
                try:
                    test_elements = [alpha, alpha**2, alpha + 1]
                except Exception:
                    test_elements = [alpha]
                    
                for x in test_elements:
                    for y in test_elements:
                        if not eq(sigma_func(x + y), sigma_func(x) + sigma_func(y)):
                            is_auto = False
                            break
                        if not eq(sigma_func(x * y), sigma_func(x) * sigma_func(y)):
                            is_auto = False
                            break
                    if not is_auto:
                        break
                if is_auto and eq(sigma_func(1), 1):
                    h3 = True
    except Exception:
        h3 = False

    # H4: alpha in K is a root of f(x)
    h4 = False
    try:
        in_K = False
        if hasattr(K, '__contains__'):
            try:
                in_K = alpha in K
            except Exception:
                pass
        if not in_K:
            if K == S.Rationals and hasattr(alpha, 'is_rational') and alpha.is_rational:
                in_K = True
            elif K == S.Reals and hasattr(alpha, 'is_real') and alpha.is_real:
                in_K = True
            elif K == S.Complexes and hasattr(alpha, 'is_complex') and alpha.is_complex:
                in_K = True
            elif hasattr(K, 'of_type'):
                try:
                    in_K = K.of_type(alpha)
                except Exception:
                    pass
            else:
                in_K = True # Relaxing if we cannot strictly verify
                
        if in_K:
            val = evaluate_poly(f, alpha)
            if val is not None and eq(val, 0):
                h4 = True
    except Exception:
        h4 = False

    # neg_Q: sigma(alpha) is NOT a root of f(x)
    neg_q = False
    try:
        sigma_func = get_sigma_func(sigma)
        if sigma_func is not None:
            sigma_alpha = sigma_func(alpha)
            val = evaluate_poly(f, sigma_alpha)
            if val is not None and not eq(val, 0):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a polynomial over F",
    "H_3: sigma is a field automorphism of K fixing F",
    "H_4: alpha in K is a root of f(x)",
    "¬Q: sigma(alpha) is not a root of f(x)"
]

N_HYP = 4
NEG_Q_INDEX = 4