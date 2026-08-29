import sympy
from sympy import symbols, Poly, expand, sympify, groebner, Symbol

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f and g are polynomials over R",
    "H_3: The content ideal c(f) is equal to the unit ideal R",
    "¬Q: The content ideal c(fg) is not equal to the content ideal c(g)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def extract_witness(witness):
    f, g, x, relations = None, None, None, []
    if isinstance(witness, dict):
        f = witness.get('f')
        g = witness.get('g')
        x = witness.get('x')
        relations = witness.get('relations', [])
    elif isinstance(witness, (list, tuple)):
        if len(witness) >= 2:
            f = witness[0]
            g = witness[1]
        if len(witness) >= 3:
            x = witness[2]
        if len(witness) >= 4:
            relations = witness[3]
            
    f = sympify(f)
    g = sympify(g)
    if x is not None:
        x = sympify(x)
    if not isinstance(relations, (list, tuple, set)):
        relations = [relations]
    relations = [sympify(r) for r in relations]
            
    if x is None and f is not None and g is not None:
        f_vars = getattr(f, 'free_symbols', set())
        g_vars = getattr(g, 'free_symbols', set())
        for s in f_vars | g_vars:
            if s.name == 'x':
                x = s
                break
        if x is None:
            rel_vars = set()
            for r in relations:
                rel_vars.update(getattr(r, 'free_symbols', set()))
            fg_vars = (f_vars | g_vars) - rel_vars
            if fg_vars:
                x = list(fg_vars)[0]
            else:
                x = Symbol('x')
                
    return f, g, x, relations

def in_ideal(element, generators, relations):
    element = sympify(element)
    gens = [sympify(g) for g in generators if sympify(g) != 0]
    rels = [sympify(r) for r in relations if sympify(r) != 0]
    
    all_gens = gens + rels
    
    if not all_gens:
        return element.is_zero or element == 0
        
    vars_set = set()
    for g in all_gens:
        if hasattr(g, 'free_symbols'):
            vars_set.update(g.free_symbols)
    if hasattr(element, 'free_symbols'):
        vars_set.update(element.free_symbols)
    vars_list = list(vars_set)
    
    if not vars_list:
        from sympy import gcd
        if all(g.is_Integer for g in all_gens) and element.is_Integer:
            g_gcd = all_gens[0]
            for g in all_gens[1:]:
                g_gcd = gcd(g_gcd, g)
            return element % g_gcd == 0
        else:
            return any(g != 0 for g in all_gens) or element == 0
        
    try:
        gb = groebner(all_gens, *vars_list, domain='ZZ')
        return gb.reduce(element)[1] == 0
    except Exception:
        try:
            gb = groebner(all_gens, *vars_list)
            return gb.reduce(element)[1] == 0
        except Exception:
            return False

def ideal_eq(gens1, gens2, relations):
    for g in gens1:
        if not in_ideal(g, gens2, relations):
            return False
    for g in gens2:
        if not in_ideal(g, gens1, relations):
            return False
    return True

def conditions(witness):
    try:
        f, g, x, relations = extract_witness(witness)
        if f is None or g is None:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    try:
        all_exprs = [f, g] + relations
        h1 = True
        for expr in all_exprs:
            if hasattr(expr, 'free_symbols'):
                if any(s.is_commutative is False for s in expr.free_symbols):
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        f_poly = Poly(f, x)
        g_poly = Poly(g, x)
        h2 = True
    except Exception:
        h2 = False

    try:
        f_coeffs = f_poly.coeffs()
        h3 = in_ideal(1, f_coeffs, relations)
    except Exception:
        h3 = False

    try:
        fg = expand(f * g)
        fg_poly = Poly(fg, x)
        fg_coeffs = fg_poly.coeffs()
        g_coeffs = g_poly.coeffs()
        
        q_holds = ideal_eq(fg_coeffs, g_coeffs, relations)
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]