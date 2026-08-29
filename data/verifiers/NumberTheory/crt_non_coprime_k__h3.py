import math
import sympy
from sympy import Rational, Integer

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        m_list, a_list = witness
        if not (isinstance(m_list, (list, tuple)) and isinstance(a_list, (list, tuple))):
            return [False, False, False]
        if len(m_list) != len(a_list) or len(m_list) == 0:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = all(isinstance(m, (int, sympy.Integer)) and not isinstance(m, bool) and m > 0 for m in m_list)
    except Exception:
        h1 = False
        
    try:
        h2 = all(isinstance(a, (int, sympy.Integer)) and not isinstance(a, bool) for a in a_list)
    except Exception:
        h2 = False
        
    try:
        has_solution = True
        for i in range(len(m_list)):
            for j in range(i + 1, len(m_list)):
                g = math.gcd(int(m_list[i]), int(m_list[j]))
                if (int(a_list[i]) - int(a_list[j])) % g != 0:
                    has_solution = False
                    break
            if not has_solution:
                break
        neg_q = not has_solution
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m1, m2, ..., mk are positive integers",
    "H_2: a1, a2, ..., ak are integers",
    "¬Q: The system does not have a unique solution modulo lcm(m1, ..., mk)"
]

N_HYP = 2
NEG_Q_INDEX = 2