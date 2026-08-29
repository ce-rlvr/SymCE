import sympy
from sympy import symbols, Poly, groebner

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z, w = symbols('x y z w')

def conditions(witness) -> list[bool]:
    # H1: R is a graded ring
    # We implicitly use R = QQ[vars] which is a graded ring.
    # We check if the witness is a valid pair of ideal generators.
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        I_gens, J_gens = witness
        if not isinstance(I_gens, (list, tuple)) or not isinstance(J_gens, (list, tuple)):
            return [False, False, False]
        
        I_gens_sym = [sympy.sympify(expr) for expr in I_gens]
        J_gens_sym = [sympy.sympify(expr) for expr in J_gens]
        h1 = True
    except Exception:
        return [False, False, False]

    # H2: I and J are homogeneous ideals of R
    h2 = False
    try:
        vars_set = set()
        for expr in I_gens_sym + J_gens_sym:
            vars_set.update(expr.free_symbols)
        vars_list = sorted(list(vars_set), key=lambda s: s.name)
        if not vars_list:
            vars_list = [x]
        
        h2 = True
        for expr in I_gens_sym + J_gens_sym:
            if expr != 0:
                poly = Poly(expr, *vars_list)
                if not poly.is_homogeneous:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: The canonical ring homomorphism from R/(I \cap J) to R/I \times R/J is NOT an isomorphism
    # By the Chinese Remainder Theorem, this map is an isomorphism iff I + J = R.
    # Thus, it is NOT an isomorphism iff I + J != R.
    neg_q = False
    try:
        # Compute the Groebner basis of I + J
        gb = groebner(I_gens_sym + J_gens_sym, *vars_list, domain='QQ')
        I_plus_J_is_R = False
        for p in gb:
            if p.is_constant() and p != 0:
                I_plus_J_is_R = True
                break
        neg_q = not I_plus_J_is_R
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a graded ring",
    "H_2: I and J are homogeneous ideals of R",
    "¬Q: The canonical ring homomorphism from R/(I \\cap J) to R/I \\times R/J is not an isomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2