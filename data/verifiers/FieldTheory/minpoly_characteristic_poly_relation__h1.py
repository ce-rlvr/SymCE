import sympy
from sympy import Matrix, eye, zeros, Rational, Symbol, degree, sympify
import itertools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_minpoly(A, x):
    try:
        return A.minimal_polynomial(x)
    except Exception:
        pass
    try:
        return A.minpoly(x)
    except Exception:
        pass
    
    c = A.charpoly(x).as_expr()
    factors = sympy.factor_list(c)[1]
    
    bases = [f[0] for f in factors]
    max_mults = [f[1] for f in factors]
    
    ranges = [range(1, m + 1) for m in max_mults]
    
    best_poly = c
    best_deg = degree(c, x)
    
    I = eye(A.shape[0])
    
    for mults in itertools.product(*ranges):
        test_poly = sympy.Integer(1)
        for b, m in zip(bases, mults):
            test_poly *= b**m
        
        if degree(test_poly, x) <= best_deg:
            coeffs = sympy.Poly(test_poly, x).all_coeffs()
            val = zeros(A.shape[0], A.shape[1])
            A_pow = I
            for coeff in reversed(coeffs):
                val += coeff * A_pow
                A_pow = A_pow * A
            
            is_zero = True
            for i in range(A.shape[0]):
                for j in range(A.shape[1]):
                    if sympy.simplify(val[i, j]) != 0:
                        is_zero = False
                        break
                if not is_zero:
                    break
            
            if is_zero:
                best_poly = test_poly
                best_deg = degree(test_poly, x)
                
    return best_poly

def conditions(witness):
    x = Symbol('x')
    alpha = None
    m_wit = None
    c_wit = None

    if isinstance(witness, dict):
        alpha = witness.get('alpha', witness.get('A'))
        m_wit = witness.get('m')
        c_wit = witness.get('c')
    elif isinstance(witness, tuple):
        alpha = witness[0]
        if len(witness) > 1:
            m_wit = witness[1]
        if len(witness) > 2:
            c_wit = witness[2]
    else:
        alpha = witness

    h1 = False
    try:
        if hasattr(alpha, 'shape') and len(alpha.shape) == 2 and alpha.shape[0] == alpha.shape[1]:
            h1 = True
    except Exception:
        pass

    h2 = False
    m = None
    try:
        if h1:
            m = get_minpoly(alpha, x)
            if m_wit is None:
                h2 = True
            else:
                if isinstance(m_wit, str):
                    m_wit = sympify(m_wit)
                syms = m_wit.free_symbols
                sym = list(syms)[0] if syms else x
                actual_m = get_minpoly(alpha, sym)
                if sympy.simplify(m_wit - actual_m) == 0:
                    h2 = True
                    m = m_wit
    except Exception:
        pass

    h3 = False
    c = None
    try:
        if h1:
            c = alpha.charpoly(x).as_expr()
            if c_wit is None:
                h3 = True
            else:
                if isinstance(c_wit, str):
                    c_wit = sympify(c_wit)
                syms = c_wit.free_symbols
                sym = list(syms)[0] if syms else x
                actual_c = alpha.charpoly(sym).as_expr()
                if sympy.simplify(c_wit - actual_c) == 0:
                    h3 = True
                    c = c_wit
    except Exception:
        pass

    neg_q = False
    try:
        if h1 and h2 and h3:
            n = alpha.shape[0]
            syms = m.free_symbols if m is not None else set()
            sym = list(syms)[0] if syms else x
            m_deg = degree(m, sym)
            
            if m_deg == 0:
                neg_q = True
            else:
                deg_val = Rational(n, m_deg)
                if not deg_val.is_integer:
                    neg_q = True
                else:
                    expected_c = m ** deg_val
                    c_syms = c.free_symbols if c is not None else set()
                    c_sym = list(c_syms)[0] if c_syms else sym
                    expected_c = expected_c.subs(sym, c_sym)
                    diff = sympy.simplify(c - expected_c)
                    if diff != 0:
                        neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is an element of E",
    "H_2: m is the minimal polynomial of alpha over F",
    "H_3: c is the characteristic polynomial of the F-linear transformation",
    "neg_Q: c is not equal to m raised to the degree of E over F adjoin alpha"
]

N_HYP = 3
NEG_Q_INDEX = 3