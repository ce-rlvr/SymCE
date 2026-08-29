import sympy

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        p = None
        
        if witness == sympy.CC:
            h1 = True
            p = 0
        elif witness == sympy.QQ or witness == sympy.RR:
            h1 = False
            p = 0
        elif isinstance(witness, str):
            w = witness.strip().lower()
            if w in ['c', 'cc', 'complex', 'complexes', 'algebraic closure of q', 'q_bar', 'qbar']:
                h1 = True
                p = 0
            elif w in ['q', 'qq', 'rationals', 'r', 'rr', 'reals']:
                h1 = False
                p = 0
            else:
                p = int(w)
                if p == 0 or sympy.isprime(p):
                    h1 = True
        else:
            p = int(witness)
            if p == 0 or sympy.isprime(p):
                h1 = True
                
        h2 = True
        neg_q = (p == 0)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: L is the field of Puiseux series over K",
    "¬Q: L is algebraically closed"
]

N_HYP = 2
NEG_Q_INDEX = 2