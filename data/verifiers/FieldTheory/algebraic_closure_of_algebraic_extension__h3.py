import sympy
from sympy import QQ as sympy_QQ, RR as sympy_RR, CC as sympy_CC

# Top-level setup: named object bindings that the witness expression may reference.
# We define a small universe of fields and their relations to allow constructing a counterexample.
class Field:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

QQ = Field("QQ")
QQ_sqrt2 = Field("QQ(sqrt(2))")
QQ_bar = Field("QQ_bar")
RR = Field("RR")
CC = Field("CC")
F2 = Field("F2")
F4 = Field("F4")
F2_bar = Field("F2_bar")

def get_name(obj):
    if isinstance(obj, Field):
        return obj.name
    if obj == sympy_QQ:
        return "QQ"
    if obj == sympy_RR:
        return "RR"
    if obj == sympy_CC:
        return "CC"
    if hasattr(obj, '__name__'):
        return obj.__name__
    return str(obj)

def is_algebraic_extension(E, F):
    E_name = get_name(E)
    F_name = get_name(F)
    alg_exts = {
        ("QQ", "QQ"): True,
        ("QQ(sqrt(2))", "QQ"): True,
        ("QQ_bar", "QQ"): True,
        ("QQ(sqrt(2))", "QQ(sqrt(2))"): True,
        ("QQ_bar", "QQ(sqrt(2))"): True,
        ("QQ_bar", "QQ_bar"): True,
        ("RR", "RR"): True,
        ("CC", "RR"): True,
        ("CC", "CC"): True,
        ("F2", "F2"): True,
        ("F4", "F2"): True,
        ("F2_bar", "F2"): True,
        ("F4", "F4"): True,
        ("F2_bar", "F4"): True,
        ("F2_bar", "F2_bar"): True,
    }
    return alg_exts.get((E_name, F_name), False)

def is_algebraically_closed(F):
    return get_name(F) in ("QQ_bar", "CC", "F2_bar")

def contains(sup, sub):
    sup_name = get_name(sup)
    sub_name = get_name(sub)
    containment = {
        ("QQ", "QQ"): True,
        ("QQ(sqrt(2))", "QQ"): True,
        ("QQ(sqrt(2))", "QQ(sqrt(2))"): True,
        ("QQ_bar", "QQ"): True,
        ("QQ_bar", "QQ(sqrt(2))"): True,
        ("QQ_bar", "QQ_bar"): True,
        ("RR", "QQ"): True,
        ("RR", "QQ(sqrt(2))"): True,
        ("RR", "RR"): True,
        ("CC", "QQ"): True,
        ("CC", "QQ(sqrt(2))"): True,
        ("CC", "QQ_bar"): True,
        ("CC", "RR"): True,
        ("CC", "CC"): True,
        ("F2", "F2"): True,
        ("F4", "F2"): True,
        ("F4", "F4"): True,
        ("F2_bar", "F2"): True,
        ("F2_bar", "F4"): True,
        ("F2_bar", "F2_bar"): True,
    }
    return containment.get((sup_name, sub_name), False)

def algebraic_closure_in(base, omega):
    base_name = get_name(base)
    omega_name = get_name(omega)
    if not contains(omega_name, base_name):
        return None
    closures = {
        ("QQ", "QQ"): "QQ",
        ("QQ", "QQ(sqrt(2))"): "QQ(sqrt(2))",
        ("QQ", "QQ_bar"): "QQ_bar",
        ("QQ", "CC"): "QQ_bar",
        ("QQ(sqrt(2))", "QQ(sqrt(2))"): "QQ(sqrt(2))",
        ("QQ(sqrt(2))", "QQ_bar"): "QQ_bar",
        ("QQ(sqrt(2))", "CC"): "QQ_bar",
        ("QQ_bar", "QQ_bar"): "QQ_bar",
        ("QQ_bar", "CC"): "QQ_bar",
        ("RR", "RR"): "RR",
        ("RR", "CC"): "CC",
        ("CC", "CC"): "CC",
        ("F2", "F2"): "F2",
        ("F2", "F4"): "F4",
        ("F2", "F2_bar"): "F2_bar",
        ("F4", "F4"): "F4",
        ("F4", "F2_bar"): "F2_bar",
        ("F2_bar", "F2_bar"): "F2_bar",
    }
    return closures.get((base_name, omega_name), None)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F = witness.get("F")
            E = witness.get("E")
            Omega = witness.get("Omega", witness.get("\\Omega"))
            A_E = witness.get("A_E")
            A_F = witness.get("A_F")
        elif isinstance(witness, tuple) and len(witness) == 5:
            F, E, Omega, A_E, A_F = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: E is an algebraic field extension of F
    try:
        h1_ok = is_algebraic_extension(E, F)
    except Exception:
        h1_ok = False

    # H_2: \Omega is an algebraically closed field containing E
    try:
        h2_ok = is_algebraically_closed(Omega) and contains(Omega, E)
    except Exception:
        h2_ok = False

    # H_3: A_E is the algebraic closure of E in \Omega
    try:
        h3_ok = (get_name(A_E) == algebraic_closure_in(E, Omega))
    except Exception:
        h3_ok = False

    # ¬Q: A_F != A_E (The conclusion A_F = A_E fails)
    try:
        neg_q_ok = (get_name(A_F) != get_name(A_E))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: E is an algebraic field extension of F",
    "H_2: \\Omega is an algebraically closed field containing E",
    "H_3: A_E is the algebraic closure of E in \\Omega",
    "¬Q: A_F != A_E"
]

N_HYP = 3
NEG_Q_INDEX = 3