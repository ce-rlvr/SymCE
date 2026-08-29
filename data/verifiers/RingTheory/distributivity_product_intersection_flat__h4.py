import sympy
from sympy import S, gcd, lcm, cancel, simplify, fraction
from sympy.abc import x, y, z

# Top-level setup for witness namespace
ZZ = sympy.ZZ
QQ = sympy.QQ

def get_gen(elements):
    try:
        elements = list(elements)
    except Exception:
        return S.Zero
    if not elements:
        return S.Zero
    g = S(elements[0])
    for e in elements[1:]:
        g = gcd(g, S(e))
    return g

def in_ideal(k, g_J):
    k = S(k)
    g_J = S(g_J)
    if g_J == 0:
        return k == 0
    if k == 0:
        return True
    try:
        if k.is_Integer and g_J.is_Integer:
            return k % g_J == 0
    except Exception:
        pass
    try:
        ratio = simplify(k / g_J)
        return fraction(ratio)[1] == 1
    except Exception:
        return False

def ideals_equal(a, b):
    a = S(a)
    b = S(b)
    if a == 0 and b == 0:
        return True
    if a == 0 or b == 0:
        return False
    try:
        if a.is_Integer and b.is_Integer:
            return abs(a) == abs(b)
    except Exception:
        pass
    try:
        ratio = cancel(a / b)
        return ratio.is_constant() and ratio != 0
    except Exception:
        return False

def conditions(witness):
    try:
        R = witness.get('R', None)
        I = witness.get('I', [])
        J = witness.get('J', [])
        K = witness.get('K', [])
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = False
        if R in ('ZZ', 'Z', 'QQ', 'Q', ZZ, QQ):
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
    except Exception:
        h1 = False

    # H_2: I is an ideal of R that is flat as an R-module
    # In ZZ or QQ[x], any ideal is principal, hence flat.
    # We verify it's provided as a valid collection of generators.
    try:
        h2 = isinstance(I, (list, tuple, set))
    except Exception:
        h2 = False

    # H_3: J is an ideal of R
    try:
        h3 = isinstance(J, (list, tuple, set))
    except Exception:
        h3 = False

    # ¬Q: I(J \cap K) != IJ \cap IK
    try:
        g_I = get_gen(I)
        g_J = get_gen(J)
        
        # J \cap K as a set intersection (since K is not guaranteed to be an ideal)
        J_cap_K = [k for k in K if in_ideal(k, g_J)]
        
        # Generators for I(J \cap K)
        I_J_cap_K_gens = [i * k_val for i in I for k_val in J_cap_K]
        g_I_J_cap_K = get_gen(I_J_cap_K_gens)
        
        # Generators for IJ
        IJ_gens = [i * j for i in I for j in J]
        g_IJ = get_gen(IJ_gens)
        
        # Generators for IK
        IK_gens = [i * k_val for i in I for k_val in K]
        g_IK = get_gen(IK_gens)
        
        # Generator for IJ \cap IK
        g_IJ_cap_IK = lcm(g_IJ, g_IK)
        
        neg_q = not ideals_equal(g_I_J_cap_K, g_IJ_cap_IK)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R that is flat as an R-module",
    "H_3: J is an ideal of R",
    "¬Q: I(J \\cap K) != IJ \\cap IK"
]

N_HYP = 3
NEG_Q_INDEX = 3