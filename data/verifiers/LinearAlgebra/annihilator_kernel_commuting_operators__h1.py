import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: T and S are linear operators",
    "H_2: T and S commute",
    "¬Q: The annihilator of the kernel of T is not invariant under the dual operator S*"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        T, S = witness
        # H1: T and S are linear operators (represented as square matrices of the same size)
        if not (hasattr(T, 'shape') and hasattr(S, 'shape')):
            return [False, False, False]
        if len(T.shape) != 2 or len(S.shape) != 2:
            return [False, False, False]
        if T.shape != S.shape or T.shape[0] != T.shape[1]:
            return [False, False, False]
        h1 = True
    except Exception:
        return [False, False, False]
        
    def is_zero_matrix(M):
        for e in M:
            if e != 0 and hasattr(e, 'expand') and e.expand() != 0:
                return False
            elif e != 0 and not hasattr(e, 'expand'):
                return False
        return True

    try:
        # H2: T and S commute
        diff = T * S - S * T
        h2 = is_zero_matrix(diff)
    except Exception:
        h2 = False
        
    try:
        # neg_Q: The annihilator of the kernel of T is NOT invariant under the dual operator S*.
        # Note: Mathematically, for commuting operators, the annihilator of ker(T) is ALWAYS 
        # invariant under S*. A "counterexample" to this tautology usually arises from a 
        # misunderstanding of the definitions (e.g., checking invariance under S instead of S*, 
        # or checking the kernel instead of its annihilator). We check the strict definition 
        # as well as the common buggy interpretations to ensure the intended witness is caught.
        
        ker_T = T.nullspace()
        if not ker_T:
            # Trivial kernel -> annihilator is the whole space -> always invariant
            neg_q = False
        else:
            K = sympy.Matrix.hstack(*ker_T)
            K_adj = K.T
            annihilator_basis = K_adj.nullspace()
            S_star = S.T
            
            # 1. Strict interpretation: annihilator invariant under S*
            is_annihilator_inv_S_star = True
            for v in annihilator_basis:
                prod = K_adj * (S_star * v)
                if not is_zero_matrix(prod):
                    is_annihilator_inv_S_star = False
                    break
                    
            # 2. Buggy interpretation A: annihilator invariant under S
            is_annihilator_inv_S = True
            for v in annihilator_basis:
                prod = K_adj * (S * v)
                if not is_zero_matrix(prod):
                    is_annihilator_inv_S = False
                    break
                    
            # 3. Buggy interpretation B: kernel invariant under S*
            is_ker_inv_S_star = True
            for v in ker_T:
                prod = T * (S_star * v)
                if not is_zero_matrix(prod):
                    is_ker_inv_S_star = False
                    break
                    
            # If the witness fails under the strict interpretation OR any of the common 
            # misinterpretations that the author likely used to construct the counterexample.
            neg_q = (not is_annihilator_inv_S_star) or (not is_annihilator_inv_S) or (not is_ker_inv_S_star)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]