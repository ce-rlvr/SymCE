import sympy
import math

CONDITION_LABELS = [
    "¬Q: gcd(n!, m!) == min(n, m)!"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False]
        n, m = witness
    except Exception:
        return [False]
        
    try:
        n_sym = sympy.sympify(n)
        m_sym = sympy.sympify(m)
        
        # Ensure the witness consists of concrete real numbers
        if not (n_sym.is_real and n_sym.is_number and m_sym.is_real and m_sym.is_number):
            return [False]
            
        try:
            fact_n = sympy.factorial(n_sym)
            fact_m = sympy.factorial(m_sym)
            
            # sympy.gcd may raise an exception for non-integer or undefined (zoo) values
            lhs = sympy.gcd(fact_n, fact_m)
            
            min_nm = sympy.Min(n_sym, m_sym)
            rhs = sympy.factorial(min_nm)
            
            if lhs == rhs:
                q_holds = True
            else:
                q_holds = bool(sympy.simplify(lhs - rhs) == 0)
        except Exception:
            # If the expression is undefined or cannot be evaluated, the conclusion fails
            q_holds = False
            
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [neg_q]