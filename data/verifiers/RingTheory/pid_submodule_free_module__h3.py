import sympy
from sympy import ZZ, QQ, Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    Hypotheses:
      H_1: R is a principal ideal domain
      H_2: F is a free R-module of finite rank n
    Conclusion:
      Q: M is a free R-module of rank less than or equal to n
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            n_val = witness.get('n')
            if n_val is not None:
                n = int(n_val)
            else:
                n = None
            inv_factors = witness.get('inv_factors', [])
            r = int(witness.get('r', witness.get('M_rank', 0)))
        elif isinstance(witness, (list, tuple)):
            if len(witness) < 3:
                return [False, False, False]
            
            R = witness[0]
            
            def is_int_like(val):
                return isinstance(val, int) or getattr(val, 'is_integer', False)
                
            if is_int_like(witness[1]):
                n = int(witness[1])
                m_obj = witness[2]
                if len(witness) == 4 and isinstance(witness[2], list) and is_int_like(witness[3]):
                    inv_factors = witness[2]
                    r = int(witness[3])
                    m_obj = None
            elif len(witness) >= 4 and is_int_like(witness[3]):
                n = int(witness[3])
                m_obj = witness[2]
            else:
                return [False, False, False]
                
            if m_obj is not None:
                if is_int_like(m_obj):
                    inv_factors = []
                    r = int(m_obj)
                elif isinstance(m_obj, list):
                    inv_factors = m_obj
                    r = 0
                elif hasattr(m_obj, 'smith_normal_form'):
                    S = m_obj.smith_normal_form()
                    m_rows, k_cols = m_obj.shape
                    inv_factors = [S[i, i] for i in range(min(m_rows, k_cols))]
                    r = m_rows - min(m_rows, k_cols)
                else:
                    return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a principal ideal domain
    try:
        h1 = bool(R.is_PID)
    except Exception:
        h1 = False

    # H_2: F is a free R-module of finite rank n
    try:
        h2 = isinstance(n, int) and n >= 0
    except Exception:
        h2 = False

    # ¬Q: M is not a free R-module of rank less than or equal to n
    try:
        is_free = True
        actual_rank = r
        for d in inv_factors:
            d_R = R.convert(d)
            if d_R == R.zero:
                actual_rank += 1
            else:
                try:
                    R.exquo(R.one, d_R)
                except Exception:
                    is_free = False
        
        q_holds = is_free and (actual_rank <= n)
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: F is a free R-module of finite rank n",
    "¬Q: M is not a free R-module of rank less than or equal to n"
]

N_HYP = 2
NEG_Q_INDEX = 2