import sympy as sp

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture drops the hypothesis that eigenvalues are sorted descending,
    which makes it false under the standard ascending order convention.
    """
    try:
        A, B = witness
    except Exception:
        return [False, False]
    
    # H_1: A and B are n by n Hermitian matrices
    try:
        if not isinstance(A, sp.MatrixBase) or not isinstance(B, sp.MatrixBase):
            h1 = False
        elif A.shape[0] != A.shape[1] or B.shape[0] != B.shape[1]:
            h1 = False
        elif A.shape != B.shape:
            h1 = False
        elif A.is_hermitian != True or B.is_hermitian != True:
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails at the witness
    try:
        if not h1:
            neg_q = False
        else:
            n = A.shape[0]
            if n == 0:
                neg_q = False
            else:
                def get_sorted_eigenvalues(M):
                    evs = M.eigenvals()
                    roots = []
                    for val, mult in evs.items():
                        # Evaluate to float; Hermitian matrices have real eigenvalues
                        c = complex(val.evalf())
                        roots.extend([c.real] * mult)
                    # Sort ascending (the convention that makes the conjecture false)
                    roots.sort()
                    return roots
                
                eig_A = get_sorted_eigenvalues(A)
                eig_B = get_sorted_eigenvalues(B)
                eig_AB = get_sorted_eigenvalues(A + B)
                
                if len(eig_A) != n or len(eig_B) != n or len(eig_AB) != n:
                    neg_q = False
                else:
                    conclusion_holds = True
                    lambda_1_B = eig_B[0]   # Smallest eigenvalue
                    lambda_n_B = eig_B[-1]  # Largest eigenvalue
                    
                    for k in range(n):
                        lam_k_A = eig_A[k]
                        lam_k_AB = eig_AB[k]
                        
                        lower_bound = lam_k_A + lambda_n_B
                        upper_bound = lam_k_A + lambda_1_B
                        
                        # Check if the inequality holds (with a small float tolerance)
                        if not (lower_bound <= lam_k_AB + 1e-7 and lam_k_AB <= upper_bound + 1e-7):
                            conclusion_holds = False
                            break
                    
                    neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are n by n Hermitian matrices",
    "¬Q: The inequality lambda_k(A) + lambda_n(B) <= lambda_k(A+B) <= lambda_k(A) + lambda_1(B) fails for some k"
]

N_HYP = 1
NEG_Q_INDEX = 1