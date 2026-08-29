import itertools
import math

# Top-level setup
# No specific named objects required for this real analysis theorem.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be either a tuple (p, c) where p is a real number and c is a list of complex numbers,
    or just a list of complex numbers c (in which case p defaults to -1).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (int, float)) and isinstance(witness[1], list):
            p, c = witness
        else:
            p = -1
            c = witness
    except Exception:
        return [False, False, False]
        
    # H_1: {r_n} is a finite sequence of Rademacher functions
    # This is a definitional hypothesis, inherently satisfied by the structure of the problem.
    h1 = True
    
    # H_2: {c_n} is a finite sequence of complex numbers
    try:
        h2 = isinstance(c, list) and len(c) > 0 and all(isinstance(x, (int, float, complex)) for x in c)
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion fails
    neg_q = False
    try:
        if h2:
            N = len(c)
            if N > 20:
                # Prevent timeout for excessively large sequences
                neg_q = False
            else:
                S = sum(abs(x)**2 for x in c)
                is_inf = False
                integral = 0.0
                
                # Calculate the exact integral using the independence of Rademacher functions
                for signs in itertools.product([-1, 1], repeat=N):
                    val = sum(c[i] * signs[i] for i in range(N))
                    if val == 0:
                        if p < 0:
                            is_inf = True
                            break
                        # If p == 0, |0|^0 contributes 0 to the Lebesgue integral
                    else:
                        try:
                            term = abs(val)**p
                        except OverflowError:
                            is_inf = True
                            break
                        integral += term
                        
                if is_inf or math.isinf(integral):
                    neg_q = True
                else:
                    integral /= (2**N)
                    
                    try:
                        if S == 0 and p < 0:
                            Sp = float('inf')
                        else:
                            Sp = S**(p/2.0)
                    except OverflowError:
                        Sp = float('inf')
                    except Exception:
                        Sp = float('nan')
                        
                    # Check if the inequality A_p * Sp <= integral <= B_p * Sp can hold for any A_p, B_p > 0
                    if math.isinf(Sp) and integral < float('inf'):
                        # Requires A_p * inf <= finite, which is impossible for A_p > 0
                        neg_q = True
                    elif Sp == 0 and integral > 0:
                        # Requires finite <= B_p * 0, which is impossible for integral > 0
                        neg_q = True
                    elif S > 0 and integral == 0:
                        # Requires A_p * Sp <= 0, which is impossible for A_p > 0 and Sp > 0
                        neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: {r_n} is a finite sequence of Rademacher functions",
    "H_2: {c_n} is a finite sequence of complex numbers",
    "¬Q: The Khintchine inequality fails for the given p and c_n"
]

N_HYP = 2
NEG_Q_INDEX = 2