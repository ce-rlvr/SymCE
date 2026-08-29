import sympy
from sympy import sqrt

class CustomRing:
    def __init__(self, name, is_dedekind, is_pid):
        self.name = name
        self.is_dedekind = is_dedekind
        self.is_pid = is_pid

    def __str__(self):
        return self.name

# Pre-defined common rings for the witness
ZZ = CustomRing("ZZ", True, True)
QQ = CustomRing("QQ", True, True)
ZZ_x = CustomRing("ZZ[x]", False, False)
QQ_x = CustomRing("QQ[x]", True, True)
ZZ_sqrt_minus_5 = CustomRing("ZZ[sqrt(-5)]", True, False)
Z_sqrt_minus_5 = ZZ_sqrt_minus_5

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a Dedekind domain but NOT a principal ideal domain.
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, CustomRing):
            h1 = witness.is_dedekind
            neg_q = not witness.is_pid
            
        elif isinstance(witness, str):
            w = witness.replace(" ", "").lower()
            if w in ["z", "zz", "q", "qq"]:
                h1, neg_q = True, False
            elif w in ["z[x]", "zz[x]"]:
                h1, neg_q = False, True
            elif w in ["q[x]", "qq[x]"]:
                h1, neg_q = True, False
            elif "sqrt(-5)" in w:
                h1, neg_q = True, True
            else:
                h1, neg_q = False, False
                
        elif isinstance(witness, (int, sympy.Integer)):
            # Interpret integer d as the ring of integers of Q(sqrt(d))
            d = int(witness)
            if d == 1 or d == 0:
                h1, neg_q = False, False
            else:
                is_sq_free = True
                for p in range(2, int(abs(d)**0.5) + 1):
                    if d % (p*p) == 0:
                        is_sq_free = False
                        break
                if not is_sq_free:
                    h1, neg_q = False, False
                else:
                    h1 = True
                    if d < 0:
                        # Heegner numbers for imaginary quadratic fields with class number 1
                        is_pid = d in {-1, -2, -3, -7, -11, -19, -43, -67, -163}
                    else:
                        # Known non-PIDs for small real quadratic fields
                        non_pids = {10, 15, 26, 30, 34, 35, 39, 42, 51, 55, 58, 65, 66, 70, 74, 78, 79, 82, 85, 87, 91, 95}
                        is_pid = d not in non_pids
                    neg_q = not is_pid
                    
        elif isinstance(witness, sympy.Expr):
            if witness == sympy.sqrt(-5):
                h1, neg_q = True, True
            else:
                h1, neg_q = False, False
                
        elif hasattr(witness, 'is_PID'):
            # Fallback for sympy domains
            is_pid = witness.is_PID
            if is_pid:
                h1, neg_q = True, False
            else:
                # Sympy's non-PID domains (like ZZ[x]) are generally not Dedekind
                h1, neg_q = False, True
                
    except Exception:
        h1, neg_q = False, False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Dedekind domain",
    "¬Q: R is not a principal ideal domain"
]

N_HYP = 1
NEG_Q_INDEX = 1