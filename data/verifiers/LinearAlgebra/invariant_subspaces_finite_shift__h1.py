import z3
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, W_raw = witness
            W = Matrix(W_raw)
        else:
            W = Matrix(witness)
            n = W.shape[1]
            
        m = W.shape[0]
        for i in range(m):
            for j in range(n):
                if W[i, j] != int(W[i, j]):
                    return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = (n >= 1) and (W.shape[1] == n)
    except Exception:
        h1 = False

    h2 = True

    try:
        def in_span(v, mat):
            solver = z3.Solver()
            x = [z3.Int(f'x_{i}') for i in range(m)]
            for j in range(n):
                wj = [int(mat[i, j]) for i in range(m)]
                vj = int(v[0, j])
                eq = sum(x[i] * wj[i] for i in range(m)) == vj
                solver.add(eq)
            return solver.check() == z3.sat

        is_invariant = True
        for i in range(m):
            v = W.row(i)
            Tv = Matrix([[0] + list(v)[0:-1]])
            if not in_span(Tv, W):
                is_invariant = False
                break
        
        if not is_invariant:
            neg_q = False
        else:
            is_zero = all(int(W[i, j]) == 0 for i in range(m) for j in range(n))
            if is_zero:
                neg_q = False
            else:
                is_any_Wk = False
                for k in range(1, n + 1):
                    w_sub_wk = True
                    for i in range(m):
                        for j in range(k - 1):
                            if int(W[i, j]) != 0:
                                w_sub_wk = False
                                break
                        if not w_sub_wk:
                            break
                    
                    if w_sub_wk:
                        wk_sub_w = True
                        for i in range(k - 1, n):
                            ei = Matrix([[1 if j == i else 0 for j in range(n)]])
                            if not in_span(ei, W):
                                wk_sub_w = False
                                break
                        if wk_sub_w:
                            is_any_Wk = True
                            break
                
                neg_q = not is_any_Wk

    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (e_1, ..., e_n) is an ordered basis for V",
    "H_2: T is a linear operator on V defined by T(e_i) = e_{i+1} and T(e_n) = 0",
    "¬Q: W is a T-invariant subspace but W != {0} and W != W_k for all k"
]

N_HYP = 2
NEG_Q_INDEX = 2