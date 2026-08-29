import sympy as sp
import itertools

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    A_rows = None
    A_cols = None
    Q = None

    def find_submatrix(Q_mat, A_mat):
        if not isinstance(A_mat, sp.MatrixBase) or not A_mat.is_square:
            return None, None
        n = Q_mat.shape[0]
        k = A_mat.shape[0]
        for rows in itertools.combinations(range(n), k):
            for cols in itertools.combinations(range(n), k):
                if Q_mat.extract(rows, cols) == A_mat:
                    return list(rows), list(cols)
        return None, None

    try:
        if isinstance(witness, dict):
            Q = witness.get('Q')
            if 'A_rows' in witness and 'A_cols' in witness:
                A_rows = list(witness['A_rows'])
                A_cols = list(witness['A_cols'])
            elif 'A' in witness:
                A_rows, A_cols = find_submatrix(Q, witness['A'])
        elif isinstance(witness, (tuple, list)):
            Q = witness[0]
            if isinstance(witness[1], sp.MatrixBase):
                A_rows, A_cols = find_submatrix(Q, witness[1])
            else:
                A_rows = list(witness[1])
                A_cols = list(witness[2])
    except Exception:
        pass

    # H1: Q is an n x n real matrix
    h1 = False
    try:
        if isinstance(Q, sp.MatrixBase) and Q.is_square:
            if Q.conjugate() == Q:
                h1 = True
    except Exception:
        pass

    # H2: Q is an orthogonal matrix
    h2 = False
    try:
        if h1:
            n = Q.shape[0]
            I = sp.eye(n)
            diff = sp.expand(Q.T * Q - I)
            if diff.is_zero_matrix:
                h2 = True
            else:
                diff = sp.simplify(diff)
                if diff.is_zero_matrix:
                    h2 = True
                else:
                    try:
                        h2 = all(abs(float(e)) < 1e-12 for e in diff)
                    except Exception:
                        h2 = False
    except Exception:
        pass

    # H3: B is the (n-k) x (n-k) complementary submatrix of A in Q
    h3 = False
    try:
        if h1 and A_rows is not None and A_cols is not None:
            n = Q.shape[0]
            if len(A_rows) == len(A_cols):
                k = len(A_rows)
                if all(0 <= r < n for r in A_rows) and all(0 <= c < n for c in A_cols):
                    if len(set(A_rows)) == k and len(set(A_cols)) == k:
                        B_expected = None
                        if isinstance(witness, dict) and 'B' in witness:
                            B_expected = witness['B']
                        elif isinstance(witness, (tuple, list)):
                            if len(witness) == 3 and isinstance(witness[1], sp.MatrixBase) and isinstance(witness[2], sp.MatrixBase):
                                B_expected = witness[2]
                            elif len(witness) >= 4 and isinstance(witness[3], sp.MatrixBase):
                                B_expected = witness[3]
                        
                        if B_expected is not None:
                            B_rows = [i for i in range(n) if i not in A_rows]
                            B_cols = [j for j in range(n) if j not in A_cols]
                            B_actual = Q.extract(B_rows, B_cols)
                            
                            diff_B = sp.expand(B_actual - B_expected)
                            if diff_B.is_zero_matrix:
                                h3 = True
                            else:
                                diff_B = sp.simplify(diff_B)
                                if diff_B.is_zero_matrix:
                                    h3 = True
                                else:
                                    try:
                                        h3 = all(abs(float(e)) < 1e-12 for e in diff_B)
                                    except Exception:
                                        h3 = False
                        else:
                            h3 = True
    except Exception:
        pass

    # Conclusion: The absolute value of the determinant of A is equal to the absolute value of the determinant of B
    neg_q = False
    try:
        if h1 and A_rows is not None and A_cols is not None:
            n = Q.shape[0]
            B_rows = [i for i in range(n) if i not in A_rows]
            B_cols = [j for j in range(n) if j not in A_cols]
            
            A = Q.extract(A_rows, A_cols)
            B = Q.extract(B_rows, B_cols)
            
            detA = A.det()
            detB = B.det()
            
            diff = sp.expand(detA**2 - detB**2)
            if diff == 0:
                conclusion_holds = True
            else:
                diff = sp.simplify(diff)
                if diff == 0:
                    conclusion_holds = True
                else:
                    try:
                        conclusion_holds = abs(float(diff)) < 1e-12
                    except Exception:
                        conclusion_holds = False
                        
            neg_q = not conclusion_holds
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an n x n real matrix",
    "H_2: Q is an orthogonal matrix",
    "H_3: B is the (n-k) x (n-k) complementary submatrix of A in Q",
    "¬Q: The absolute value of the determinant of A is not equal to the absolute value of the determinant of B"
]

N_HYP = 3
NEG_Q_INDEX = 3