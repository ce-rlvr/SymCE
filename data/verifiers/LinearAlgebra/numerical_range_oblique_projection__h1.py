import sympy as sp
import math

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    # H_1: P is a square matrix (so that spectral norm and numerical range are well-defined)
    try:
        h1_ok = isinstance(witness, sp.MatrixBase) and witness.rows == witness.cols and not witness.free_symbols
    except Exception:
        h1_ok = False

    # neg_Q: The numerical range of P is NOT a closed elliptical disk with foci at 0 and 1 
    # and minor axis length equal to \sqrt{\|P\|_2^2 - 1}.
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            P_num = witness.evalf()
            
            # Compute ||P||_2^2
            PtP = P_num.H * P_num
            roots_PtP = PtP.charpoly().nroots()
            max_eval_PtP = max([float(sp.re(r)) for r in roots_PtP])
            
            # If ||P||_2 < 1, the minor axis length would be imaginary, so it cannot be the specified ellipse.
            if max_eval_PtP < 1 - 1e-7:
                neg_q_ok = True
            else:
                norm_P_sq = max_eval_PtP
                N_angles = 32
                is_ellipse = True
                
                # Check the support function of the numerical range against the target ellipse
                for k in range(N_angles):
                    theta = 2 * math.pi * k / N_angles
                    exp_neg_i_theta = complex(math.cos(theta), -math.sin(theta))
                    exp_i_theta = complex(math.cos(theta), math.sin(theta))
                    
                    # H(theta) = (e^{-i\theta} P + e^{i\theta} P^*) / 2
                    H_theta = (exp_neg_i_theta * P_num + exp_i_theta * P_num.H) / 2
                    roots_H = H_theta.charpoly().nroots()
                    max_eval_H = max([float(sp.re(r)) for r in roots_H])
                    
                    # Target support function for an ellipse with foci 0, 1 and minor axis \sqrt{||P||_2^2 - 1}
                    val_inside_sqrt = norm_P_sq - 1 + math.cos(theta)**2
                    if val_inside_sqrt < 0:
                        if val_inside_sqrt > -1e-5:
                            val_inside_sqrt = 0.0
                        else:
                            is_ellipse = False
                            break
                            
                    target = math.cos(theta)/2 + 0.5 * math.sqrt(val_inside_sqrt)
                    
                    # If the support function differs, the numerical range is not the target ellipse
                    if abs(max_eval_H - target) > 1e-4:
                        is_ellipse = False
                        break
                
                neg_q_ok = not is_ellipse
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: P is a square matrix (spectral norm is well-defined)",
    "¬Q: The numerical range of P is not a closed elliptical disk with foci at 0 and 1 and minor axis length sqrt(||P||_2^2 - 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1