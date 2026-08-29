import sympy as sp
from sympy import symbols

# Top-level setup for the witness namespace
x, y, z, w = symbols('x y z w')

def intersect_ideals(A, B, vars):
    """
    Computes the intersection of two ideals A and B in the polynomial ring over vars.
    Ideals are represented as lists of generating polynomials.
    """
    t = sp.Symbol('_t_intersect_dummy_')
    # Intersection of A and B can be found by eliminating t from t*A + (1-t)*B
    gens = [t * a for a in A] + [(1 - t) * b for b in B]
    gb = sp.groebner(gens, *( [t] + list(vars) ), order='lex')
    res = []
    for p in gb:
        if t not in p.free_symbols:
            res.append(p)
    if not res:
        return [sp.Integer(0)]
    return res

def ideal_subset(A, B, vars):
    """
    Checks if ideal A is a subset of ideal B.
    """
    def is_zero(I):
        return not I or all(sp.expand(i) == 0 for i in I)
    
    if is_zero(A): 
        return True
    if is_zero(B): 
        return is_zero(A)
        
    gb = sp.groebner(B, *vars)
    G = list(gb)
    for a in A:
        _, rem = sp.reduced(a, G, *vars)
        if rem != 0:
            return False
    return True

def ideal_equal(A, B, vars):
    """
    Checks if ideal A is equal to ideal B.
    """
    return ideal_subset(A, B, vars) and ideal_subset(B, A, vars)

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness should be a dictionary containing:
      'vars': list of variables (e.g., [x, y])
      'I': list of generators for ideal I
      'J': list of generators for ideal J
      'Q': list of lists of generators for primary ideals Q_i
      'P': list of lists of generators for primary ideals P_k
    """
    try:
        vars = witness['vars']
        I = witness['I']
        J = witness['J']
        Q = witness['Q']
        P = witness['P']
    except Exception:
        return [False, False, False, False]
        
    # H_1: Let R be a commutative ring
    # Polynomial rings over fields (like QQ) are commutative rings.
    h1 = True
    
    # H_2: Let I and J be ideals of R
    # Represented as lists of polynomials, they validly generate ideals.
    h2 = True
    
    # H_3: Assume I has a primary decomposition I = Q_1 \cap \dots \cap Q_n
    try:
        if not Q:
            h3 = False
            int_Q = [sp.Integer(1)]
        else:
            int_Q = Q[0]
            for q in Q[1:]:
                int_Q = intersect_ideals(int_Q, q, vars)
            h3 = ideal_equal(I, int_Q, vars)
    except Exception:
        h3 = False
        int_Q = [sp.Integer(1)]
        
    # ¬Q: The intersection I \cap J does NOT admit a primary decomposition 
    # given by the intersection of all Q_i and P_k.
    # This holds if I \cap J != (\bigcap Q_i) \cap (\bigcap P_k).
    try:
        if not P:
            int_P = [sp.Integer(1)]
        else:
            int_P = P[0]
            for p in P[1:]:
                int_P = intersect_ideals(int_P, p, vars)
                
        int_I_J = intersect_ideals(I, J, vars)
        int_Q_P = intersect_ideals(int_Q, int_P, vars)
        
        neg_q = not ideal_equal(int_I_J, int_Q_P, vars)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "H_3: I has a primary decomposition I = Q_1 \\cap \\dots \\cap Q_n",
    "¬Q: The intersection I \\cap J does not admit a primary decomposition given by the intersection of all Q_i and P_k"
]

N_HYP = 3
NEG_Q_INDEX = 3