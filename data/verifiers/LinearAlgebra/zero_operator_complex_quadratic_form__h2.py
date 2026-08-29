import sympy
from sympy import symbols, Matrix, I, simplify, expand, eye, zeros
import math

# Top-level setup for standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_test_vectors(dim, num_vectors=50):
    """Generate deterministic pseudo-random complex vectors for testing."""
    vectors = []
    for i in range(num_vectors):
        vec = []
        for j in range(dim):
            idx = i * dim + j
            r = 10 * math.sin(idx * 1.234 + i)
            im = 10 * math.cos(idx * 2.345 - i)
            vec.append(r + I * im)
        vectors.append(Matrix(vec))
    return vectors

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a non-linear operator T on a complex inner product space.
    """
    dim = None
    apply_T = None
    
    # Determine the dimension of the space and how to apply the operator T
    for n in range(1, 10):
        v_test = Matrix([1]*n)
        
        # Try as a callable function
        if callable(witness):
            try:
                res = witness(v_test)
                res_mat = Matrix(res)
                if res_mat.shape == (n, 1) or res_mat.shape == (1, n):
                    dim = n
                    apply_T = lambda v, w=witness, d=n: Matrix(w(v)).reshape(d, 1)
                    break
            except Exception:
                pass
                
        # Try as an object supporting multiplication (e.g., a matrix or custom class)
        try:
            res = witness * v_test
            res_mat = Matrix(res)
            if res_mat.shape == (n, 1) or res_mat.shape == (1, n):
                dim = n
                apply_T = lambda v, w=witness, d=n: Matrix(w * v).reshape(d, 1)
                break
        except Exception:
            pass
            
    if dim is None or apply_T is None:
        return [False, False, False]

    # H_1: V is an inner product space over the field of complex numbers
    # We verify this by checking if T can operate on complex vectors.
    try:
        v_test = Matrix([1 + I]*dim)
        res = apply_T(v_test)
        h1_ok = isinstance(res, Matrix) and res.shape == (dim, 1)
    except Exception:
        h1_ok = False

    # H_2: <Tx, x> = 0 for all x in V
    h2_ok = False
    try:
        if dim > 4:
            raise ValueError("Skip symbolic evaluation for large dimensions to ensure speed")
        reals = symbols(f'r0:{dim}', real=True)
        imags = symbols(f'i0:{dim}', real=True)
        v = Matrix([r + I*im for r, im in zip(reals, imags)])
        res = apply_T(v)
        # Inner product <Tx, x> over C is computed as x.adjoint() * Tx
        ip = (v.adjoint() * res)[0]
        ip_simp = simplify(expand(ip))
        if ip_simp == 0:
            h2_ok = True
        else:
            # Fallback to numerical evaluation if symbolic doesn't simplify to 0
            h2_ok = True
            for v_num in get_test_vectors(dim, 50):
                res_num = apply_T(v_num.copy())
                ip_num = (v_num.adjoint() * res_num)[0]
                if abs(complex(ip_num.evalf())) > 1e-7:
                    h2_ok = False
                    break
    except Exception:
        # If symbolic evaluation fails entirely, rely purely on numerical testing
        try:
            h2_ok = True
            for v_num in get_test_vectors(dim, 50):
                res_num = apply_T(v_num.copy())
                ip_num = (v_num.adjoint() * res_num)[0]
                if abs(complex(ip_num.evalf())) > 1e-7:
                    h2_ok = False
                    break
        except Exception:
            h2_ok = False

    # neg_Q: T is not the zero operator
    neg_q_ok = False
    try:
        if dim > 4:
            raise ValueError("Skip symbolic evaluation for large dimensions to ensure speed")
        reals = symbols(f'r0:{dim}', real=True)
        imags = symbols(f'i0:{dim}', real=True)
        v = Matrix([r + I*im for r, im in zip(reals, imags)])
        res = apply_T(v)
        if not all(simplify(c) == 0 for c in res):
            neg_q_ok = True
    except Exception:
        pass
        
    if not neg_q_ok:
        try:
            for v_num in get_test_vectors(dim, 50):
                res_num = apply_T(v_num.copy())
                if any(abs(complex(c.evalf())) > 1e-7 for c in res_num):
                    neg_q_ok = True
                    break
        except Exception:
            pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    r"H_1: V is an inner product space over the field of complex numbers",
    r"H_2: \langle Tx, x \rangle = 0 for all x \in V",
    r"¬Q: T is not the zero operator"
]

N_HYP = 2
NEG_Q_INDEX = 2