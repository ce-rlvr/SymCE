import sympy as sp
from sympy import eye, zeros

# Top-level setup for standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Verifies that the witness is a valid counterexample to the conjecture.
    The conjecture fails for modules over a ring where the dual module does not separate points.
    A standard counterexample uses Z-modules (abelian groups) where W is a torsion module (e.g., Z_n).
    In this case, W^* = Hom(Z_n, Z) = {0}, so S^* = T^* = 0 for all S, T, but S and T need not be equal.
    
    Expected witness format:
      A tuple (S, T, n) or a dict {'S': S, 'T': T, 'n': n}
      where S and T represent Z-linear maps to Z_n (as integers, matrices, or functions).
    """
    h1, h2, neg_q = False, False, False
    
    def check_Z_module(S, T, n):
        nonlocal h1, h2, neg_q
        try:
            n = int(n)
        except Exception:
            return False
            
        if n < 2:
            return False
        
        # Case 1: S and T are integers (representing maps x -> S*x mod n)
        if isinstance(S, int) and isinstance(T, int):
            h1 = True
            h2 = True
            neg_q = (S % n) != (T % n)
            return True
            
        # Case 2: S and T are callable functions
        if callable(S) and callable(T):
            is_linear = True
            # Check Z-linearity: f(x+y) == f(x) + f(y) mod n
            for x in range(1, 4):
                for y in range(1, 4):
                    try:
                        if (int(S(x+y)) - (int(S(x)) + int(S(y)))) % n != 0:
                            is_linear = False
                        if (int(T(x+y)) - (int(T(x)) + int(T(y)))) % n != 0:
                            is_linear = False
                    except Exception:
                        is_linear = False
            if is_linear:
                h1 = True
                h2 = True
                neg_q = False
                for x in range(1, 5):
                    try:
                        if (int(S(x)) - int(T(x))) % n != 0:
                            neg_q = True
                            break
                    except Exception:
                        pass
                return True

        # Case 3: S and T are matrices or lists of lists
        try:
            S_mat = sp.Matrix(S) if not isinstance(S, sp.Matrix) else S
            T_mat = sp.Matrix(T) if not isinstance(T, sp.Matrix) else T
            
            if S_mat.shape == T_mat.shape:
                is_integer_matrix = True
                for i in range(S_mat.shape[0]):
                    for j in range(S_mat.shape[1]):
                        val_S = S_mat[i, j]
                        val_T = T_mat[i, j]
                        if not (isinstance(val_S, int) or getattr(val_S, 'is_integer', False) is True):
                            is_integer_matrix = False
                        if not (isinstance(val_T, int) or getattr(val_T, 'is_integer', False) is True):
                            is_integer_matrix = False
                
                if is_integer_matrix:
                    h1 = True
                    h2 = True
                    neg_q = False
                    for i in range(S_mat.shape[0]):
                        for j in range(S_mat.shape[1]):
                            diff = S_mat[i, j] - T_mat[i, j]
                            if (diff % n) != 0:
                                neg_q = True
                                break
                        if neg_q:
                            break
                    return True
        except Exception:
            pass
            
        return False

    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            check_Z_module(witness[0], witness[1], witness[2])
    except Exception:
        pass

    if not (h1 and h2 and neg_q):
        try:
            if isinstance(witness, dict) and 'S' in witness and 'T' in witness and 'n' in witness:
                check_Z_module(witness['S'], witness['T'], witness['n'])
        except Exception:
            pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S and T are linear transformations",
    "H_2: The dual transformations S^* and T^* are equal",
    "¬Q: S and T are not equal"
]

N_HYP = 2
NEG_Q_INDEX = 2