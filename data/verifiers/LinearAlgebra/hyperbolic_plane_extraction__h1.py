import sympy
from sympy import Matrix, eye, zeros
from itertools import product

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            B = witness.get('B')
            x = witness.get('x')
            p = witness.get('p', 0)
        elif isinstance(witness, tuple) and len(witness) == 3:
            B, x, p = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            B, x = witness
            p = 0
        else:
            return [False, False, False]
            
        p = int(p)
        if p > 0 and not sympy.isprime(p):
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: B is a non-degenerate symmetric bilinear form on V
    try:
        if not isinstance(B, Matrix):
            h1 = False
        elif B.shape[0] != B.shape[1]:
            h1 = False
        else:
            n = B.shape[0]
            sym = True
            for i in range(n):
                for j in range(n):
                    val = B[i, j] - B[j, i]
                    if p > 0:
                        val = val % p
                    if val != 0:
                        sym = False
            det = B.det()
            if p > 0:
                det = det % p
            non_deg = (det != 0)
            h1 = sym and non_deg
    except Exception:
        h1 = False

    # H2: There exists a non-zero vector x in V such that B(x,x) = 0
    try:
        if not isinstance(x, Matrix):
            h2 = False
        else:
            n = B.shape[0]
            if x.shape != (n, 1):
                h2 = False
            else:
                is_zero = True
                for i in range(n):
                    val = x[i, 0]
                    if p > 0:
                        val = val % p
                    if val != 0:
                        is_zero = False
                
                b_xx = (x.T * B * x)[0]
                if p > 0:
                    b_xx = b_xx % p
                
                h2 = (not is_zero) and (b_xx == 0)
    except Exception:
        h2 = False

    # neg_Q: For all y in V, B(y,y) != 0 or B(x,y) != 1
    try:
        n = B.shape[0]
        if p <= 0 or p**n > 100000:
            neg_q = False
        else:
            exists_y = False
            for elements in product(range(p), repeat=n):
                y = Matrix(n, 1, elements)
                
                b_yy = (y.T * B * y)[0]
                b_xy = (x.T * B * y)[0]
                
                if p > 0:
                    b_yy = b_yy % p
                    b_xy = b_xy % p
                
                if b_yy == 0 and b_xy == 1:
                    exists_y = True
                    break
            
            neg_q = not exists_y
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: B is a non-degenerate symmetric bilinear form on V",
    "H_2: There exists a non-zero vector x in V such that B(x,x) = 0",
    "¬Q: There is no vector y in V such that B(y,y) = 0 and B(x,y) = 1"
]

N_HYP = 2
NEG_Q_INDEX = 2