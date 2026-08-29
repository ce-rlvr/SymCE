import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    # H_1: U is a 2n x 2n matrix
    try:
        if not isinstance(witness, sp.MatrixBase):
            h1 = False
        elif witness.rows != witness.cols:
            h1 = False
        elif witness.rows == 0 or witness.rows % 2 != 0:
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    neg_q = False
    if h1:
        try:
            n = witness.rows // 2
            U11 = witness[:n, :n]
            U12 = witness[:n, n:]
            U21 = witness[n:, :n]
            U22 = witness[n:, n:]

            def is_zero(expr):
                if expr == 0:
                    return True
                try:
                    expr_exp = sp.expand(expr)
                    if expr_exp == 0:
                        return True
                    expr_simp = sp.simplify(expr_exp)
                    if expr_simp == 0:
                        return True
                except Exception:
                    pass
                return False

            def commutes(A, B):
                diff = A * B - B * A
                for i in range(diff.rows):
                    for j in range(diff.cols):
                        if not is_zero(diff[i, j]):
                            return False
                return True

            def is_hermitian(M):
                diff = M - M.H
                for i in range(diff.rows):
                    for j in range(diff.cols):
                        if not is_zero(diff[i, j]):
                            return False
                return True

            # Necessary conditions for the CS decomposition to hold:
            # 1. The Gram matrices of the blocks must commute appropriately.
            if not commutes(U11.H * U11, U21.H * U21):
                neg_q = True
            elif not commutes(U11 * U11.H, U12 * U12.H):
                neg_q = True
            elif not commutes(U22.H * U22, U12.H * U12):
                neg_q = True
            elif not commutes(U22 * U22.H, U21 * U21.H):
                neg_q = True
            else:
                # 2. The cyclic products of the blocks must be Hermitian matrices.
                cycles = [
                    U11 * U21.H * U22 * U12.H,
                    U21.H * U22 * U12.H * U11,
                    U22 * U12.H * U11 * U21.H,
                    U12.H * U11 * U21.H * U22,
                    U11.H * U12 * U22.H * U21,
                    U12 * U22.H * U21 * U11.H,
                    U22.H * U21 * U11.H * U12,
                    U21 * U11.H * U12 * U22.H
                ]
                for C in cycles:
                    if not is_hermitian(C):
                        neg_q = True
                        break
        except Exception:
            neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a 2n x 2n matrix partitioned into four n x n blocks",
    "¬Q: The CS decomposition into real diagonal matrices fails"
]

N_HYP = 1
NEG_Q_INDEX = 1