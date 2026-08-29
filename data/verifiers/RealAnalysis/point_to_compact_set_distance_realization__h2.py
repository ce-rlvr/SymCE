import sympy
from sympy import Interval, FiniteSet, Union, oo, S

# Top-level setup
# (No specific named algebraic objects needed for this real analysis theorem)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should provide a point x and a set K (subset of Reals).
    """
    try:
        if isinstance(witness, dict):
            x_val = witness.get('x')
            K = witness.get('K')
        else:
            x_val, K = witness
            
        # H1: (X, d) is a metric space
        # We implicitly use X = Reals and d(a, b) = |a - b|, which forms a valid metric space.
        h1 = True
        
        # H2: x is a point in X
        h2 = (x_val in S.Reals)
        
        # Calculate inf_{z \in K} d(x, z)
        if K.is_EmptySet:
            inf_dist = oo
        else:
            def get_inf(subK):
                if isinstance(subK, FiniteSet):
                    return min(abs(x_val - z) for z in subK)
                elif isinstance(subK, Interval):
                    a, b = subK.start, subK.end
                    if x_val < a:
                        return a - x_val
                    elif x_val > b:
                        return x_val - b
                    else:
                        return 0
                else:
                    raise ValueError("Unsupported set type")
            
            if isinstance(K, Union):
                inf_dist = min(get_inf(arg) for arg in K.args)
            else:
                inf_dist = get_inf(K)
                
        # neg_Q: There does NOT exist y in K such that d(x, y) == inf_dist
        if inf_dist == oo:
            found_y = False
        elif inf_dist == 0:
            found_y = K.contains(x_val)
        else:
            found_y = K.contains(x_val - inf_dist) or K.contains(x_val + inf_dist)
            
        neg_q = not found_y
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: x is a point in X",
    "¬Q: There does not exist y in K such that d(x, y) = inf_{z \in K} d(x, z)"
]

N_HYP = 2
NEG_Q_INDEX = 2