import sympy as sp
from sympy import Matrix, I

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        T = witness['T']
        B_raw = witness['B']
        lam = witness['lam']
        mu = witness['mu']
        x = witness['x']
        y = witness['y']
    except KeyError:
        return [False] * 5

    if callable(B_raw):
        B = B_raw
    elif getattr(B_raw, 'is_Matrix', False):
        B = lambda u, v: (u.T * B_raw * v.conjugate())[0, 0]
    else:
        B = None

    # H1: V is a vector space over a field F
    try:
        if not getattr(T, 'is_Matrix', False) or not T.is_square:
            h1 = False
        else:
            n = T.shape[0]
            if not getattr(x, 'is_Matrix', False) or x.shape != (n, 1) or x.is_zero_matrix:
                h1 = False
            elif not getattr(y, 'is_Matrix', False) or y.shape != (n, 1) or y.is_zero_matrix:
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False

    # H2: T is an isometry of V with respect to B
    try:
        if not h1 or B is None:
            h2 = False
        else:
            n = T.shape[0]
            test_vecs = [x, y]
            for i in range(n):
                v = sp.zeros(n, 1)
                v[i, 0] = 1
                test_vecs.append(v)
                
                v2 = sp.zeros(n, 1)
                v2[i, 0] = I
                test_vecs.append(v2)
                
            for i in range(n):
                for j in range(i+1, n):
                    v = sp.zeros(n, 1)
                    v[i, 0] = 1
                    v[j, 0] = 1
                    test_vecs.append(v)
                    
                    v3 = sp.zeros(n, 1)
                    v3[i, 0] = I
                    v3[j, 0] = 1
                    test_vecs.append(v3)
            
            h2 = True
            for u in test_vecs:
                for v in test_vecs:
                    val1 = B(T*u, T*v)
                    val2 = B(u, v)
                    diff = val1 - val2
                    if getattr(diff, 'is_Matrix', False):
                        diff = diff[0, 0]
                    if sp.simplify(diff) != 0:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: lambda and mu are eigenvalues of T with corresponding eigenvectors x and y
    try:
        if not h1:
            h3 = False
        else:
            eq_x = sp.simplify(T*x - lam*x)
            eq_y = sp.simplify(T*y - mu*y)
            h3 = eq_x.is_zero_matrix and eq_y.is_zero_matrix
    except Exception:
        h3 = False

    # H4: lambda * mu != 1
    try:
        h4 = sp.simplify(lam * mu - 1) != 0
    except Exception:
        h4 = False

    # Negated Conclusion: B(x, y) != 0
    try:
        if B is None:
            neg_q = False
        else:
            val = B(x, y)
            if getattr(val, 'is_Matrix', False):
                val = val[0, 0]
            neg_q = sp.simplify(val) != 0
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: T is an isometry of V with respect to B, such that B(T(u), T(v)) = B(u, v) for all u, v in V",
    "H_3: lambda and mu are eigenvalues of T with corresponding eigenvectors x and y",
    "H_4: lambda * mu != 1",
    "¬Q: The eigenvectors x and y are not orthogonal with respect to B (B(x, y) != 0)"
]

N_HYP = 4
NEG_Q_INDEX = 4