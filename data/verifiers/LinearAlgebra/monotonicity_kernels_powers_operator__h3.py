import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # The witness can be either a single operator T, or a tuple (T, k)
        if isinstance(witness, tuple) and len(witness) == 2:
            T, k = witness
            check_all_k = False
        else:
            T = witness
            check_all_k = True

        # H_1: V is a vector space over a field F
        # In our computational model, this is represented by T being a SymPy Matrix
        h1 = isinstance(T, Matrix)
        
        # H_2: T: V -> V is a linear operator
        # This means T must be a square matrix
        h2 = h1 and T.is_square
        
        if not (h1 and h2):
            return [False, False, False]
            
        neg_q = False
        
        if check_all_k:
            # If k is not specified, we check if there exists ANY k >= 1 where the conclusion fails.
            # For an n x n matrix, the sequence of kernels stabilizes by k = n.
            n = T.shape[0]
            for k_val in range(1, n + 2):
                null_k = (T**k_val).nullspace()
                Tk1 = T**(k_val + 1)
                is_subset = True
                for v in null_k:
                    prod = Tk1 * v
                    for val in prod:
                        if not (val == 0 or val.expand() == 0 or sympy.simplify(val) == 0):
                            is_subset = False
                            break
                    if not is_subset:
                        break
                if not is_subset:
                    neg_q = True
                    break
        else:
            # If k is specified in the witness, we check for that specific k.
            if not (isinstance(k, int) and k >= 1):
                return [h1, h2, False]
                
            null_k = (T**k).nullspace()
            Tk1 = T**(k + 1)
            is_subset = True
            for v in null_k:
                prod = Tk1 * v
                for val in prod:
                    if not (val == 0 or val.expand() == 0 or sympy.simplify(val) == 0):
                        is_subset = False
                        break
                if not is_subset:
                    break
            neg_q = not is_subset
            
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F (T is a Matrix)",
    "H_2: T: V -> V is a linear operator (T is square)",
    "¬Q: The kernel of T^k is NOT a subset of the kernel of T^{k+1}"
]

N_HYP = 2
NEG_Q_INDEX = 2