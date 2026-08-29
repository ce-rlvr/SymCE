import math
from sympy.ntheory import factorint
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# No specific named bindings needed for this domain; integers and SymPy objects are used directly.

def get_order(F):
    if hasattr(F, 'order'):
        o = F.order
        if callable(o):
            o = o()
        return int(o)
    return int(F)

def is_prime_power(k):
    if k < 2: return False
    facs = factorint(k)
    return len(facs) == 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            p = witness.get('p')
            n = witness.get('n')
            m = witness.get('m')
        else:
            try:
                F = witness.F
                p = witness.p
                n = witness.n
                m = witness.m
            except AttributeError:
                F, p, n, m = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a finite field
    try:
        order_F = get_order(F)
        h1 = is_prime_power(order_F)
    except Exception:
        h1 = False

    # H_2: The order of F is p^n
    try:
        order_F = get_order(F)
        val = p**n
        if isinstance(val, complex):
            h2 = False
        else:
            try:
                h2 = (val == order_F) or math.isclose(float(val), float(order_F))
            except Exception:
                h2 = (val == order_F)
    except Exception:
        h2 = False

    # H_3: m is a positive integer
    try:
        if hasattr(m, 'is_integer') and m.is_integer:
            m_int = int(m)
        elif isinstance(m, int) or (isinstance(m, float) and m.is_integer()):
            m_int = int(m)
        else:
            m_int = None
            
        h3 = (m_int is not None) and (m_int > 0)
    except Exception:
        h3 = False

    # neg_Q: F contains a subfield of order p^m if and only if m divides n (fails)
    try:
        order_F = get_order(F)
        order_S = p**m
        
        contains_subfield = False
        try:
            if hasattr(order_S, 'is_integer') and order_S.is_integer:
                order_S_int = int(order_S)
            elif isinstance(order_S, int) or (isinstance(order_S, float) and order_S.is_integer()):
                order_S_int = int(order_S)
            else:
                order_S_int = None
                
            if order_S_int is not None and order_S_int >= 2:
                fac_F = factorint(order_F)
                fac_S = factorint(order_S_int)
                if len(fac_F) == 1 and len(fac_S) == 1:
                    q_F, k_F = list(fac_F.items())[0]
                    q_S, k_S = list(fac_S.items())[0]
                    if q_F == q_S and k_F % k_S == 0:
                        contains_subfield = True
        except Exception:
            pass

        m_divides_n = False
        try:
            if hasattr(n, 'is_integer') and n.is_integer:
                n_int = int(n)
            elif isinstance(n, int) or (isinstance(n, float) and n.is_integer()):
                n_int = int(n)
            else:
                n_int = None
                
            if n_int is not None:
                m_int_val = int(m)
                if m_int_val != 0 and n_int % m_int_val == 0:
                    m_divides_n = True
        except Exception:
            pass

        q_val = (contains_subfield == m_divides_n)
        neg_q = not q_val
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field",
    "H_2: The order of F is p^n",
    "H_3: m is a positive integer",
    "¬Q: The equivalence (F contains a subfield of order p^m iff m divides n) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3