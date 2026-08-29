import sympy
from sympy import symbols, factor_list, I
from sympy.polys.domains import QQ, ZZ, FF, RR, CC

x, y = symbols('x y')

try:
    QQ_I = QQ.algebraic_field(I)
except Exception:
    QQ_I = None

def conditions(witness) -> list[bool]:
    try:
        domain = FF(int(witness)) if isinstance(witness, (int, sympy.Integer)) else witness
        h1 = bool(getattr(domain, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        domain = FF(int(witness)) if isinstance(witness, (int, sympy.Integer)) else witness
        factors = factor_list(x**2 + y**2, domain=domain)
        neg_q = bool(sum(m for f, m in factors[1]) > 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "¬Q: x^2 + y^2 is reducible"
]

N_HYP = 1
NEG_Q_INDEX = 1