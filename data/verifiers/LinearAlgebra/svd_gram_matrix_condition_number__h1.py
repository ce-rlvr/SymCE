import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A has full column rank
    try:
        if not isinstance(witness, sympy.MatrixBase):
            h1 = False
        else:
            h1 = witness.rank() == witness.shape[1]
    except Exception:
        h1 = False

    # H_2: kappa_2(M) denotes the condition number of M with respect to the 2-norm
    # This is a definitional hypothesis, so it is vacuously true for any witness.
    h2 = True

    # neg_Q: kappa_2(A^T A) != (kappa_2(A))^2
    try:
        if not isinstance(witness, sympy.MatrixBase):
            neg_q = False
        else:
            def cond2_num(M):
                if min(M.shape) == 0:
                    return 1.0
                try:
                    sv = M.singular_values()
                except Exception:
                    return float('inf')
                
                if len(sv) < min(M.shape):
                    return float('inf')
                    
                sv_num = []
                for s in sv:
                    try:
                        val = float(sympy.Abs(s.evalf()))
                        sv_num.append(val)
                    except Exception:
                        return float('inf')
                        
                if not sv_num:
                    return float('inf')
                    
                if min(sv_num) < 1e-12:
                    return float('inf')
                    
                return max(sv_num) / min(sv_num)

            c_A = cond2_num(witness)
            ATA = witness.T * witness
            c_ATA = cond2_num(ATA)

            if c_A == float('inf') and c_ATA == float('inf'):
                neg_q = False
            elif c_A == float('inf') or c_ATA == float('inf'):
                neg_q = True
            else:
                expected = c_A**2
                diff = abs(c_ATA - expected)
                # Use relative error for large values to avoid floating point noise
                if expected > 1.0:
                    neg_q = (diff / expected) > 1e-5
                else:
                    neg_q = diff > 1e-5
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A has full column rank",
    "H_2: kappa_2(M) denotes the condition number of M with respect to the 2-norm",
    "¬Q: kappa_2(A^T A) != (kappa_2(A))^2"
]

N_HYP = 2
NEG_Q_INDEX = 2