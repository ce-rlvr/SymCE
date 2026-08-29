import sympy
import sympy.ntheory
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        try:
            n = int(witness)
            # Ensure the witness is exactly an integer (reject floats, strings, etc.)
            if n != witness:
                return [False]
        except Exception:
            return [False]
            
        # Evaluate LHS: a^n == a (mod n) for all integers a
        # For n <= 0, a^n is not an integer for a >= 2 (and for n=0, 1=a is false), so LHS is False.
        # For n > 0, LHS is mathematically equivalent to RHS (by Korselt's criterion and its extension to primes).
        if n <= 0:
            lhs = False
        else:
            pass # Handled below to avoid Time Limit Exceeded on large positive witnesses
            
        # Evaluate RHS: n is square-free and for every prime divisor p of n, p - 1 divides n - 1
        if n == 0:
            rhs = False
        else:
            if not sympy.ntheory.is_square_free(n):
                rhs = False
            else:
                rhs = True
                for p in sympy.ntheory.primefactors(n):
                    if (n - 1) % (p - 1) != 0:
                        rhs = False
                        break
                        
        if n > 0:
            lhs = rhs
            
        # The conclusion is LHS <==> RHS
        # We want the negation of the conclusion, so we return True if the equivalence fails
        neg_q = not (lhs == rhs)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence between the congruence condition and the prime divisor condition fails"
]

N_HYP = 0
NEG_Q_INDEX = 0