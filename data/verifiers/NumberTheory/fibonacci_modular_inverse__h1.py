import sympy
import math

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    try:
        # H_1: F_k denotes the k-th Fibonacci number, with F_1 = 1 and F_2 = 1
        # This is a definitional hypothesis, so it holds as long as the witness is an integer index.
        h1_ok = isinstance(witness, (int, sympy.Integer))
        if not h1_ok:
            return [False, False]
            
        n = int(witness)
    except Exception:
        return [False, False]
        
    try:
        def fib(k):
            if k >= 0:
                a, b = 0, 1
                for _ in range(k):
                    a, b = b, a + b
                return a
            else:
                return ((-1)**(-k + 1)) * fib(-k)
                
        fn = fib(n)
        fn1 = fib(n+1)
        fn_minus1 = fib(n-1)
        
        # ¬Q: The modular inverse of F_n modulo F_{n+1} is NOT congruent to (-1)^n F_{n-1} mod F_{n+1}
        # In standard number theory, the modular inverse is undefined or degenerate for modulus 0, 1, or -1.
        # If the modulus is in this range, the conclusion fails (meaning neg_Q is True).
        if abs(fn1) <= 1:
            neg_q_ok = True
        else:
            try:
                inv = sympy.mod_inverse(fn, fn1)
                rhs = ((-1)**n) * fn_minus1
                # Check if they are NOT congruent modulo |F_{n+1}|
                neg_q_ok = (inv % abs(fn1)) != (rhs % abs(fn1))
            except Exception:
                # If mod_inverse raises an exception (e.g., inverse doesn't exist), the conclusion fails
                neg_q_ok = True
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer (index for Fibonacci sequence)",
    "¬Q: The modular inverse of F_n modulo F_{n+1} is not congruent to (-1)^n F_{n-1} mod F_{n+1} (or is undefined)"
]

N_HYP = 1
NEG_Q_INDEX = 1