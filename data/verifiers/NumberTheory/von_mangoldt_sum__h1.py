import sympy
from sympy import factorint, log
from sympy.ntheory import divisors

N_HYP = 0
NEG_Q_INDEX = 0

CONDITION_LABELS = [
    "¬Q: sum_{d|n} Lambda(d) != ln(n)"
]

def conditions(witness):
    try:
        n = sympy.sympify(witness)
        
        # Evaluate sum_{d|n} Lambda(d)
        # divisors(n) returns the positive divisors of n
        divs = divisors(n)
        
        lhs = sympy.S.Zero
        for d in divs:
            if d > 1:
                f = factorint(d)
                # Von Mangoldt function Lambda(d) is ln(p) if d = p^k, else 0
                if len(f) == 1:
                    p = list(f.keys())[0]
                    lhs += log(p)
                    
        rhs = log(n)
        
        diff = lhs - rhs
        if diff == 0:
            q_holds = True
        else:
            val = complex(diff.evalf())
            q_holds = (abs(val) < 1e-9)
            
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [neg_q]