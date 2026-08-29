import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        A = witness
        if not isinstance(A, sp.MatrixBase):
            A = sp.Matrix(A)
        
        m, n = A.shape
        if m != n:
            # If A is not square, the set of matrices commuting with A is empty.
            # An empty set is not a vector space, so it does not have a dimension >= n.
            neg_q = True
        else:
            # If A is square, compute the dimension of its centralizer.
            # We find the rank of the linear operator T(B) = AB - BA.
            M_rows = []
            for i in range(n):
                for j in range(n):
                    row = []
                    for k in range(n):
                        for l in range(n):
                            val = 0
                            if l == j:
                                val += A[i, k]
                            if k == i:
                                val -= A[l, j]
                            row.append(val)
                    M_rows.append(row)
            
            M = sp.Matrix(M_rows)
            rank = M.rank()
            dim = n**2 - rank
            
            # The conclusion is that the dimension is at least n.
            # The negated conclusion is that the dimension is strictly less than n.
            neg_q = bool(dim < n)
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The dimension of the vector space of all matrices commuting with A is less than n (or undefined)"
]

N_HYP = 0
NEG_Q_INDEX = 0