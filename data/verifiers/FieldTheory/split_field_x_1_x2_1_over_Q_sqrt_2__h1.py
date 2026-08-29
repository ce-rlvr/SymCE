import sympy
from sympy import QQ, I, sqrt
from sympy.abc import x, t

Z2 = sympy.combinatorics.CyclicGroup(2)
S3 = sympy.combinatorics.SymmetricGroup(3)

def get_field(gens):
    real_gens = []
    seen = []
    for g in gens:
        if g in seen:
            continue
        seen.append(g)
        try:
            QQ.from_expr(g)
        except Exception:
            real_gens.append(g)
    if not real_gens:
        return QQ
    try:
        return QQ.algebraic_field(*real_gens)
    except Exception:
        return None

def fields_equal(F1, F2):
    if F1 is None or F2 is None:
        return False
    if F1 == F2:
        return True
    if F1 == QQ and F2 == QQ:
        return True
    if F1 == QQ or F2 == QQ:
        return False
    try:
        if F1.ext.minpoly.degree() != F2.ext.minpoly.degree():
            return False
        F1.from_expr(F2.ext.as_expr())
        return True
    except Exception:
        return False

def field_degree(F):
    if F == QQ:
        return 1
    return F.ext.minpoly.degree()

def parse_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (list, tuple)) and isinstance(witness[1], (list, tuple)):
        return list(witness[0]), list(witness[1])
    elif isinstance(witness, (list, tuple)):
        return list(witness), list(witness) + [I]
    else:
        return [witness], [witness, I]

def conditions(witness) -> list[bool]:
    try:
        F_gens, K_gens = parse_witness(witness)
    except Exception:
        return [False, False, False]
    
    try:
        F_field = get_field(F_gens)
        h1 = (F_field is not None)
    except Exception:
        h1 = False

    try:
        K_field = get_field(K_gens)
        expected_K_field = get_field(F_gens + [I])
        h2 = fields_equal(K_field, expected_K_field)
    except Exception:
        h2 = False

    try:
        Q_sqrt2_i = get_field([sqrt(2), I])
        is_Q_sqrt2_i = fields_equal(K_field, Q_sqrt2_i)
        
        if F_field is None or K_field is None:
            deg_ok = False
        else:
            deg_K = field_degree(K_field)
            deg_F = field_degree(F_field)
            deg_ok = (deg_K == 2 * deg_F)
            
        conclusion = is_Q_sqrt2_i and deg_ok
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) = (x+1)(x^2+1) in F polynomials",
    "H_2: K is the splitting field of f(x) over F",
    "¬Q: K != Q(sqrt(2), i) or degree of K over F != 2"
]

N_HYP = 2
NEG_Q_INDEX = 2