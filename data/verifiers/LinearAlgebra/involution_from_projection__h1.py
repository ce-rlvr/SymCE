import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: P is a linear operator on V",
    "H_2: I denotes the identity operator on V",
    "¬Q: P is a projection iff I - 2P is an involution is FALSE"
]

def is_square_matrix(M):
    if hasattr(M, 'is_square'):
        return M.is_square
    if hasattr(M, 'shape') and len(M.shape) == 2 and M.shape[0] == M.shape[1]:
        return True
    return False

def conditions(witness):
    try:
        # Check if witness is provided as a tuple (Matrix, modulus) to represent a field of characteristic 2
        if isinstance(witness, tuple) and len(witness) == 2 and is_square_matrix(witness[0]):
            P, n = witness
            if not is_square_matrix(P):
                return [False, False, False]
            
            H1 = True
            H2 = True
            
            I = eye(P.shape[0])
            
            # Evaluate P^2 == P modulo n
            P_sq = (P**2).applyfunc(lambda x: x % n)
            P_mod = P.applyfunc(lambda x: x % n)
            is_proj = (P_sq == P_mod)
            
            # Evaluate (I - 2P)^2 == I modulo n
            I_minus_2P = I - 2*P
            inv_sq = (I_minus_2P**2).applyfunc(lambda x: x % n)
            I_mod = I.applyfunc(lambda x: x % n)
            is_inv = (inv_sq == I_mod)
            
            neg_Q = bool(is_proj != is_inv)
            return [H1, H2, neg_Q]
            
        else:
            # Witness is provided directly as a matrix (e.g., over GF(2) or a custom class)
            P = witness
            if not is_square_matrix(P):
                return [False, False, False]
            
            H1 = True
            H2 = True
            
            try:
                I = P**0
            except Exception:
                I = eye(P.shape[0])
                
            is_proj = bool(P**2 == P)
            is_inv = bool((I - 2*P)**2 == I)
            
            neg_Q = bool(is_proj != is_inv)
            return [H1, H2, neg_Q]
            
    except Exception:
        return [False, False, False]