import sympy
from sympy import Poly, Matrix, eye, zeros, factor_list, simplify, minpoly
from sympy import QQ, ZZ
from sympy.abc import x

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero(obj):
    try:
        if hasattr(obj, 'is_zero_matrix') and obj.is_zero_matrix:
            return True
        if hasattr(obj, 'is_zero') and obj.is_zero:
            return True
        if isinstance(obj, (list, tuple)):
            return all(is_zero(item) for item in obj)
        return simplify(obj) == 0
    except Exception:
        return False

def in_domain(c, domain):
    try:
        if c in domain:
            return True
    except Exception:
        pass
    try:
        if domain.from_sympy(c) is not None:
            return True
    except Exception:
        pass
    return False

def eval_poly(m, alpha, x_sym):
    p = Poly(m, x_sym)
    coeffs = p.all_coeffs()
    d = p.degree()
    
    if isinstance(alpha, Matrix):
        n = alpha.shape[0]
        I = eye(n)
        res = coeffs[-1] * I
        curr_pow = alpha
        for i in range(1, d + 1):
            res += coeffs[-(i + 1)] * curr_pow
            if i < d:
                curr_pow = curr_pow * alpha
        return res
    else:
        return m.subs(x_sym, alpha)

def check_linear_independence(powers):
    flat_powers = [list(p) for p in powers]
    M = Matrix(flat_powers)
    return M.rank() == len(powers)

def conditions(witness) -> list[bool]:
    F = witness.get('F')
    K = witness.get('K')
    alpha = witness.get('alpha')
    m = witness.get('m')
    x_sym = witness.get('x', x)
    
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False
        
    try:
        k_is_field = getattr(K, 'is_Field', False)
        h2 = bool(k_is_field and (F == K or (hasattr(K, 'has_subring') and K.has_subring(F)) or str(F) in str(K)))
    except Exception:
        h2 = False
        
    try:
        p = Poly(m, x_sym)
        d = p.degree()
        
        coeffs_in_F = all(in_domain(c, F) for c in p.all_coeffs())
        is_monic = (p.LC() == 1)
        
        is_least = False
        if d > 0 and coeffs_in_F and is_monic:
            m_alpha = eval_poly(m, alpha, x_sym)
            if is_zero(m_alpha):
                if isinstance(alpha, Matrix):
                    powers = [eye(alpha.shape[0])]
                    for _ in range(1, d):
                        powers.append(powers[-1] * alpha)
                    is_least = check_linear_independence(powers)
                else:
                    mp = minpoly(alpha, x_sym)
                    is_least = (Poly(mp, x_sym).degree() == d)
        h3 = bool(d > 0 and coeffs_in_F and is_monic and is_least)
    except Exception:
        h3 = False
        
    try:
        factors = factor_list(m, domain=F)[1]
        is_irreducible = (len(factors) == 1 and factors[0][1] == 1 and Poly(factors[0][0], x_sym).degree() == p.degree())
        neg_q = not is_irreducible
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is an extension field of F",
    "H_3: m(x) is the monic polynomial over F of least positive degree such that m(alpha) = 0",
    "¬Q: m(x) is not irreducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3