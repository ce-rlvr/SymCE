import sympy
from sympy import isprime

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypothesis and fails the conclusion.
    H_1: Every non-zero prime ideal of R is a maximal ideal
    Conclusion: R is a principal ideal domain
    """
    h1 = False
    is_pid = True
    
    try:
        if isinstance(witness, str):
            w = witness.replace(" ", "")
            if w.startswith("Z/") and w.endswith("Z"):
                try:
                    n = int(w[2:-1])
                    h1 = True
                    is_pid = isprime(n) if n >= 2 else (n == 0)
                except ValueError:
                    pass
            elif w in ["Z[sqrt(-5)]", "Z[sqrt(-6)]", "Z[sqrt(-10)]", "Z[sqrt(-3)]"]:
                h1 = True
                is_pid = False
            elif w in ["Z[i]", "Z[sqrt(-2)]", "Z[sqrt(2)]", "Z[sqrt(-1)]"]:
                h1 = True
                is_pid = True
            elif w in ["Z[x]", "QQ[x,y]", "k[x,y]", "R[x,y]", "C[x,y]"]:
                h1 = False
                is_pid = False
            elif w in ["Z", "QQ", "R", "C"]:
                h1 = True
                is_pid = True
                
        elif isinstance(witness, int):
            n = abs(witness)
            if n == 0:
                h1 = True
                is_pid = True
            elif n == 1:
                h1 = True
                is_pid = False
            else:
                h1 = True
                is_pid = isprime(n)
                
        elif hasattr(witness, 'is_PID'):
            is_pid = bool(witness.is_PID)
            if witness.is_Field:
                h1 = True
            elif witness.__class__.__name__ == 'IntegerRing':
                h1 = True
            elif witness.__class__.__name__ == 'PolynomialRing':
                base = witness.domain
                num_vars = len(witness.symbols)
                if base.is_Field and num_vars == 1:
                    h1 = True
                else:
                    h1 = False
            else:
                h1 = False
                
        elif hasattr(witness, 'domain') and hasattr(witness, 'gens'):
            base = witness.domain
            num_vars = len(witness.gens)
            if base.is_Field and num_vars == 1:
                h1 = True
                is_pid = True
            else:
                h1 = False
                is_pid = False
                
        elif isinstance(witness, tuple) and len(witness) == 2:
            if hasattr(witness[0], 'is_PID') and isinstance(witness[1], int):
                if witness[0].__class__.__name__ == 'IntegerRing':
                    n = abs(witness[1])
                    h1 = True
                    is_pid = isprime(n) if n >= 2 else (n == 0)
                    
    except Exception:
        return [False, False]

    return [h1, not is_pid]

CONDITION_LABELS = [
    "H_1: Every non-zero prime ideal of R is a maximal ideal",
    "¬Q: R is not a principal ideal domain"
]

N_HYP = 1
NEG_Q_INDEX = 1