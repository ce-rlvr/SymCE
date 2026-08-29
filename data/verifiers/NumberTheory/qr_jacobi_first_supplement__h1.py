import sympy
from sympy.ntheory import jacobi_symbol

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        n = int(witness)
        
        try:
            lhs = jacobi_symbol(-1, n)
        except Exception:
            lhs = "undefined"
            
        if (n - 1) % 2 == 0:
            power = (n - 1) // 2
            rhs = 1 if power % 2 == 0 else -1
        else:
            rhs = "complex"
            
        if lhs == "undefined" or rhs == "complex":
            eq = False
        else:
            eq = (lhs == rhs)
            
        neg_q = not eq
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The Jacobi symbol (-1/n) is not equal to (-1)^((n-1)/2)"
]

N_HYP = 0
NEG_Q_INDEX = 0