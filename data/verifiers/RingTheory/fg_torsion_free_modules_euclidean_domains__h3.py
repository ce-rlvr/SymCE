import sympy
from sympy import ZZ, QQ, eye, zeros, Matrix
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "A finitely generated module over a Euclidean domain is free."
    
    The witness is expected to represent a finitely generated module M over a ring R.
    It can be provided as:
      - A list of invariant factors (assumes R = ZZ).
      - A tuple (R, inv_factors) where R is a SymPy domain and inv_factors is a list.
      - A sympy.Matrix representing a presentation matrix over ZZ.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, inv_factors = witness
        elif isinstance(witness, list):
            R = ZZ
            inv_factors = witness
        elif isinstance(witness, Matrix):
            R = ZZ
            snf = witness.smith_normal_form()
            inv_factors = [snf[i, i] for i in range(min(snf.rows, snf.cols))]
        else:
            R = None
            inv_factors = None
    except Exception:
        R = None
        inv_factors = None

    # H_1: R is a Euclidean domain
    h1_ok = False
    try:
        if R is not None:
            if R == ZZ:
                h1_ok = True
            elif hasattr(R, 'is_Field') and R.is_Field:
                h1_ok = True
            elif hasattr(R, 'is_PID') and R.is_PID:
                # In SymPy, common PIDs like QQ[x] are Euclidean domains.
                h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: M is a finitely generated module over R
    h2_ok = False
    try:
        if R is not None and isinstance(inv_factors, list):
            all_in_R = True
            for d in inv_factors:
                try:
                    R.convert(d)
                except Exception:
                    all_in_R = False
                    break
            if all_in_R:
                h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: M is not a free module
    # M is free iff all its invariant factors are either 0 or units in R.
    neg_q_ok = False
    try:
        if h1_ok and h2_ok:
            for d in inv_factors:
                d_R = R.convert(d)
                if d_R != R.zero:
                    is_u = False
                    if hasattr(R, 'is_unit'):
                        is_u = R.is_unit(d_R)
                    else:
                        # Fallback unit check
                        if R == ZZ:
                            is_u = (d_R == 1 or d_R == -1)
                        elif getattr(R, 'is_Field', False):
                            is_u = True
                    
                    if not is_u:
                        neg_q_ok = True
                        break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: M is a finitely generated module over R",
    "¬Q: M is not a free module"
]

N_HYP = 2
NEG_Q_INDEX = 2