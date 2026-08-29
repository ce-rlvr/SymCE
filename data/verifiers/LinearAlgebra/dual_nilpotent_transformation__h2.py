import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness can be a sympy Matrix, a tuple (T, k), or a dict {'T': T, 'k': k}.
    """
    try:
        # Extract T and k from the witness
        if isinstance(witness, tuple) and len(witness) == 2:
            T, k = witness
        elif isinstance(witness, dict) and 'T' in witness and 'k' in witness:
            T = witness['T']
            k = witness['k']
        else:
            T = witness
            if hasattr(T, 'k'):
                k = T.k
            elif hasattr(T, 'shape'):
                k = T.shape[0]
            else:
                return [False, False, False]
                
        # H_1: V is a vector space over a field F
        # We verify that T represents a linear operator (e.g., a square matrix or an object with required methods)
        is_sq = getattr(T, 'is_square', False)
        if callable(is_sq):
            is_sq = is_sq()
        h1 = bool(is_sq) or (hasattr(T, '__pow__') and (hasattr(T, 'dual') or hasattr(T, 'T')))
             
        # H_2: T: V -> V is a linear operator such that T^k = 0
        h2 = False
        if h1:
            try:
                Tk = T**k
                if hasattr(Tk, 'expand'):
                    Tk = Tk.expand()
                
                if hasattr(Tk, 'is_zero_matrix') and Tk.is_zero_matrix is not None:
                    h2 = bool(Tk.is_zero_matrix)
                elif hasattr(Tk, 'rows') and hasattr(Tk, 'cols'):
                    h2 = True
                    for i in range(Tk.rows):
                        for j in range(Tk.cols):
                            val = Tk[i, j]
                            if hasattr(val, 'is_zero') and val.is_zero is True:
                                continue
                            if val == 0:
                                continue
                            h2 = False
                            break
                        if not h2:
                            break
                elif hasattr(Tk, 'is_zero') and callable(Tk.is_zero):
                    h2 = bool(Tk.is_zero())
                elif hasattr(Tk, 'is_zero') and Tk.is_zero is not None:
                    h2 = bool(Tk.is_zero)
                else:
                    h2 = (Tk == 0)
            except Exception:
                h2 = False
                
        # ¬Q: The dual transformation T* is not nilpotent or (T*)^k != 0
        neg_q = False
        if h1:
            try:
                if hasattr(T, 'dual'):
                    T_star = T.dual() if callable(T.dual) else T.dual
                else:
                    T_star = T.T
                    
                T_star_k = T_star**k
                if hasattr(T_star_k, 'expand'):
                    T_star_k = T_star_k.expand()
                    
                is_zero = True
                if hasattr(T_star_k, 'is_zero_matrix') and T_star_k.is_zero_matrix is not None:
                    is_zero = bool(T_star_k.is_zero_matrix)
                elif hasattr(T_star_k, 'rows') and hasattr(T_star_k, 'cols'):
                    for i in range(T_star_k.rows):
                        for j in range(T_star_k.cols):
                            val = T_star_k[i, j]
                            if hasattr(val, 'is_zero') and val.is_zero is True:
                                continue
                            if val == 0:
                                continue
                            is_zero = False
                            break
                        if not is_zero:
                            break
                elif hasattr(T_star_k, 'is_zero') and callable(T_star_k.is_zero):
                    is_zero = bool(T_star_k.is_zero())
                elif hasattr(T_star_k, 'is_zero') and T_star_k.is_zero is not None:
                    is_zero = bool(T_star_k.is_zero)
                else:
                    is_zero = (T_star_k == 0)
                    
                neg_q = not is_zero
            except Exception:
                neg_q = False
                
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: T: V -> V is a linear operator such that T^k = 0",
    "¬Q: The dual transformation T* is not nilpotent or (T*)^k != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2