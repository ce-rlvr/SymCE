import sympy
from sympy import symbols
from sympy.polys.domains import ZZ, QQ

# Top-level setup
x, y, z = symbols('x y z')

KNOWN_RINGS = {
    "Z": {"integral_domain": True, "bezout": True, "pid": True},
    "Q": {"integral_domain": True, "bezout": True, "pid": True},
    "Z[x]": {"integral_domain": True, "bezout": False, "pid": False},
    "Q[x]": {"integral_domain": True, "bezout": True, "pid": True},
    "Q[x,y]": {"integral_domain": True, "bezout": False, "pid": False},
    "algebraic_integers": {"integral_domain": True, "bezout": True, "pid": False},
    "entire_functions": {"integral_domain": True, "bezout": True, "pid": False},
    "Z+xQ[x]": {"integral_domain": True, "bezout": False, "pid": False},
    "Z[sqrt(-5)]": {"integral_domain": True, "bezout": False, "pid": False},
    "Z_6": {"integral_domain": False, "bezout": False, "pid": False},
}

def _evaluate_attr(obj, attr_name):
    if hasattr(obj, attr_name):
        val = getattr(obj, attr_name)
        return bool(val() if callable(val) else val)
    return None

def is_integral_domain(w):
    res = _evaluate_attr(w, 'is_integral_domain')
    if res is not None:
        return res
    if isinstance(w, str):
        return KNOWN_RINGS.get(w, {}).get("integral_domain", False)
    if _evaluate_attr(w, 'is_Ring'):
        return True
    if _evaluate_attr(w, 'is_Field'):
        return True
    return False

def is_bezout(w):
    res = _evaluate_attr(w, 'is_bezout')
    if res is not None:
        return res
    if isinstance(w, str):
        return KNOWN_RINGS.get(w, {}).get("bezout", False)
    if _evaluate_attr(w, 'is_PID'):
        return True
    if _evaluate_attr(w, 'is_Field'):
        return True
    return False

def is_pid(w):
    res = _evaluate_attr(w, 'is_pid')
    if res is not None:
        return res
    if isinstance(w, str):
        return KNOWN_RINGS.get(w, {}).get("pid", False)
    res_pid = _evaluate_attr(w, 'is_PID')
    if res_pid is not None:
        return res_pid
    if _evaluate_attr(w, 'is_Field'):
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = is_integral_domain(witness)
    except Exception:
        h1 = False

    try:
        h2 = is_bezout(witness)
    except Exception:
        h2 = False

    try:
        q = is_pid(witness)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: R is a Bezout domain",
    "¬Q: R is not a principal ideal domain"
]

N_HYP = 2
NEG_Q_INDEX = 2