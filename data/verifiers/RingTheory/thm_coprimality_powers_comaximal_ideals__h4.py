import math
from sympy import sympify, S
from sympy.abc import x, y, z

Z = S.Integers
ZZ = S.Integers
Q = S.Rationals
QQ = S.Rationals

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('I', witness.get('a'))
            b = witness.get('J', witness.get('b'))
            m = witness.get('m')
            n = witness.get('n')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                a, b, m, n = witness
            elif len(witness) == 5:
                _, a, b, m, n = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]

        if a is None or b is None or m is None or n is None:
            return [False, False, False, False]

        def extract_int(val):
            val_sym = sympify(val)
            if val_sym.is_Integer:
                return int(val_sym)
            if val_sym.is_Mul:
                for arg in val_sym.args:
                    if arg.is_Integer:
                        return int(arg)
            if val_sym == S.Integers or str(val_sym) in ('Z', 'ZZ'):
                return 1
            return int(val_sym)

        a = extract_int(a)
        b = extract_int(b)
        m_sym = sympify(m)
        n_sym = sympify(n)

        h1 = True
        h2 = True
        h3 = math.gcd(a, b) == 1

        try:
            m_int = int(m_sym)
            n_int = int(n_sym)
            
            if m_sym != m_int or n_sym != n_int:
                are_comaximal = False
            elif m_int > 10000 or n_int > 10000:
                return [False, False, False, False]
            else:
                if m_int < 0:
                    am = a ** m_int if a in (1, -1) else None
                else:
                    am = a ** m_int
                    
                if n_int < 0:
                    bn = b ** n_int if b in (1, -1) else None
                else:
                    bn = b ** n_int
                    
                if am is not None and bn is not None:
                    are_comaximal = math.gcd(am, bn) == 1
                else:
                    are_comaximal = False
        except Exception:
            are_comaximal = False

        neg_q = not are_comaximal

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "H_3: I and J are comaximal",
    "¬Q: I^m and J^n are not comaximal"
]

N_HYP = 3
NEG_Q_INDEX = 3