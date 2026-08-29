import sympy
from sympy import sympify, MatrixBase, Expr, Symbol, Integer
from sympy.abc import x

def is_divisible(p, q):
    if q == 0:
        return p == 0
    if p == 0:
        return True
    try:
        if isinstance(p, int) and isinstance(q, int):
            return p % q == 0
        p = sympify(p)
        q = sympify(q)
        if p.is_Integer and q.is_Integer:
            return p % q == 0
        
        q_poly, r_poly = sympy.div(p, q)
        if r_poly == 0:
            return True
    except Exception:
        pass
    
    try:
        ratio = sympy.cancel(p / q)
        num, den = ratio.as_numer_denom()
        if p.free_symbols or q.free_symbols:
            return den.is_number
        else:
            return abs(den) == 1
    except Exception:
        return False

def are_associates(p, q):
    return is_divisible(p, q) and is_divisible(q, p)

def conditions(witness):
    a = b = m = d = None
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            m = witness.get('m')
            d = witness.get('d')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                a, b, m, d = witness
            elif len(witness) == 5:
                _, a, b, m, d = witness
    except Exception:
        pass

    if a is None or b is None or m is None or d is None:
        return [False, False, False, False]

    # H_1: R is a principal ideal domain
    # We assume the domain is either ZZ or QQ[x], both of which are PIDs.
    # We verify that the provided elements are valid ring elements (scalars/polynomials, not matrices).
    try:
        a_sym = sympify(a)
        b_sym = sympify(b)
        m_sym = sympify(m)
        d_sym = sympify(d)
        
        def is_valid_ring_elem(val):
            return isinstance(val, (int, Integer, Symbol, Expr)) and not isinstance(val, MatrixBase)
            
        h1 = all(is_valid_ring_elem(val) for val in (a_sym, b_sym, m_sym, d_sym))
    except Exception:
        h1 = False

    # H_2: a and b are non-zero elements of R
    try:
        h2 = (a_sym != 0) and (b_sym != 0)
    except Exception:
        h2 = False

    # H_3: m is a least common multiple of a and b
    try:
        is_mult = is_divisible(m_sym, a_sym) and is_divisible(m_sym, b_sym)
        std_lcm = sympy.lcm(a_sym, b_sym)
        is_least = is_divisible(std_lcm, m_sym)
        h3 = is_mult and is_least
    except Exception:
        h3 = False

    # ¬Q: The product ab is not associate to the product dm in R
    try:
        ab = a_sym * b_sym
        dm = d_sym * m_sym
        neg_q = not are_associates(ab, dm)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: a and b are non-zero elements of R",
    "H_3: m is a least common multiple of a and b",
    "¬Q: The product ab is not associate to the product dm in R"
]

N_HYP = 3
NEG_Q_INDEX = 3