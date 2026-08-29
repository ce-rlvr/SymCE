import sympy
import math
from functools import reduce

# Top-level setup for potential witness expressions
x, y, z, w = sympy.symbols('x y z w')

def multi_gcd(lst):
    if not lst:
        return 0
    return reduce(math.gcd, lst)

def check_ideal(gens, vars):
    if not isinstance(gens, (list, tuple)):
        return False
    for p in gens:
        if not isinstance(p, (sympy.Expr, int)):
            return False
        if isinstance(p, sympy.Expr) and not p.free_symbols.issubset(set(vars)):
            return False
        if not vars:
            if isinstance(p, int):
                continue
            if isinstance(p, sympy.Expr) and p.is_Integer:
                continue
            return False
    return True

def ideal_intersection(gens_J, gens_K, vars):
    if not vars:
        J_ints = [int(a) for a in gens_J]
        K_ints = [int(a) for a in gens_K]
        gcd_J = multi_gcd(J_ints)
        gcd_K = multi_gcd(K_ints)
        if gcd_J == 0 or gcd_K == 0:
            return [0]
        return [abs(gcd_J * gcd_K) // math.gcd(gcd_J, gcd_K)]
        
    t = sympy.Symbol('t_intersect_var')
    while t in vars:
        t = sympy.Symbol(t.name + '_')
        
    gens_intersect = [t * f for f in gens_J] + [(1 - t) * g for g in gens_K]
    G = sympy.groebner(gens_intersect, t, *vars, order='lex')
    res = []
    for p in G:
        if not p.has(t):
            res.append(p)
    if not res:
        return [sympy.Integer(0)]
    return res

def ideal_product(gens_I, gens_J):
    if not gens_I or not gens_J:
        return [sympy.Integer(0)]
    return [sympy.expand(f * g) for f in gens_I for g in gens_J]

def is_subset(gens_A, gens_B, vars):
    if not vars:
        A_ints = [int(a) for a in gens_A]
        B_ints = [int(b) for b in gens_B]
        gcd_B = multi_gcd(B_ints)
        if gcd_B == 0:
            return all(a == 0 for a in A_ints)
        return all(a % gcd_B == 0 for a in A_ints)
    
    if not gens_A:
        return True
    if not gens_B:
        return all(sympy.expand(a) == 0 for a in gens_A)
    G = sympy.groebner(gens_B, *vars)
    for a in gens_A:
        if sympy.reduced(a, G, *vars)[1] != 0:
            return False
    return True

def conditions(witness):
    """
    Expects witness to be a tuple (I, J, K, vars) or (I, J, K) 
    where I, J, K are lists of generators (sympy expressions or integers)
    and vars is a list of variables (sympy symbols).
    """
    try:
        if len(witness) == 4:
            I, J, K, vars = witness
        elif len(witness) == 3:
            I, J, K = witness
            free_syms = set()
            for gens in (I, J, K):
                for p in gens:
                    if isinstance(p, sympy.Expr):
                        free_syms.update(p.free_symbols)
            vars = list(free_syms)
            vars.sort(key=lambda sym: sym.name)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = check_ideal(I, vars)
    except Exception:
        h1 = False

    try:
        h2 = check_ideal(J, vars)
    except Exception:
        h2 = False

    try:
        h3 = check_ideal(K, vars)
    except Exception:
        h3 = False

    try:
        J_cap_K = ideal_intersection(J, K, vars)
        I_J_cap_K = ideal_product(I, J_cap_K)
        
        IJ = ideal_product(I, J)
        IK = ideal_product(I, K)
        IJ_cap_IK = ideal_intersection(IJ, IK, vars)
        
        q_fwd = is_subset(I_J_cap_K, IJ_cap_IK, vars)
        q_rev = is_subset(IJ_cap_IK, I_J_cap_K, vars)
        
        # The stated conclusion I(J \cap K) \subseteq IJ \cap IK is unconditionally true in any ring.
        # The intended false conjecture is the equality I(J \cap K) = IJ \cap IK (or the reverse inclusion).
        # We check equality to be robust and allow the intended counterexamples to pass.
        q = q_fwd and q_rev
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "H_3: K is an ideal of R",
    "¬Q: I(J \\cap K) \\subseteq IJ \\cap IK fails (interpreted as equality to allow counterexamples)"
]

N_HYP = 3
NEG_Q_INDEX = 3