import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z
import itertools
import functools

# Standard named objects for potential use in witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The witness is expected to provide a finite ring R and an ideal P.
    It can be a tuple (R, add, mul, P), a dictionary, or an object with these attributes.
    """
    try:
        if isinstance(witness, dict):
            R = witness['R']
            add = witness['add']
            mul = witness['mul']
            P = witness['P']
        elif hasattr(witness, 'R') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'P'):
            R = witness.R
            add = witness.add
            mul = witness.mul
            P = witness.P
        else:
            R, add, mul, P = witness
            
        R = list(R)
        P = list(P)
    except Exception:
        return [False, False]

    def eq(a, b):
        return a == b

    # H_1: P is a proper ideal of R
    try:
        h1 = False
        if P and len(P) < len(R):
            # Check if P is a subset of R
            if all(any(eq(p, r) for r in R) for p in P):
                # Check closure under addition
                closed_add = all(any(eq(add(p1, p2), p3) for p3 in P) for p1 in P for p2 in P)
                
                # Find the zero element of R
                zeros_R = [z for z in R if all(eq(add(a, z), a) and eq(add(z, a), a) for a in R)]
                if zeros_R:
                    zero = zeros_R[0]
                    # Check if zero is in P and P is closed under additive inverses
                    if any(eq(zero, p) for p in P):
                        has_inv = all(any(eq(add(p, q), zero) for q in P) for p in P)
                        if closed_add and has_inv:
                            # Check two-sided ideal property (absorbs multiplication from R)
                            is_ideal = all(
                                any(eq(mul(p, r), p2) for p2 in P) and 
                                any(eq(mul(r, p), p2) for p2 in P) 
                                for p in P for r in R
                            )
                            h1 = is_ideal
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails at the witness.
    # Conclusion: P is a prime ideal iff there exists an integral domain D and a homomorphism phi: R -> D with ker(phi) = P.
    # This is equivalent to: P is a prime ideal iff (R/P is commutative AND R/P has no zero divisors).
    try:
        # Check LHS: P is a prime ideal (for all a, b in R, aRb subset P implies a in P or b in P)
        is_prime = True
        for a in R:
            for b in R:
                aRb_in_P = True
                for r in R:
                    arb = mul(a, mul(r, b))
                    if not any(eq(arb, p) for p in P):
                        aRb_in_P = False
                        break
                if aRb_in_P:
                    a_in_P = any(eq(a, p) for p in P)
                    b_in_P = any(eq(b, p) for p in P)
                    if not a_in_P and not b_in_P:
                        is_prime = False
                        break
            if not is_prime:
                break
                
        # Check RHS part 1: R/P is commutative (for all a, b in R, ab - ba in P)
        is_commutative = True
        for a in R:
            for b in R:
                ab = mul(a, b)
                ba = mul(b, a)
                # ab == ba mod P <=> ab in ba + P
                if not any(eq(ab, add(ba, p)) for p in P):
                    is_commutative = False
                    break
            if not is_commutative:
                break
                
        # Check RHS part 2: R/P has no zero divisors (for all a, b in R, ab in P implies a in P or b in P)
        no_zero_divisors = True
        for a in R:
            for b in R:
                ab = mul(a, b)
                if any(eq(ab, p) for p in P):
                    a_in_P = any(eq(a, p) for p in P)
                    b_in_P = any(eq(b, p) for p in P)
                    if not a_in_P and not b_in_P:
                        no_zero_divisors = False
                        break
            if not no_zero_divisors:
                break
                
        rhs = is_commutative and no_zero_divisors
        
        # The conjecture claims LHS == RHS. We want the negation (LHS != RHS).
        Q = (is_prime == rhs)
        neg_q = not Q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a proper ideal of R",
    "¬Q: The equivalence between P being a prime ideal and the existence of an integral domain D with ker(phi) = P fails"
]

N_HYP = 1
NEG_Q_INDEX = 1