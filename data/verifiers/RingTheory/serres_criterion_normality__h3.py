import sympy
import itertools

# Top-level setup for potential witness expressions
x, y, z, w, u, v = sympy.symbols('x y z w u v')

def ideal_dimension(I, vars):
    """
    Computes the Krull dimension of the affine ring k[vars]/I.
    Returns -1 if the ideal is the whole ring.
    """
    I = [f for f in I if f != 0]
    if not I:
        return len(vars)
    try:
        G = sympy.groebner(I, *vars, order='grevlex')
    except Exception:
        return -1
    if list(G) == [1]:
        return -1
    
    LT_vars = []
    for p in G.polys:
        if p.is_zero:
            continue
        lm = p.lead_monom()
        v_set = set(vars[i] for i, e in enumerate(lm) if e > 0)
        LT_vars.append(v_set)
        
    for d in range(len(vars), -1, -1):
        for subset in itertools.combinations(vars, d):
            subset_set = set(subset)
            independent = True
            for v_set in LT_vars:
                if v_set.issubset(subset_set):
                    independent = False
                    break
            if independent:
                return d
    return -1

def satisfies_R1(vars, I_gens):
    """
    Checks Serre's condition (R1) for the affine ring k[vars]/I_gens.
    (R1) holds if the singular locus has codimension >= 2.
    """
    d = ideal_dimension(I_gens, vars)
    if d == -1:
        return True
    
    n = len(vars)
    c = n - d
    if c <= 0:
        return True
    
    J = []
    for f in I_gens:
        row = [sympy.diff(f, var) for var in vars]
        J.append(row)
    J = sympy.Matrix(J)
    
    minors = []
    if len(I_gens) >= c:
        for row_indices in itertools.combinations(range(len(I_gens)), c):
            for col_indices in itertools.combinations(range(n), c):
                submatrix = J[row_indices, col_indices]
                minors.append(submatrix.det())
                
    I_sing = list(I_gens) + minors
    dim_sing = ideal_dimension(I_sing, vars)
    
    if dim_sing == -1:
        return True
    return dim_sing <= d - 2

def is_normal(vars, I_gens):
    """
    A partial check for normality. A normal ring must be reduced, and if it is 
    connected (e.g. graded by positive degrees), it must be a domain.
    We check for obvious nilpotents and zero divisors among the variables.
    """
    try:
        G = sympy.groebner(I_gens, *vars, order='grevlex')
    except Exception:
        return True
        
    if list(G) == [1]:
        return True
        
    # Check for nilpotents among variables
    for var in vars:
        rem_v = sympy.reduced(var, G)[1]
        if rem_v != 0:
            rem_v2 = sympy.reduced(var**2, G)[1]
            if rem_v2 == 0:
                return False
                
    # Check for zero divisors among variables
    for i in range(len(vars)):
        for j in range(i+1, len(vars)):
            v1, v2 = vars[i], vars[j]
            if sympy.reduced(v1, G)[1] != 0 and sympy.reduced(v2, G)[1] != 0:
                if sympy.reduced(v1*v2, G)[1] == 0:
                    return False
                    
    # Check for nilpotents among sums of variables
    for i in range(len(vars)):
        for j in range(i+1, len(vars)):
            v_sum = vars[i] + vars[j]
            if sympy.reduced(v_sum, G)[1] != 0:
                if sympy.reduced(v_sum**2, G)[1] == 0:
                    return False

    return True

def conditions(witness):
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    The witness is expected to be a tuple: (list_of_vars, list_of_polynomials)
    representing the quotient ring k[vars] / (polynomials).
    """
    try:
        vars_list, I_gens = witness
        if not isinstance(vars_list, (list, tuple)) or not isinstance(I_gens, (list, tuple)):
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative Noetherian ring
    # Any quotient of a polynomial ring over a field by a finitely generated ideal is commutative Noetherian.
    try:
        h1 = True
        for f in I_gens:
            if not hasattr(f, 'free_symbols'):
                h1 = False
                break
    except Exception:
        h1 = False
        
    # H_2: R satisfies Serre's condition (R1)
    try:
        h2 = satisfies_R1(vars_list, I_gens)
    except Exception:
        h2 = False
        
    # neg_Q: R is NOT a normal ring
    try:
        neg_q = not is_normal(vars_list, I_gens)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: R satisfies Serre's condition (R1)",
    "¬Q: R is not a normal ring"
]

N_HYP = 2
NEG_Q_INDEX = 2