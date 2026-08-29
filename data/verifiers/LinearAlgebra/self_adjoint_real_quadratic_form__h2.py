import sympy as sp
from sympy import Matrix, I, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_complex(val, tol=1e-9):
    try:
        return abs(complex(val)) < tol
    except Exception:
        try:
            val = sp.simplify(val)
            if val == 0:
                return True
            return abs(complex(val.evalf())) < tol
        except Exception:
            return False

def is_real_complex(val, tol=1e-9):
    try:
        return abs(complex(val).imag) < tol
    except Exception:
        try:
            val = sp.simplify(val)
            if sp.im(val) == 0:
                return True
            return abs(complex(val.evalf()).imag) < tol
        except Exception:
            return False

def get_dim(witness, vectors):
    for v in vectors:
        try:
            res = witness(v)
            if not isinstance(res, Matrix):
                res = Matrix(res)
            if res.shape == v.shape:
                return v.shape[0]
        except Exception:
            continue
    return None

def conditions(witness):
    vectors = [
        Matrix([[1]]), Matrix([[I]]), Matrix([[1+I]]), Matrix([[-1+2*I]]),
        Matrix([[1], [0]]), Matrix([[0], [I]]), Matrix([[1+I], [2-I]]), Matrix([[I], [I]]),
        Matrix([[1], [2], [3]]), Matrix([[I], [1+I], [-I]]), Matrix([[1-I], [2], [3+I]])
    ]

    # H_1: V is an inner product space over the field of complex numbers
    h1_ok = False
    try:
        if isinstance(witness, Matrix):
            h1_ok = witness.is_square
        elif callable(witness):
            dim = get_dim(witness, vectors)
            if dim is not None:
                h1_ok = True
    except Exception:
        pass

    # H_2: <Tx, x> is real for all x in V
    h2_ok = False
    try:
        if isinstance(witness, Matrix):
            if witness.is_square:
                h2_ok = True
                for v in vectors:
                    if v.shape[0] == witness.shape[0]:
                        ip = (v.H * witness * v)[0]
                        if not is_real_complex(ip):
                            h2_ok = False
                            break
        elif callable(witness):
            dim = get_dim(witness, vectors)
            if dim is not None:
                h2_ok = True
                for v in vectors:
                    if v.shape[0] == dim:
                        Tv = witness(v)
                        if not isinstance(Tv, Matrix):
                            Tv = Matrix(Tv)
                        ip = (v.H * Tv)[0]
                        if not is_real_complex(ip):
                            h2_ok = False
                            break
    except Exception:
        h2_ok = False

    # ¬Q: T is not a self-adjoint operator
    # A self-adjoint operator must be both linear and self-adjoint.
    neg_q_ok = False
    try:
        if isinstance(witness, Matrix):
            diff = witness - witness.H
            neg_q_ok = not all(is_zero_complex(val) for val in diff)
        elif callable(witness):
            dim = get_dim(witness, vectors)
            if dim is None:
                neg_q_ok = True
            else:
                valid_vecs = [v for v in vectors if v.shape[0] == dim]
                is_linear = True
                is_self_adjoint = True
                
                # Check additivity
                for u in valid_vecs:
                    for v in valid_vecs:
                        Tu = witness(u)
                        Tv = witness(v)
                        Tuv = witness(u + v)
                        if not isinstance(Tu, Matrix): Tu = Matrix(Tu)
                        if not isinstance(Tv, Matrix): Tv = Matrix(Tv)
                        if not isinstance(Tuv, Matrix): Tuv = Matrix(Tuv)
                        
                        diff = Tuv - (Tu + Tv)
                        if not all(is_zero_complex(val) for val in diff):
                            is_linear = False
                            break
                    if not is_linear: break
                
                # Check homogeneity
                if is_linear:
                    for u in valid_vecs:
                        for c in [2, I, 1-I]:
                            Tu = witness(u)
                            Tcu = witness(c * u)
                            if not isinstance(Tu, Matrix): Tu = Matrix(Tu)
                            if not isinstance(Tcu, Matrix): Tcu = Matrix(Tcu)
                            
                            diff = Tcu - c * Tu
                            if not all(is_zero_complex(val) for val in diff):
                                is_linear = False
                                break
                        if not is_linear: break
                
                # Check self-adjointness
                if is_linear:
                    for u in valid_vecs:
                        for v in valid_vecs:
                            Tu = witness(u)
                            Tv = witness(v)
                            if not isinstance(Tu, Matrix): Tu = Matrix(Tu)
                            if not isinstance(Tv, Matrix): Tv = Matrix(Tv)
                            
                            ip1 = (v.H * Tu)[0]
                            ip2 = (Tv.H * u)[0]
                            if not is_zero_complex(ip1 - ip2):
                                is_self_adjoint = False
                                break
                        if not is_self_adjoint: break
                
                neg_q_ok = not (is_linear and is_self_adjoint)
        else:
            neg_q_ok = True
    except Exception:
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is an inner product space over the field of complex numbers",
    "H_2: <Tx, x> is real for all x in V",
    "¬Q: T is not a self-adjoint operator"
]

N_HYP = 2
NEG_Q_INDEX = 2