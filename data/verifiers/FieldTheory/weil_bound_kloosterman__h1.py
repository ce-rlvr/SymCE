import sympy
import math
import cmath
import itertools

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a dictionary or a tuple.
    Format 1 (F_p[t]/(t^k)): (p, k, a, b)
    Format 2 (Custom Algebra): (p, dim, mult_table, a, b)
    where mult_table[i][j][m] is the coefficient of e_m in e_i * e_j.
    """
    try:
        if isinstance(witness, dict):
            p = witness['p']
            if 'mult_table' in witness:
                dim = witness['dim']
                mult_table = witness['mult_table']
                a = witness['a']
                b = witness['b']
            else:
                dim = witness['k']
                a = witness['a']
                b = witness['b']
                mult_table = [[[0]*dim for _ in range(dim)] for _ in range(dim)]
                for i in range(dim):
                    for j in range(dim - i):
                        mult_table[i][j][i+j] = 1
        else:
            if len(witness) == 5:
                p, dim, mult_table, a, b = witness
            elif len(witness) == 4:
                p, dim, a, b = witness
                mult_table = [[[0]*dim for _ in range(dim)] for _ in range(dim)]
                for i in range(dim):
                    for j in range(dim - i):
                        mult_table[i][j][i+j] = 1
            else:
                return [False, False, False]

        q = p ** dim
        if q > 100000:
            return [False, False, False]

        if isinstance(a, int):
            a = [a]
        if isinstance(b, int):
            b = [b]
        a = list(a)
        b = list(b)
        if len(a) < dim:
            a += [0] * (dim - len(a))
        if len(b) < dim:
            b += [0] * (dim - len(b))

        def mul(u, v):
            res = [0] * dim
            for i in range(dim):
                if u[i] == 0: continue
                for j in range(dim):
                    if v[j] == 0: continue
                    for m in range(dim):
                        res[m] = (res[m] + u[i] * v[j] * mult_table[i][j][m]) % p
            return res

        id_elem = [1] + [0] * (dim - 1)
        for i in range(dim):
            test_elem = [0] * dim
            test_elem[i] = 1
            if mul(id_elem, test_elem) != test_elem:
                return [False, False, False]
            if mul(test_elem, id_elem) != test_elem:
                return [False, False, False]

        def get_inv_fast(u):
            mat_data = []
            for m in range(dim):
                row = []
                for j in range(dim):
                    val = sum(u[i] * mult_table[i][j][m] for i in range(dim)) % p
                    row.append(val)
                mat_data.append(row)
            
            M_u = sympy.Matrix(mat_data)
            id_vec = sympy.Matrix(dim, 1, id_elem)
            try:
                det = int(M_u.det()) % p
                if det == 0:
                    return None
                det_inv = pow(det, -1, p)
                adj = M_u.adjugate()
                M_u_inv = adj.applyfunc(lambda val: (det_inv * int(val)) % p)
                y_vec = M_u_inv * id_vec
                y = [int(y_vec[i]) % p for i in range(dim)]
                if mul(u, y) == id_elem and mul(y, u) == id_elem:
                    return y
            except Exception:
                pass
            return None

        def trace(u):
            tr = 0
            for j in range(dim):
                for i in range(dim):
                    tr += u[i] * mult_table[i][j][j]
            return tr % p

        if not sympy.isprime(p):
            h1 = False
        else:
            a_zero = all(c % p == 0 for c in a)
            b_zero = all(c % p == 0 for c in b)
            h1 = not a_zero and not b_zero

        if not h1:
            return [False, False, False]

        k_sum = 0j
        elements = itertools.product(range(p), repeat=dim)
        for x_tuple in elements:
            if all(c == 0 for c in x_tuple):
                continue
            x_val = list(x_tuple)
            x_inv = get_inv_fast(x_val)
            if x_inv is not None:
                ax = mul(a, x_val)
                bx_inv = mul(b, x_inv)
                val = [(ax[i] + bx_inv[i]) % p for i in range(dim)]
                tr = trace(val)
                k_sum += cmath.exp(2j * math.pi * tr / p)
        
        h2 = True
        
        neg_q_ok = abs(k_sum) > 2 * math.sqrt(q) + 1e-9

        return [h1, h2, neg_q_ok]

    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of F",
    "H_2: K(a,b) is the Kloosterman sum defined as sum_{x in F^x} exp(2pi i Tr(ax+bx^-1)/p)",
    "¬Q: The absolute value |K(a,b)| is NOT bounded above by 2*sqrt(q)"
]

N_HYP = 2
NEG_Q_INDEX = 2