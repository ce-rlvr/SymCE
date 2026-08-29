import sympy
from sympy import isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "Let F be a field. Then F is a Euclidean domain with respect to the Euclidean function d."
    
    A valid witness provides a field F and a function d that fails the Euclidean domain conditions.
    For simplicity, we evaluate finite prime fields F = Z/pZ.
    The witness can be:
      - A dictionary mapping 1..p-1 to non-negative integers (where p = len(witness) + 1).
      - A list of non-negative integers of length p-1.
      - A tuple (p, d) where p is the prime order and d is a dict, list, or callable.
    """
    h1 = False
    neg_q = False
    
    try:
        p = None
        d_func = None
        
        if isinstance(witness, dict):
            p = len(witness) + 1
            d_func = lambda x: witness[x]
        elif isinstance(witness, list):
            p = len(witness) + 1
            d_func = lambda x: witness[x - 1]
        elif isinstance(witness, tuple) and len(witness) == 2:
            p_obj, d_obj = witness
            
            if isinstance(p_obj, int):
                p = p_obj
            else:
                if hasattr(p_obj, 'domain') and hasattr(p_obj.domain, 'order'):
                    p = p_obj.domain.order
                elif hasattr(p_obj, 'order'):
                    p = p_obj.order() if callable(p_obj.order) else p_obj.order
                elif hasattr(p_obj, 'mod'):
                    p = p_obj.mod
                p = int(p)
                
            if isinstance(d_obj, dict):
                d_func = lambda x: d_obj[x]
            elif isinstance(d_obj, list):
                d_func = lambda x: d_obj[x - 1]
            elif callable(d_obj):
                d_func = d_obj

        if p is not None and d_func is not None:
            if isprime(p):
                d_vals = {}
                valid_d = True
                for i in range(1, p):
                    try:
                        v = d_func(i)
                        if not isinstance(v, int) or v < 0:
                            valid_d = False
                            break
                        d_vals[i] = v
                    except Exception:
                        valid_d = False
                        break
                
                if valid_d:
                    h1 = True
                    
                    is_euclidean = True
                    # Condition 1: d(a) <= d(ab) for all a, b in F*
                    for a in range(1, p):
                        for b in range(1, p):
                            ab = (a * b) % p
                            if d_vals[a] > d_vals[ab]:
                                is_euclidean = False
                                break
                        if not is_euclidean:
                            break
                            
                    # Condition 2: Division algorithm
                    # For all a in F, b in F*, exists q, r in F s.t. a = bq + r and (r == 0 or d(r) < d(b))
                    if is_euclidean:
                        for a in range(p):
                            for b in range(1, p):
                                exists = False
                                for q in range(p):
                                    r = (a - b * q) % p
                                    if r == 0 or d_vals[r] < d_vals[b]:
                                        exists = True
                                        break
                                if not exists:
                                    is_euclidean = False
                                    break
                            if not is_euclidean:
                                break
                                
                    neg_q = not is_euclidean
                    
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: F is not a Euclidean domain with respect to d"
]

N_HYP = 1
NEG_Q_INDEX = 1