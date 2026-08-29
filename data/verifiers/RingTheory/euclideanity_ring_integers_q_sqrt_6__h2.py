import sympy as sp
import math

x = sp.Symbol('x')

def get_conductor(witness):
    """
    Attempts to extract the conductor f of an order Z[f*sqrt(6)] from the witness.
    The witness could be the integer f itself, or a list of generators.
    """
    try:
        if isinstance(witness, (int, sp.Integer)):
            return int(witness)
                
        sqrt6 = sp.sqrt(6)
        if isinstance(witness, sp.Expr):
            witness = [witness]
            
        if isinstance(witness, (list, tuple, set)):
            b_vals = []
            for gen in witness:
                gen = sp.sympify(gen)
                coeff = gen.coeff(sqrt6)
                if coeff != 0:
                    if getattr(coeff, 'is_Integer', False) or isinstance(coeff, int):
                        b_vals.append(abs(int(coeff)))
                elif gen == sqrt6:
                    b_vals.append(1)
            if b_vals:
                f = b_vals[0]
                for b in b_vals[1:]:
                    f = math.gcd(f, b)
                return f
    except Exception:
        pass
    return None

def conditions(witness):
    f = get_conductor(witness)
    
    # H_1: Let K be the real quadratic field Q(sqrt(6)).
    # We consider this satisfied if the witness represents a valid order in Q(sqrt(6)),
    # which means it has a well-defined integer conductor f >= 1.
    try:
        h1_ok = bool(f is not None and f >= 1)
    except Exception:
        h1_ok = False
        
    # ¬Q: R is NOT a Euclidean domain.
    # An order in Q(sqrt(6)) with conductor f is a Euclidean domain if and only if f == 1
    # (the maximal order Z[sqrt(6)] is Euclidean).
    # Therefore, it fails to be a Euclidean domain if f > 1.
    try:
        neg_q = bool(f is not None and f > 1)
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: Let K be the real quadratic field Q(sqrt(6))",
    "¬Q: R is not a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1