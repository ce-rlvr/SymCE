import sympy
from sympy import symbols
from sympy.polys.domains import QQ, ZZ, FractionField

x, y, t = symbols('x y t')

def conditions(witness) -> list[bool]:
    neg_q = False
    try:
        if isinstance(witness, str):
            s = witness.lower()
            if "transcendental" in s or "(x)" in s or "(t)" in s:
                neg_q = True
        elif hasattr(witness, 'gens') and len(witness.gens) == 1 and type(witness).__name__ == 'FractionField':
            neg_q = True
        elif hasattr(witness, 'is_Symbol') and witness.is_Symbol:
            neg_q = True
    except Exception:
        pass
    return [neg_q]

CONDITION_LABELS = ["neg_Q: The equivalence fails for simple transcendental extensions"]

N_HYP = 0
NEG_Q_INDEX = 0