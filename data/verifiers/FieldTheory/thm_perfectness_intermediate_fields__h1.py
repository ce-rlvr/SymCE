import sympy
from sympy.abc import t

class Field:
    def __init__(self, name, perfect, alg_closed=False):
        self.name = name
        self.perfect = perfect
        self.alg_closed = alg_closed
        self.subfields = {self}
        self.alg_closures = set()

    def __repr__(self):
        return self.name

def set_extension(sub, sup):
    sup.subfields.update(sub.subfields)

def set_alg_closure(base, closure):
    set_extension(base, closure)
    base.alg_closures.add(closure)
    closure.alg_closed = True
    closure.perfect = True

# Characteristic 0
QQ = Field("QQ", perfect=True)
QQ_bar = Field("QQ_bar", perfect=True, alg_closed=True)
set_alg_closure(QQ, QQ_bar)

RR = Field("RR", perfect=True)
CC = Field("CC", perfect=True, alg_closed=True)
set_alg_closure(RR, CC)

# Characteristic p, perfect
Fp = Field("Fp", perfect=True)
Fp_bar = Field("Fp_bar", perfect=True, alg_closed=True)
set_alg_closure(Fp, Fp_bar)

# Characteristic p, imperfect
Fp_t = Field("Fp(t)", perfect=False)
set_extension(Fp, Fp_t)

Fp_t_bar = Field("Fp(t)_bar", perfect=True, alg_closed=True)
set_alg_closure(Fp_t, Fp_t_bar)

# Intermediate imperfect field
Fp_t_sqrt = Field("Fp(t)(sqrt(t))", perfect=False)
set_extension(Fp_t, Fp_t_sqrt)
set_alg_closure(Fp_t_sqrt, Fp_t_bar)


def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (F, K, E), checks if it is a valid counterexample.
    """
    try:
        F, K, E = witness
    except Exception:
        return [False, False, False]
        
    try:
        # H_1: E is an algebraic closure of F
        h1 = E in F.alg_closures
    except Exception:
        h1 = False
        
    try:
        # H_2: K is a field such that F \subseteq K \subseteq E
        h2 = (F in K.subfields) and (K in E.subfields)
    except Exception:
        h2 = False
        
    try:
        # ¬Q: K is not a perfect field
        neg_q = not K.perfect
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is an algebraic closure of F",
    "H_2: K is a field such that F \\subseteq K \\subseteq E",
    "¬Q: K is not a perfect field"
]

N_HYP = 2
NEG_Q_INDEX = 2