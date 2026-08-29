import sympy as sp
from sympy import Matrix, eye, simplify

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness is expected to be a list or tuple of vectors (each vector being a list, tuple, or sympy Matrix).
    """
    try:
        if not isinstance(witness, (list, tuple)):
            return [False, False]
        
        k = len(witness)
        if k == 0:
            return [False, False]
            
        # Infer n from the dimension of the first vector
        n = len(witness[0])
        
        # Check H_1: Let {v_1, v_2, ..., v_k} be a set of orthonormal vectors in R^n
        h1_ok = True
        for v in witness:
            if len(v) != n:
                h1_ok = False
                break
            for x in v:
                if not sp.sympify(x).is_real:
                    h1_ok = False
                    break
        
        if h1_ok:
            for i in range(k):
                for j in range(k):
                    dot = sum(witness[i][m] * witness[j][m] for m in range(n))
                    expected = 1 if i == j else 0
                    if simplify(dot - expected) != 0:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
                    
        # Check neg_Q: There does NOT exist an n x n real orthogonal matrix Q 
        # whose first k columns are exactly v_1, v_2, ..., v_k.
        # An orthogonal matrix Q of size n x n with these first k columns exists 
        # if and only if k <= n and the given k vectors form a real orthonormal set.
        q_exists = True
        if k > n:
            q_exists = False
        else:
            for v in witness:
                if len(v) != n:
                    q_exists = False
                    break
                for x in v:
                    if not sp.sympify(x).is_real:
                        q_exists = False
                        break
            if q_exists:
                for i in range(k):
                    for j in range(k):
                        dot = sum(witness[i][m] * witness[j][m] for m in range(n))
                        expected = 1 if i == j else 0
                        if simplify(dot - expected) != 0:
                            q_exists = False
                            break
                    if not q_exists:
                        break
                        
        neg_q_ok = not q_exists
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: Let {v_1, v_2, ..., v_k} be a set of orthonormal vectors in R^n",
    "¬Q: There does not exist an n x n real orthogonal matrix Q whose first k columns are exactly v_1, v_2, ..., v_k"
]

N_HYP = 1
NEG_Q_INDEX = 1