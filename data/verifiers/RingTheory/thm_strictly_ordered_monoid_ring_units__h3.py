import sympy
from sympy import symbols, Rational, Integer, Poly, expand

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

x, y, z = symbols('x y z')

def check_attr(obj, attr_names):
    for name in attr_names:
        if hasattr(obj, name):
            val = getattr(obj, name)
            if callable(val):
                try:
                    return bool(val())
                except Exception:
                    pass
            else:
                return bool(val)
    return False

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False

    if isinstance(witness, dict):
        h1 = bool(witness.get("is_integral_domain", witness.get("h1", False)))
        h2 = bool(witness.get("is_strictly_totally_ordered", witness.get("h2", False)))
        neg_q = bool(witness.get("neg_q", witness.get("neg_Q", False)))
        if h1 or h2 or neg_q:
            return [h1, h2, neg_q]

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            u, v = witness
            if hasattr(u, 'as_poly') and hasattr(v, 'as_poly'):
                pu = u.as_poly()
                pv = v.as_poly()
                if pu is not None and pv is not None:
                    h1 = bool(pu.domain.is_Domain)
                    h2 = True
                    is_unit = (expand(u * v) == 1)
                    is_monomial = (len(pu.terms()) == 1)
                    neg_q = bool(is_unit and not is_monomial)
                    return [h1, h2, neg_q]
    except Exception:
        pass

    h1 = check_attr(witness, ["is_integral_domain", "h1"])
    h2 = check_attr(witness, ["is_strictly_totally_ordered", "h2"])
    neg_q = check_attr(witness, ["neg_q", "neg_Q"])

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: M is a strictly totally ordered monoid",
    "¬Q: The group of units of the monoid ring does not consist exactly of the elements of the form u*m"
]

N_HYP = 2
NEG_Q_INDEX = 2