import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, sympy.MatrixBase) and witness.shape[0] == witness.shape[1]
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            is_diag = witness.is_diagonalizable()
            
            has_non_real_eval = False
            is_real = True
            for a in witness.atoms():
                if getattr(a, 'is_real', None) is False:
                    is_real = False
                    break
                    
            if is_real:
                evals = witness.eigenvals()
                for ev in evals:
                    if getattr(ev, 'is_real', None) is False:
                        has_non_real_eval = True
                        break
                    elif getattr(ev, 'is_real', None) is None:
                        try:
                            if abs(complex(ev.evalf()).imag) > 1e-9:
                                has_non_real_eval = True
                                break
                        except Exception:
                            pass
                            
            neg_q = bool((not is_diag) or has_non_real_eval)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M_n(C) is equipped with the standard Euclidean topology (witness is a square matrix)",
    "¬Q: Witness is not diagonalizable or not in the closure of R-diagonalizable matrices"
]

N_HYP = 1
NEG_Q_INDEX = 1