import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (A, B) or a dict {'A': A, 'B': B}.
    """
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            if A is None or B is None:
                return [False, False]
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            A, B = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: Let A be an m \times n complex matrix
    try:
        h1_ok = isinstance(A, sp.MatrixBase)
    except Exception:
        h1_ok = False

    # ¬Q: \sigma_{\max}(AB) > \sigma_{\max}(A) \sigma_{\max}(B)
    try:
        def get_sigma_max(M):
            if hasattr(M, 'singular_values'):
                svs = M.singular_values()
                if not svs:
                    return sp.S.Zero
                try:
                    # Try to evaluate numerically for safe comparison
                    return max([sp.N(s) for s in svs])
                except Exception:
                    # Fallback to symbolic Max if numerical evaluation fails
                    return sp.Max(*svs)
            else:
                # If M is a scalar or other expression
                try:
                    return abs(sp.N(M))
                except Exception:
                    return abs(M)

        s_AB = get_sigma_max(A * B)
        s_A = get_sigma_max(A)
        s_B = get_sigma_max(B)

        diff = s_AB - s_A * s_B
        
        try:
            neg_q_ok = bool(diff > 0)
        except TypeError:
            # If the difference is symbolic and cannot be directly evaluated as a boolean
            diff_simp = sp.simplify(diff)
            try:
                neg_q_ok = bool(diff_simp > 0)
            except TypeError:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "¬Q: sigma_max(AB) > sigma_max(A) * sigma_max(B)"
]

N_HYP = 1
NEG_Q_INDEX = 1