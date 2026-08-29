import sympy
from sympy.ntheory import factorint
from sympy.abc import x, y, z

# Top-level setup
# (No specific named objects required for this FieldTheory conjecture, 
# but we provide standard sympy symbols just in case)

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (q, k) or (F_q, k).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F_or_q, k_in = witness
            # Extract q if the witness provided a finite field object
            if hasattr(F_or_q, 'order'):
                q_in = F_or_q.order
            elif hasattr(F_or_q, 'mod'):
                q_in = F_or_q.mod
            else:
                q_in = F_or_q
        else:
            return [False, False]
            
        q = int(q_in)
        k = int(k_in)
    except Exception:
        return [False, False]
        
    # H_1: k is a non-negative integer
    try:
        h1 = isinstance(k_in, (int, sympy.Integer)) and k >= 0
    except Exception:
        h1 = False
        
    # ¬Q: The conclusion fails at the witness
    # Conclusion: The sum evaluates to -1 if k > 0 and q-1 divides k, and 0 otherwise.
    try:
        if q < 2:
            neg_q = True
        else:
            factors = factorint(q)
            if len(factors) == 1:
                # q is a prime power. F_q is a valid finite field.
                # It is a mathematically proven fact that for any finite field F_q,
                # the sum of x^k over all x in F_q ALWAYS matches the condition exactly.
                # Therefore, the conclusion holds, and neg_Q is False.
                neg_q = False
            else:
                # q is not a prime power. F_q is undefined.
                # We evaluate the sum in the ring Z/qZ as a fallback to see if it 
                # accidentally matches the condition. If it doesn't, the conclusion fails.
                expected = (q - 1) if (k > 0 and k % (q - 1) == 0) else 0
                actual = sum(pow(base, k, q) for base in range(q)) % q
                
                if actual == expected:
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is a non-negative integer",
    "¬Q: The sum does not evaluate to -1 if k > 0 and q-1 divides k, and 0 otherwise"
]

N_HYP = 1
NEG_Q_INDEX = 1