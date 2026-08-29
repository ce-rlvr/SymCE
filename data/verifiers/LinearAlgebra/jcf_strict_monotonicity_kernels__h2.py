import sympy as sp
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) == 3:
            A, lambda_val, m_wit = witness
        elif len(witness) == 2:
            A, lambda_val = witness
            m_wit = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: A is an n x n complex matrix
    try:
        if not isinstance(A, sp.MatrixBase):
            h1 = False
        elif A.shape[0] != A.shape[1]:
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # H2: m is the index of lambda
    try:
        if not h1:
            h2 = False
        else:
            n = A.shape[0]
            I = sp.eye(n)
            T = A - lambda_val * I
            
            ranks = [n]
            Tk = I
            # The sequence of kernels stabilizes in at most n steps
            for k in range(1, n + 2):
                Tk = Tk * T
                ranks.append(Tk.rank())
                
            m_actual = 0
            for k in range(len(ranks) - 1):
                if ranks[k] == ranks[k+1]:
                    m_actual = k
                    break
                    
            if m_wit is not None:
                h2 = bool(m_wit == m_actual)
            else:
                h2 = True
                m_wit = m_actual
    except Exception:
        h2 = False

    # ¬Q: The sequence of dimensions is NOT strictly increasing for 0 <= k <= m
    try:
        if not h1 or m_wit is None:
            neg_q = False
        else:
            # dim(ker(T^k)) = n - rank(T^k)
            dims = [n - ranks[k] for k in range(m_wit + 1)]
            
            is_increasing = True
            # A sequence must have at least 2 elements to be strictly increasing in this context.
            # If lambda is not an eigenvalue, m=0, and the sequence is just [0], which is not strictly increasing.
            if len(dims) < 2:
                is_increasing = False
            else:
                for i in range(len(dims) - 1):
                    if dims[i] >= dims[i+1]:
                        is_increasing = False
                        break
                        
            neg_q = not is_increasing
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "H_2: m is the index of lambda",
    "¬Q: The sequence of dimensions is not strictly increasing for 0 <= k <= m"
]

N_HYP = 2
NEG_Q_INDEX = 2