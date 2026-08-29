import sympy
from sympy.ntheory import totient
from sympy.abc import x
from sympy import cyclotomic_poly, Expr, QQ

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        n = None
        K_deg = None
        
        if isinstance(witness, dict):
            n = witness.get('n')
            for key in ['K_deg', 'degree', 'K_degree', 'deg']:
                if key in witness:
                    K_deg = witness[key]
                    break
        elif isinstance(witness, (tuple, list)):
            if len(witness) > 0:
                n = witness[0]
            for item in reversed(witness[1:]):
                if isinstance(item, (int, sympy.Integer)):
                    K_deg = int(item)
                    break
        else:
            n = witness
            
        if isinstance(n, (int, sympy.Integer)) and n >= 3:
            h1 = True
            
        h2 = True
        if isinstance(witness, dict) and 'Phi_n' in witness:
            if sympy.expand(witness['Phi_n'] - cyclotomic_poly(int(n), x)) != 0:
                h2 = False
        elif isinstance(witness, (tuple, list)):
            for item in witness[1:]:
                if isinstance(item, Expr) and item.has(x):
                    if sympy.expand(item - cyclotomic_poly(int(n), x)) != 0:
                        h2 = False
                    break
                    
        if K_deg is not None and isinstance(K_deg, (int, sympy.Integer)):
            neg_q = (int(K_deg) != totient(int(n)))
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "H_2: Phi_n(x) is the n-th cyclotomic polynomial",
    "¬Q: The degree of the field extension K:Q is not equal to phi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2