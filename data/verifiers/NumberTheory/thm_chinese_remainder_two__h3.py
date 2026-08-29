import sympy
import math

def conditions(witness):
    try:
        if isinstance(witness, dict):
            m1 = witness.get('m1', witness.get('m_1'))
            m2 = witness.get('m2', witness.get('m_2'))
            a1 = witness.get('a1', witness.get('a_1'))
            a2 = witness.get('a2', witness.get('a_2'))
            if a1 is None:
                a1 = 0.5
            if a2 is None:
                a2 = 0.5
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 4:
                m1, m2, a1, a2 = witness
            elif len(witness) == 2:
                m1, m2 = witness
                a1, a2 = 0.5, 0.5
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if m1 is None or m2 is None:
            return [False, False, False]

        try:
            m1_val = sympy.sympify(m1)
            m2_val = sympy.sympify(m2)
        except Exception:
            return [False, False, False]

        # H1: m1 and m2 are positive integers
        try:
            h1 = m1_val.is_integer and m2_val.is_integer and m1_val > 0 and m2_val > 0
            h1 = bool(h1)
        except Exception:
            h1 = False

        # H2: gcd(m1, m2) = 1
        try:
            if h1:
                h2 = math.gcd(int(m1_val), int(m2_val)) == 1
            else:
                h2 = False
        except Exception:
            h2 = False

        # neg_Q: The system does NOT have a unique solution modulo m1*m2
        try:
            a1_val = sympy.sympify(a1)
            a2_val = sympy.sympify(a2)
            
            if not (m1_val.is_integer and m2_val.is_integer and m1_val != 0 and m2_val != 0):
                neg_q = False
            elif not a1_val.is_integer or not a2_val.is_integer:
                neg_q = True
            else:
                m1_int = abs(int(m1_val))
                m2_int = abs(int(m2_val))
                a1_int = int(a1_val)
                a2_int = int(a2_val)
                g = math.gcd(m1_int, m2_int)
                if (a1_int - a2_int) % g == 0:
                    solutions = g
                else:
                    solutions = 0
                neg_q = (solutions != 1)
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: m_1 and m_2 are positive integers",
    "H_2: \gcd(m_1, m_2) = 1",
    "¬Q: The system of congruences does not have a unique solution modulo m_1 m_2"
]

N_HYP = 2
NEG_Q_INDEX = 2