import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: V is a finite-dimensional vector space.
    # We interpret the witness as a linear transformation T represented by a matrix.
    # The domain of T is V = F^n, which is inherently finite-dimensional.
    try:
        H_1 = isinstance(witness, sympy.Matrix)
    except Exception:
        H_1 = False

    # neg_Q: The conclusion fails.
    # Conclusion: There exists a non-negative integer k such that V = ker(T^k) \oplus im(T^k),
    # and both ker(T^k) and im(T^k) are T-invariant subspaces.
    neg_Q = False
    try:
        if not isinstance(witness, sympy.Matrix):
            neg_Q = True
        else:
            T = witness
            n = T.shape[1]
            m = T.shape[0]
            
            conclusion_holds = False
            # We check k from 0 to n. If the conclusion holds for any such k, it is True.
            for k in range(n + 1):
                try:
                    if k == 0:
                        Tk = sympy.eye(n)
                    elif k == 1:
                        Tk = T
                    else:
                        Tk = T**k
                    
                    ker_Tk = Tk.nullspace()
                    im_Tk = Tk.columnspace()
                    
                    # For the direct sum to be V = F^n, im(T^k) must be a subspace of F^n.
                    if any(v.shape[0] != n for v in im_Tk):
                        continue
                        
                    # Check if dimensions add up to n
                    if len(ker_Tk) + len(im_Tk) != n:
                        continue
                        
                    # Check if their union spans F^n (implying direct sum since dimensions add up)
                    basis = ker_Tk + im_Tk
                    if basis:
                        M = sympy.Matrix.hstack(*basis)
                        if M.rank() != n:
                            continue
                    else:
                        if n != 0:
                            continue
                            
                    # Check T-invariance of ker(T^k)
                    ker_inv = True
                    if ker_Tk:
                        M1 = sympy.Matrix.hstack(*ker_Tk)
                        rank_M1 = len(ker_Tk)
                        for v in ker_Tk:
                            Tv = T * v
                            if Tv.shape[0] != n:
                                ker_inv = False
                                break
                            M2 = sympy.Matrix.hstack(M1, Tv)
                            if M2.rank() > rank_M1:
                                ker_inv = False
                                break
                    if not ker_inv:
                        continue
                        
                    # Check T-invariance of im(T^k)
                    im_inv = True
                    if im_Tk:
                        M1 = sympy.Matrix.hstack(*im_Tk)
                        rank_M1 = len(im_Tk)
                        for v in im_Tk:
                            Tv = T * v
                            if Tv.shape[0] != n:
                                im_inv = False
                                break
                            M2 = sympy.Matrix.hstack(M1, Tv)
                            if M2.rank() > rank_M1:
                                im_inv = False
                                break
                    if not im_inv:
                        continue
                        
                    conclusion_holds = True
                    break
                except Exception:
                    continue
                    
            neg_Q = not conclusion_holds
    except Exception:
        neg_Q = True

    return [H_1, neg_Q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "¬Q: There is no non-negative integer k such that V = ker(T^k) ⊕ im(T^k) and both are T-invariant"
]

N_HYP = 1
NEG_Q_INDEX = 1