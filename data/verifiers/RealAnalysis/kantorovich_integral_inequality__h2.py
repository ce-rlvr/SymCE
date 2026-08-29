import sympy as sp
import math

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false Kantorovich Inequality conjecture.
    The witness is expected to be a tuple: (probs, values, m, M)
    where `probs` is a list of probabilities, `values` is a list of values (scalars or matrices),
    and `m`, `M` are the bounds.
    """
    try:
        if len(witness) != 4:
            return [False, False, False]
            
        probs, values, m, M = witness
        
        # H_1: (X, Sigma, mu) is a probability space
        # The probabilities must sum to 1 and be non-negative.
        sum_probs = sum(probs)
        h1 = abs(float(sum_probs) - 1.0) < 1e-7 and all(float(p) >= -1e-7 for p in probs)
        
        # H_2: There exist constants 0 < m <= M such that m <= f(x) <= M for almost all x in X
        h2 = (0 < float(m) <= float(M))
        
        is_matrix = False
        try:
            mat = sp.Matrix(values[0])
            if mat.shape[0] == mat.shape[1] and mat.shape[0] > 1:
                is_matrix = True
        except Exception:
            pass
            
        for p, v in zip(probs, values):
            if float(p) > 1e-7:
                if is_matrix:
                    v_sp = sp.Matrix(v)
                    # For matrices, m <= f(x) <= M means m*I <= f(x) <= M*I in the Loewner order
                    if not v_sp.is_hermitian:
                        h2 = False
                        break
                    evals = v_sp.eigenvals().keys()
                    for ev in evals:
                        if not (float(m) - 1e-7 <= float(sp.re(ev)) <= float(M) + 1e-7 and abs(float(sp.im(ev))) < 1e-7):
                            h2 = False
                            break
                else:
                    if not (float(m) - 1e-7 <= float(v) <= float(M) + 1e-7):
                        h2 = False
                        break
                        
        # Conclusion: (\int f d\mu) (\int 1/f d\mu) <= (m+M)^2 / (4mM)
        if is_matrix:
            n = sp.Matrix(values[0]).shape[0]
            A = sp.zeros(n)
            B = sp.zeros(n)
            for p, v in zip(probs, values):
                v_sp = sp.Matrix(v)
                A += float(p) * v_sp
                B += float(p) * v_sp.inv()
            prod = A * B
            bound = (float(m) + float(M))**2 / (4 * float(m) * float(M))
            diff = bound * sp.eye(n) - prod
            
            # Check if diff is Hermitian (required for Loewner order inequality)
            is_herm = True
            for i in range(n):
                for j in range(n):
                    if abs(complex(diff[i, j]) - complex(diff[j, i]).conjugate()) > 1e-7:
                        is_herm = False
                        break
                if not is_herm:
                    break
                    
            if not is_herm:
                Q = False
            else:
                evals = diff.eigenvals().keys()
                Q = all(float(sp.re(ev)) >= -1e-7 for ev in evals)
        else:
            A = sum(float(p) * float(v) for p, v in zip(probs, values))
            B = sum(float(p) / float(v) for p, v in zip(probs, values))
            bound = (float(m) + float(M))**2 / (4 * float(m) * float(M))
            Q = float(A * B) <= bound + 1e-7
            
        return [bool(h1), bool(h2), not bool(Q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: (X, Sigma, mu) is a probability space",
    "H_2: There exist constants 0 < m <= M such that m <= f(x) <= M for almost all x in X",
    "not Q: The Kantorovich inequality fails at the witness"
]

N_HYP = 2
NEG_Q_INDEX = 2