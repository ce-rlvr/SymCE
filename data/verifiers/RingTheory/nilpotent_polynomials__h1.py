import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = False
        if isinstance(witness, list) and len(witness) > 0:
            from sympy import MatrixBase, Expr
            if isinstance(witness[0], MatrixBase):
                shape = witness[0].shape
                if shape[0] == shape[1]:
                    h1 = all(isinstance(m, MatrixBase) and m.shape == shape for m in witness)
            else:
                h1 = all(isinstance(m, Expr) or isinstance(m, (int, float)) for m in witness)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            from sympy import MatrixBase
            
            def poly_mul(p, q):
                if not p or not q: return []
                n = len(p) - 1
                m = len(q) - 1
                if isinstance(p[0], MatrixBase):
                    k = p[0].shape[0]
                    zero_elem = zeros(k, k)
                else:
                    zero_elem = 0
                res = [zero_elem] * (n + m + 1)
                for i in range(n + 1):
                    for j in range(m + 1):
                        res[i+j] = res[i+j] + p[i] * q[j]
                while len(res) > 1 and res[-1] == zero_elem:
                    res.pop()
                return res

            def is_nilpotent(a):
                if isinstance(a, MatrixBase):
                    k = a.shape[0]
                    return a**k == zeros(k, k)
                else:
                    return a == 0

            def is_poly_nilpotent(p):
                if not p: return True
                if isinstance(p[0], MatrixBase):
                    k = p[0].shape[0]
                    zero_elem = zeros(k, k)
                    pk = p
                    for _ in range(20):
                        if all(c == zero_elem for c in pk):
                            return True
                        pk = poly_mul(pk, p)
                    return False
                else:
                    return all(c == 0 for c in p)

            poly_nilp = is_poly_nilpotent(witness)
            coeffs_nilp = all(is_nilpotent(a) for a in witness)
            
            neg_q = (poly_nilp != coeffs_nilp)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: f is a polynomial in R", "not Q: f is nilpotent iff all a_i are nilpotent is FALSE"]
N_HYP = 1
NEG_Q_INDEX = 1