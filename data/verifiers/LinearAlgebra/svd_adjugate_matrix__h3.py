import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is an n x n complex matrix with n >= 2
    try:
        h1 = False
        if isinstance(witness, sympy.MatrixBase):
            if witness.shape[0] == witness.shape[1] and witness.shape[0] >= 2:
                h1 = True
                for val in witness:
                    if not isinstance(val, sympy.Expr):
                        h1 = False
                        break
                    if val.is_finite is False:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: A is invertible
    try:
        h2 = False
        if h1:
            det_A = witness.det()
            if sympy.simplify(det_A) != 0:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The singular values of adj(A) are NOT exactly the n products prod_{j!=i} sigma_j for i=1..n
    # Note: The conjecture implies a sequence equality (i-th singular value equals i-th product).
    # Since singular values are sorted descending and the products are ascending, 
    # they can only match if all singular values are equal (i.e., A^H A is a multiple of I).
    try:
        neg_q = False
        if h1:
            A = witness
            n = A.shape[0]
            evaluated = False
            
            if not A.free_symbols:
                try:
                    # Numerical evaluation for concrete matrices
                    lam = sympy.symbols('lam')
                    A_num = A.evalf()
                    
                    Gram_A = A_num.H * A_num
                    P_A = Gram_A.charpoly(lam)
                    roots_A = P_A.nroots()
                    
                    sigmas_A = []
                    for r in roots_A:
                        val = float(sympy.re(r))
                        if val < 0: val = 0.0
                        sigmas_A.append(val**0.5)
                    sigmas_A.sort(reverse=True)
                    
                    adjA = A.adjugate().evalf()
                    Gram_adjA = adjA.H * adjA
                    P_adjA = Gram_adjA.charpoly(lam)
                    roots_adjA = P_adjA.nroots()
                    
                    sigmas_adjA = []
                    for r in roots_adjA:
                        val = float(sympy.re(r))
                        if val < 0: val = 0.0
                        sigmas_adjA.append(val**0.5)
                    sigmas_adjA.sort(reverse=True)
                    
                    q_holds = True
                    for i in range(n):
                        prod = 1.0
                        for j in range(n):
                            if j != i:
                                prod *= sigmas_A[j]
                        
                        if abs(sigmas_adjA[i] - prod) > 1e-5:
                            q_holds = False
                            break
                    neg_q = not q_holds
                    evaluated = True
                except Exception:
                    evaluated = False
            
            if not evaluated:
                # Symbolic evaluation fallback
                Gram = A.H * A
                is_multiple_of_I = True
                for i in range(n):
                    for j in range(n):
                        if i != j:
                            if sympy.simplify(Gram[i, j]) != 0:
                                is_multiple_of_I = False
                                break
                    if not is_multiple_of_I:
                        break
                if is_multiple_of_I:
                    diag_val = Gram[0, 0]
                    for i in range(1, n):
                        if sympy.simplify(Gram[i, i] - diag_val) != 0:
                            is_multiple_of_I = False
                            break
                
                if is_multiple_of_I:
                    q_holds = True
                else:
                    det_A = A.det()
                    if sympy.simplify(det_A) == 0:
                        adjA = A.adjugate()
                        if adjA.is_zero_matrix:
                            q_holds = True
                        else:
                            q_holds = False
                    else:
                        q_holds = False
                
                neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix with n >= 2",
    "H_2: A is invertible",
    "¬Q: The singular values of adj(A) are not exactly the n products prod_{j!=i} sigma_j for i=1..n"
]

N_HYP = 2
NEG_Q_INDEX = 2