import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = bool(hasattr(witness, 'is_square') and witness.is_square and hasattr(witness, 'shape'))
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            h2 = True
            for x in witness:
                complex(x)
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            n = witness.shape[0]
            R = []
            for i in range(n):
                r_i = sum(abs(complex(witness[i, k])) for k in range(n) if k != i)
                R.append(r_i)
            
            eigenvalues = witness.eigenvals()
            neg_q = False
            for ev in eigenvalues:
                try:
                    ev_c = complex(ev)
                except Exception:
                    ev_c = complex(ev.evalf())
                
                in_any = False
                for i in range(n):
                    for j in range(n):
                        if i != j:
                            aii = complex(witness[i, i])
                            ajj = complex(witness[j, j])
                            if abs(ev_c - aii) * abs(ev_c - ajj) <= R[i] * R[j] + 1e-9:
                                in_any = True
                                break
                    if in_any:
                        break
                if not in_any:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "H_2: Entries of A are numeric",
    "¬Q: There exists an eigenvalue of A not in the union of K_ij for distinct i, j"
]

N_HYP = 2
NEG_Q_INDEX = 2