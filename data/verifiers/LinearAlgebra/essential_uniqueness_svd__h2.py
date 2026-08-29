import sympy as sp
from sympy.matrices import MatrixBase
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero(expr):
    try:
        s = sp.simplify(expr)
        if s == 0:
            return True
        if abs(complex(s)) < 1e-9:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    A = U1 = V1 = U2 = V2 = None
    r = 0
    
    # Unpack witness
    if isinstance(witness, dict):
        A = witness.get('A')
        U1 = witness.get('U1')
        V1 = witness.get('V1')
        U2 = witness.get('U2')
        V2 = witness.get('V2')
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 5:
            A, U1, V1, U2, V2 = witness
        elif len(witness) == 7:
            A, U1, _, V1, U2, _, V2 = witness

    # H_1: A is an m x n complex matrix of rank r
    try:
        h1_ok = False
        if isinstance(A, MatrixBase):
            r = A.rank()
            h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: All r non-zero singular values of A are distinct
    try:
        h2_ok = False
        if h1_ok:
            M = A.H * A
            eigenvals = M.eigenvals()
            non_zero_eigenvals = []
            for ev, mult in eigenvals.items():
                if not is_zero(ev):
                    non_zero_eigenvals.append((ev, mult))
            
            # Distinct non-zero singular values mean all non-zero eigenvalues of A*A have multiplicity 1
            if all(mult == 1 for ev, mult in non_zero_eigenvals):
                if sum(mult for ev, mult in non_zero_eigenvals) == r:
                    h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: The conclusion FAILS
    try:
        neg_q_ok = False
        if h1_ok:
            if not (isinstance(U1, MatrixBase) and isinstance(V1, MatrixBase) and 
                    isinstance(U2, MatrixBase) and isinstance(V2, MatrixBase)):
                neg_q_ok = True
            elif U1.cols < r or U2.cols < r or V1.cols < r or V2.cols < r:
                neg_q_ok = True
            else:
                exists_D = True
                for j in range(r):
                    w1 = list(U1[:, j]) + list(V1[:, j])
                    w2 = list(U2[:, j]) + list(V2[:, j])
                    
                    if len(w1) != len(w2):
                        exists_D = False
                        break
                    
                    idx = -1
                    for i in range(len(w1)):
                        if not is_zero(w1[i]):
                            idx = i
                            break
                    
                    if idx == -1:
                        if any(not is_zero(x) for x in w2):
                            exists_D = False
                            break
                    else:
                        d = sp.simplify(w2[idx] / w1[idx])
                        if not is_zero(d * sp.conjugate(d) - 1):
                            exists_D = False
                            break
                        
                        match = True
                        for i in range(len(w1)):
                            if i != idx:
                                if not is_zero(w2[i] - d * w1[i]):
                                    match = False
                                    break
                        if not match:
                            exists_D = False
                            break
                
                neg_q_ok = not exists_D
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: A is an m by n complex matrix of rank r", "H_2: All r non-zero singular values of A are distinct", "not Q: There is no diagonal matrix D with absolute value 1 diagonal entries such that U2 is U1 D and V2 is V1 D"]
N_HYP = 2
NEG_Q_INDEX = 2