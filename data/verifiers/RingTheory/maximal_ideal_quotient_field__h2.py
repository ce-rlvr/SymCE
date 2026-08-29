import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
# ZZ and QQ are available from sympy

CONDITION_LABELS = [
    "H_1: R is a commutative ring with a non-zero identity",
    "¬Q: The equivalence between M being a maximal ideal and R/M being a field fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "M is a maximal ideal if and only if the quotient ring R/M is a field"
    (The dropped hypothesis is that M must be an ideal).
    """
    try:
        # Witness can be a tuple (R, M) or just M (with R implicitly ZZ)
        if isinstance(witness, tuple) and len(witness) == 2 and not witness[0] == "ideal":
            R, M = witness
        else:
            R = ZZ
            M = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a commutative ring with a non-zero identity
    h1 = False
    try:
        if R == ZZ or R == QQ:
            h1 = True
        elif isinstance(R, tuple) and R[0] == "Z_n":
            n = R[1]
            if n > 1:
                h1 = True
        elif hasattr(R, "is_commutative") and R.is_commutative and hasattr(R, "has_identity") and R.has_identity:
            h1 = bool(R.one != R.zero)
    except Exception:
        h1 = False

    # neg_Q: not (M is a maximal ideal <==> R/M is a field)
    is_max = False
    is_f = False
    eval_success = False
    
    try:
        if R == ZZ:
            if isinstance(M, (int, sympy.Integer)):
                # M is an element, not an ideal. Thus it cannot be a maximal ideal.
                # However, R/M interpreted as R/(M) can be a field.
                is_max = False
                is_f = sympy.isprime(abs(M))
                eval_success = True
            elif isinstance(M, tuple) and len(M) == 2 and M[0] == "ideal":
                # M is explicitly an ideal
                val = abs(M[1])
                is_max = sympy.isprime(val)
                is_f = sympy.isprime(val)
                eval_success = True
            elif M == ZZ:
                is_max = False
                is_f = False
                eval_success = True
                
        elif R == QQ:
            if isinstance(M, (int, sympy.Integer, sympy.Rational)):
                is_max = False
                is_f = (M == 0)
                eval_success = True
            elif isinstance(M, tuple) and len(M) == 2 and M[0] == "ideal":
                val = M[1]
                is_max = (val == 0)
                is_f = (val == 0)
                eval_success = True
                
        elif isinstance(R, tuple) and R[0] == "Z_n":
            n = R[1]
            if isinstance(M, (int, sympy.Integer)):
                is_max = False
                d = sympy.gcd(n, abs(M))
                is_f = sympy.isprime(d)
                eval_success = True
            elif isinstance(M, tuple) and len(M) == 2 and M[0] == "ideal":
                d = sympy.gcd(n, abs(M[1]))
                is_max = sympy.isprime(d)
                is_f = sympy.isprime(d)
                eval_success = True
    except Exception:
        pass
        
    if not eval_success:
        try:
            # Fallback for generic SymPy ring/ideal objects
            if hasattr(M, "is_maximal_ideal"):
                is_max = bool(M.is_maximal_ideal())
            elif hasattr(M, "is_maximal"):
                is_max = bool(M.is_maximal())
            else:
                is_max = False
                
            if hasattr(R, "quotient_ring"):
                quotient = R.quotient_ring(M)
                if hasattr(quotient, "is_field"):
                    is_f = bool(quotient.is_field())
                else:
                    is_f = False
            else:
                is_f = False
            eval_success = True
        except Exception:
            pass

    if not eval_success:
        return [h1, False]
        
    neg_q = not (is_max == is_f)
    
    return [h1, neg_q]