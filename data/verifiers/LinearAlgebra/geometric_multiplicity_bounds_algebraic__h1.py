import sympy
from sympy import Symbol, eye, simplify, Matrix, zeros
from sympy.polys import div

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # Parse the witness
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            T, lambda_val = witness
        elif isinstance(witness, dict) and 'T' in witness and 'lambda' in witness:
            T = witness['T']
            lambda_val = witness['lambda']
        elif hasattr(witness, 'shape') and len(witness.shape) == 2:
            T = witness
            eigenvals = T.eigenvals()
            if not eigenvals:
                return [False, False, False, False]
            
            found = False
            for l, m_a_alg in eigenvals.items():
                M = T - l * eye(T.shape[0])
                m_g_alg = T.shape[1] - M.rank()
                if m_g_alg > m_a_alg:
                    lambda_val = l
                    found = True
                    break
            if not found:
                lambda_val = list(eigenvals.keys())[0]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: lambda_val is an eigenvalue of T
    try:
        I = eye(T.shape[0])
        M = T - lambda_val * I
        det_val = M.det()
        h1 = bool(det_val == 0 or simplify(det_val) == 0)
    except Exception:
        h1 = False

    # H2: m_a is defined as the algebraic multiplicity
    try:
        x = Symbol('x')
        cp_expr = T.charpoly(x).as_expr()
        m_a = 0
        for k in range(1, T.shape[0] + 2):
            divisor = (x - lambda_val)**k
            q, r = div(cp_expr, divisor, x)
            if r == 0 or simplify(r) == 0:
                m_a = k
            else:
                break
        h2 = True
    except Exception:
        h2 = False
        m_a = None

    # H3: m_g is defined as the geometric multiplicity
    try:
        m_g = T.shape[1] - M.rank()
        h3 = True
    except Exception:
        h3 = False
        m_g = None

    # neg_Q: m_g > m_a (Conclusion m_g <= m_a FAILS)
    try:
        if h2 and h3 and m_a is not None and m_g is not None:
            neg_q = bool(m_g > m_a)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: lambda is an eigenvalue of T",
    "H_2: m_a(lambda) is defined as the algebraic multiplicity",
    "H_3: m_g(lambda) is defined as the geometric multiplicity",
    "¬Q: m_g(lambda) > m_a(lambda)"
]

N_HYP = 3
NEG_Q_INDEX = 3