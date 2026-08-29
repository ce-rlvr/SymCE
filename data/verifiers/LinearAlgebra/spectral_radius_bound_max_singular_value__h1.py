import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def get_max_sym(values):
    if not values:
        return None
    max_val = None
    max_float = -float('inf')
    for v in values:
        try:
            v_float = float(sp.Abs(v).evalf(50))
            if v_float > max_float:
                max_float = v_float
                max_val = sp.Abs(v)
        except Exception:
            pass
    return max_val

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    rho = None
    sigma_1 = None
    
    try:
        if isinstance(witness, sp.MatrixBase) and witness.is_square:
            evs = witness.eigenvals()
            if evs:
                rho = get_max_sym(list(evs.keys()))
                if rho is not None:
                    h1 = True
    except Exception:
        pass
        
    try:
        if isinstance(witness, sp.MatrixBase):
            svs = witness.singular_values()
            if svs:
                sigma_1 = get_max_sym(svs)
                if sigma_1 is not None:
                    h2 = True
    except Exception:
        pass
        
    try:
        if h1 and h2 and rho is not None and sigma_1 is not None:
            diff = (rho - sigma_1).evalf(50)
            diff_float = float(diff)
            # Using a small tolerance to avoid false positives from floating point inaccuracies
            neg_q = bool(diff_float > 1e-12)
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: rho(A) is defined as the spectral radius of A",
    "H_2: sigma_1(A) is defined as the maximum singular value of A",
    "¬Q: rho(A) > sigma_1(A)"
]

N_HYP = 2
NEG_Q_INDEX = 2