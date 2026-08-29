import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space of dimension n >= 1",
    "H_2: k is an integer such that 0 <= k <= n",
    "¬Q: There does NOT exist a T-invariant subspace of V of dimension k"
]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            k = witness.get('k')
        else:
            T, k = witness
    except Exception:
        return [False, False, False]

    # H1: V is a finite-dimensional vector space of dimension n >= 1
    try:
        if not hasattr(T, 'shape') or len(T.shape) != 2:
            h1 = False
            n = -1
        else:
            n = T.shape[0]
            h1 = bool(T.shape[0] == T.shape[1] and n >= 1)
    except Exception:
        h1 = False
        n = -1

    # H2: k is an integer such that 0 <= k <= n
    try:
        k_val = int(k)
        h2 = bool(k_val == k and 0 <= k_val <= n)
    except Exception:
        h2 = False

    # neg_Q: There does NOT exist a T-invariant subspace of V of dimension k
    # Over the field of definition, T has an invariant subspace of dimension k
    # if and only if its characteristic polynomial has a factor of degree k.
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            dummy = sp.Dummy('lambda')
            cp = T.charpoly(dummy)
            factors = cp.factor_list()
            
            possible_degrees = {0}
            for poly, mult in factors[1]:
                d = poly.degree()
                new_degrees = set()
                for deg in possible_degrees:
                    for i in range(mult + 1):
                        new_degrees.add(deg + i * d)
                possible_degrees = new_degrees
                
            neg_q = bool(k_val not in possible_degrees)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]