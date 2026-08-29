import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is an n x n matrix with entries in R
    try:
        h1_ok = False
        if isinstance(witness, sympy.MatrixBase) and witness.is_square and witness.rows >= 1:
            h1_ok = True
            for i in range(witness.rows):
                for j in range(witness.cols):
                    val = witness[i, j]
                    if val.is_real is False:
                        h1_ok = False
                        break
                    try:
                        c = complex(val)
                        if abs(c.imag) > 1e-9:
                            h1_ok = False
                            break
                    except Exception:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # neg_Q: Conclusion fails
    neg_q_ok = False
    try:
        if h1_ok:
            q_ok = False
            evs = witness.eigenvects()
            
            real_pos = []
            for val, mult, vecs in evs:
                is_rp = False
                if val.is_real and val.is_positive:
                    is_rp = True
                else:
                    try:
                        c = complex(val)
                        if abs(c.imag) < 1e-9 and c.real > 1e-9:
                            is_rp = True
                    except Exception:
                        pass
                if is_rp:
                    real_pos.append((val, mult, vecs))
                    
            if real_pos:
                def get_real_val(x):
                    try:
                        return float(x[0])
                    except Exception:
                        return complex(x[0]).real
                        
                rho_tuple = max(real_pos, key=get_real_val)
                rho = rho_tuple[0]
                rho_f = get_real_val(rho_tuple)
                
                other_less = True
                for val, mult, vecs in evs:
                    if val != rho:
                        less = False
                        try:
                            rel = sympy.Abs(val) < rho
                            if rel == True or rel is sympy.true:
                                less = True
                        except Exception:
                            pass
                        if not less:
                            try:
                                c_val = complex(val)
                                if abs(c_val) < rho_f - 1e-9:
                                    less = True
                            except Exception:
                                pass
                        if not less:
                            other_less = False
                            break
                            
                if other_less:
                    vecs = rho_tuple[2]
                    if len(vecs) == 1:
                        v = vecs[0]
                        all_pos = True
                        all_neg = True
                        for entry in v:
                            is_pos = False
                            is_neg = False
                            if entry.is_real and entry.is_positive:
                                is_pos = True
                            elif entry.is_real and entry.is_negative:
                                is_neg = True
                            elif entry.is_zero:
                                pass
                            else:
                                try:
                                    c = complex(entry)
                                    if abs(c.imag) < 1e-9:
                                        if c.real > 1e-9:
                                            is_pos = True
                                        elif c.real < -1e-9:
                                            is_neg = True
                                except Exception:
                                    pass
                                    
                            if not is_pos:
                                all_pos = False
                            if not is_neg:
                                all_neg = False
                                
                        if all_pos or all_neg:
                            q_ok = True
            neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with entries in R",
    "¬Q: A does not have a unique largest real eigenvalue rho > 0 strictly dominating others, with a 1D eigenspace spanned by a strictly positive eigenvector"
]

N_HYP = 1
NEG_Q_INDEX = 1