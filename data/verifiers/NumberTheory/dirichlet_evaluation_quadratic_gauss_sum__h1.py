import sympy
import math

# Top-level setup
# No special named objects needed for this number theory conjecture.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for any integer p, the Gauss sum 
    sum_{x=0}^{p-1} exp(2*pi*i*x^2 / p) equals sqrt(p) if p = 1 mod 4, 
    and equals i*sqrt(p) if p = 3 mod 4.
    """
    try:
        p = int(witness)
    except Exception:
        return [False]
    
    try:
        # The sum is undefined or division by zero if p == 0
        if p == 0:
            return [False]
            
        # Evaluate the Gauss sum exactly/numerically
        # For p < 0, Python's range(p) is empty, making the sum 0,
        # which mathematically serves as a counterexample since the expected value is non-zero.
        if p > 0:
            # Compute the sum numerically to avoid sympy simplification issues with large sums
            total = sum(sympy.exp(2 * sympy.pi * sympy.I * (x**2) / p) for x in range(p))
            total_c = complex(total.evalf())
        else:
            total_c = complex(0)
            
        # Check the conclusion based on p mod 4
        if p % 4 == 1:
            expected = sympy.sqrt(p)
            expected_c = complex(expected.evalf())
            # Conclusion fails if the sum does not equal sqrt(p)
            neg_q = bool(abs(total_c - expected_c) > 1e-7)
            
        elif p % 4 == 3:
            expected = sympy.I * sympy.sqrt(p)
            expected_c = complex(expected.evalf())
            # Conclusion fails if the sum does not equal i*sqrt(p)
            neg_q = bool(abs(total_c - expected_c) > 1e-7)
            
        else:
            # If p = 0 or 2 mod 4, the conditional statement 
            # "equals A if p=1 mod 4, and B if p=3 mod 4" is vacuously true.
            # Therefore, the conclusion holds, and neg_Q is False.
            neg_q = False
            
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The Gauss sum does not equal sqrt(p) for p ≡ 1 (mod 4) or i*sqrt(p) for p ≡ 3 (mod 4)"
]

N_HYP = 0
NEG_Q_INDEX = 0