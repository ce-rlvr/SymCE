import sympy
from sympy import Matrix, eye, zeros, QQ, Rational

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    if not isinstance(witness, dict):
        return [False, False, False, False]

    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    # H1: k is a field
    try:
        k = witness.get('k', None)
        if k is not None:
            h1 = bool(hasattr(k, 'is_Field') and k.is_Field)
    except Exception:
        pass

    is_matrix = 'basis' in witness
    is_table = 'table' in witness

    def in_span(mat, basis):
        vecs = [Matrix(list(b)) for b in basis]
        if not vecs:
            return all(c == 0 for c in mat)
        M = Matrix.hstack(*vecs)
        v = Matrix(list(mat))
        M_aug = Matrix.hstack(M, v)
        return M.rank() == M_aug.rank()

    def mul_table(u, v, table, k_field):
        n = len(table)
        res = [k_field(0)] * n
        for i in range(n):
            for j in range(n):
                c = u[i] * v[j]
                for m in range(n):
                    res[m] += c * table[i][j][m]
        return res

    def eq_table(u, v):
        return all(u[i] == v[i] for i in range(len(u)))

    # H2: A is a finite-dimensional algebra over k
    try:
        if is_matrix:
            basis = witness['basis']
            one = witness['one']
            shape = basis[0].shape
            h2 = True
            for b in basis:
                if b.shape != shape: 
                    h2 = False
            for b1 in basis:
                for b2 in basis:
                    if not in_span(b1 * b2, basis):
                        h2 = False
                        break
            if not in_span(one, basis): 
                h2 = False
            for b in basis:
                if one * b != b or b * one != b: 
                    h2 = False
        elif is_table:
            table = witness['table']
            one = witness['one']
            k_field = witness['k']
            n = len(table)
            h2 = True
            for i in range(n):
                b = [k_field(0)] * n
                b[i] = k_field(1)
                if not eq_table(mul_table(one, b, table, k_field), b): 
                    h2 = False
                if not eq_table(mul_table(b, one, table, k_field), b): 
                    h2 = False
    except Exception:
        h2 = False

    # H3: y is in A and yx = 1
    try:
        if is_matrix:
            y = witness['y']
            x = witness['x']
            one = witness['one']
            basis = witness['basis']
            h3 = bool(in_span(y, basis) and (y * x == one))
        elif is_table:
            y = witness['y']
            x = witness['x']
            one = witness['one']
            table = witness['table']
            k_field = witness['k']
            h3 = bool(eq_table(mul_table(y, x, table, k_field), one))
    except Exception:
        h3 = False

    # neg_Q: x is not a unit in A or y is not its unique two-sided inverse
    try:
        if is_matrix:
            y = witness['y']
            x = witness['x']
            one = witness['one']
            basis = witness['basis']
            
            try:
                is_x_in_A = in_span(x, basis)
            except Exception:
                is_x_in_A = False
                
            try:
                xy_eq_one = (x * y == one)
            except Exception:
                xy_eq_one = False
                
            try:
                yx_eq_one = (y * x == one)
            except Exception:
                yx_eq_one = False
                
            q = is_x_in_A and xy_eq_one and yx_eq_one
            neg_q = not q
            
        elif is_table:
            y = witness['y']
            x = witness['x']
            one = witness['one']
            table = witness['table']
            k_field = witness['k']
            
            try:
                xy_eq_one = eq_table(mul_table(x, y, table, k_field), one)
            except Exception:
                xy_eq_one = False
                
            try:
                yx_eq_one = eq_table(mul_table(y, x, table, k_field), one)
            except Exception:
                yx_eq_one = False
                
            q = xy_eq_one and yx_eq_one
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: A is a finite-dimensional algebra over k",
    "H_3: y is in A and yx = 1",
    "¬Q: x is not a unit in A or y is not its unique two-sided inverse"
]

N_HYP = 3
NEG_Q_INDEX = 3