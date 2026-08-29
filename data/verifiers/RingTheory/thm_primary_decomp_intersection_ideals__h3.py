import sympy
from sympy import symbols, groebner, reduced, Dummy

# Top-level setup for witness expressions
x, y, z = symbols('x y z')

def ideal_intersection(A, B, vars):
    A = [a for a in A if a != 0] or [0]
    B = [b for b in B if b != 0] or [0]
    if A == [0] or B == [0]:
        return [0]
    t = Dummy('t')
    tA = [t * a for a in A]
    t1B = [(1 - t) * b for b in B]
    G = groebner(tA + t1B, t, *vars, order='lex')
    res = [g for g in G if t not in g.free_symbols]
    return res or [0]

def ideal_subset(A, B, vars):
    A = [a for a in A if a != 0] or [0]
    B = [b for b in B if b != 0] or [0]
    if B == [0]:
        return A == [0]
    if A == [0]:
        return True
    G = groebner(B, *vars)
    for a in A:
        _, rem = reduced(a, G, *vars)
        if rem != 0:
            return False
    return True

def ideal_equal(A, B, vars):
    return ideal_subset(A, B, vars) and ideal_subset(B, A, vars)

def conditions(witness):
    try:
        vars = witness['vars']
        I = witness['I']
        J = witness['J']
        P_list = witness['J_primary_decomp']
        Q_list = witness.get('I_primary_decomp', [])
    except Exception:
        return [False, False, False, False]

    try:
        # H_1: R is a commutative ring
        # Implicitly true for polynomial rings over fields in SymPy
        h1 = True
    except Exception:
        h1 = False

    try:
        # H_2: I and J are ideals of R
        h2 = isinstance(I, (list, tuple)) and isinstance(J, (list, tuple))
    except Exception:
        h2 = False

    try:
        # H_3: J has a primary decomposition J = P_1 \cap \dots \cap P_m
        if not P_list:
            h3 = False
        else:
            intersect = P_list[0]
            for P in P_list[1:]:
                intersect = ideal_intersection(intersect, P, vars)
            h3 = ideal_equal(J, intersect, vars)
    except Exception:
        h3 = False

    try:
        # ¬Q: The intersection I \cap J does not admit a primary decomposition given by the intersection of all Q_i and P_k
        I_cap_J = ideal_intersection(I, J, vars)
        proposed_list = list(Q_list) + list(P_list)
        
        if not proposed_list:
            proposed_intersect = [1] # Whole ring
        else:
            proposed_intersect = proposed_list[0]
            for P in proposed_list[1:]:
                proposed_intersect = ideal_intersection(proposed_intersect, P, vars)
        
        # If the proposed intersection does not equal I \cap J, the conclusion fails.
        neg_q = not ideal_equal(I_cap_J, proposed_intersect, vars)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "H_3: J has a primary decomposition J = P_1 \\cap \\dots \\cap P_m",
    "¬Q: The intersection I \\cap J does not admit a primary decomposition given by the intersection of all Q_i and P_k"
]

N_HYP = 3
NEG_Q_INDEX = 3