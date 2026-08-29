import sympy as sp
import math

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False

    f = None
    A = None
    H = None

    if callable(witness):
        f = witness
        A = sp.Matrix([[2.0, 1.0], [1.0, 2.0]])
        H = sp.Matrix([[1.0, 0.0], [0.0, -1.0]])
    elif isinstance(witness, sp.Matrix):
        A = witness
        H = sp.eye(A.shape[0])
        def default_f(X):
            d = float(X.det())
            if d <= 0:
                raise ValueError("det <= 0")
            return math.log(d)
        f = default_f
    elif isinstance(witness, tuple):
        if len(witness) == 3 and callable(witness[0]):
            f, A, H = witness
        elif len(witness) == 2:
            if isinstance(witness[0], int) and callable(witness[1]):
                n = witness[0]
                f = witness[1]
                A = sp.eye(n) * 2.0
                H = sp.eye(n)
            elif callable(witness[0]):
                f = witness[0]
                A = witness[1]
                if isinstance(A, sp.Matrix):
                    H = sp.eye(A.shape[0])
            elif callable(witness[1]):
                f = witness[1]
                A = sp.Matrix([[2.0, 1.0], [1.0, 2.0]])
                H = sp.Matrix([[1.0, 0.0], [0.0, -1.0]])
            else:
                A, H = witness
                def default_f(X):
                    d = float(X.det())
                    if d <= 0:
                        raise ValueError("det <= 0")
                    return math.log(d)
                f = default_f

    if f is None or A is None or H is None:
        return [False, False]

    # Test H_1: f is defined by f(A) = ln(det(A)) on GL+(n, R)
    try:
        try:
            det_A = float(A.det())
        except Exception:
            det_A = -1.0

        if det_A <= 0:
            test_A = sp.Matrix([[2.0, 1.0], [1.0, 2.0]])
            det_test = 3.0
        else:
            test_A = A
            det_test = det_A
            
        val = float(f(test_A))
        expected = math.log(det_test)
        h1_ok = abs(val - expected) < 1e-4
    except Exception:
        h1_ok = False

    # Test neg_Q: f is not differentiable or its differential is not tr(A^{-1}H)
    try:
        t = 1e-6
        val_plus = float(f(A + t*H))
        val_minus = float(f(A - t*H))
        diff = (val_plus - val_minus) / (2*t)
        
        A_inv = A.inv()
        expected_diff = float(sp.trace(A_inv * H))
        
        neg_q_ok = abs(diff - expected_diff) > 1e-2
    except Exception:
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is defined by f(A) = ln(det(A))",
    "¬Q: f is not differentiable or its differential is not tr(A^{-1}H)"
]

N_HYP = 1
NEG_Q_INDEX = 1