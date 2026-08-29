import sympy
from sympy import Poly, GF, groebner, reduced
from sympy.abc import a, b, c, d, x, y, z, t, u, v, w

def get_components(p, vars, degrees, grading_mod, char):
    domain = GF(char) if char > 0 else 'QQ'
    poly = Poly(p, *vars, domain=domain)
    
    components = {}
    for monom, coeff in poly.terms():
        deg = sum(m * d for m, d in zip(monom, degrees))
        if grading_mod > 0:
            deg = deg % grading_mod
        if deg not in components:
            components[deg] = 0
        
        if char > 0:
            term_expr = int(coeff)
        else:
            term_expr = sympy.sympify(coeff)
            
        for var, m in zip(vars, monom):
            term_expr *= var**m
        components[deg] += term_expr
    return components

def is_homogeneous(p, vars, degrees, grading_mod, char):
    comps = get_components(p, vars, degrees, grading_mod, char)
    return len(comps) <= 1

def is_nilpotent(p, I, vars, char, max_n=30):
    domain = GF(char) if char > 0 else 'QQ'
    if not I:
        poly = Poly(p, *vars, domain=domain)
        return poly.is_zero
        
    G = [poly.as_expr() for poly in groebner(I, *vars, domain=domain)]
    
    curr_expr = p
    rem = reduced(curr_expr, G, *vars, domain=domain)[1]
    if Poly(rem, *vars, domain=domain).is_zero:
        return True
        
    base_expr = rem
    curr_expr = rem
    for _ in range(2, max_n + 1):
        curr_expr = curr_expr * base_expr
        rem = reduced(curr_expr, G, *vars, domain=domain)[1]
        curr_expr = rem
        if Poly(rem, *vars, domain=domain).is_zero:
            return True
            
    return False

def conditions(witness):
    """
    witness is expected to be a dictionary with:
      - 'vars': list of SymPy symbols
      - 'I': list of polynomials generating the ideal
      - 'x': the element to test (SymPy expression)
      - 'degrees': list of integer degrees corresponding to 'vars'
      - 'grading_mod': integer modulus for the grading group (e.g., 2 for Z/2Z). 0 for Z-grading.
      - 'char': characteristic of the base field (e.g., 2 for GF(2)). 0 for QQ.
    """
    try:
        vars = witness['vars']
        I = witness['I']
        x_elem = witness['x']
        degrees = witness['degrees']
        grading_mod = witness.get('grading_mod', 0)
        char = witness.get('char', 0)
    except Exception:
        return [False, False, False]

    # H1: R is a commutative graded ring
    try:
        h1 = all(is_homogeneous(g, vars, degrees, grading_mod, char) for g in I)
    except Exception:
        h1 = False

    # H2: x is a nilpotent element of R
    try:
        h2 = is_nilpotent(x_elem, I, vars, char)
    except Exception:
        h2 = False

    # neg_Q: Each homogeneous component x_i is a nilpotent element of R (Negated)
    try:
        comps = get_components(x_elem, vars, degrees, grading_mod, char)
        neg_q = False
        for deg, xi in comps.items():
            if not is_nilpotent(xi, I, vars, char):
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative graded ring",
    "H_2: x is a nilpotent element of R",
    "¬Q: At least one homogeneous component of x is not nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2