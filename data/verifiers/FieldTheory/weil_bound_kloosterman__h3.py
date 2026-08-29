import math
from sympy import isprime, Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    
    The conjecture claims that for a finite field F of order q and characteristic p,
    and non-zero elements a, b in F, the absolute value of the Kloosterman sum
    |K(a,b)| is bounded by 2*sqrt(q).
    
    The dropped hypothesis is that the additive character must be NON-TRIVIAL.
    If the trivial character is used, K(a,b) = sum_{x in F*} 1 = q - 1.
    For q >= 7, q - 1 > 2*sqrt(q), which violates the bound.
    """
    try:
        F, a, b = witness
    except Exception:
        return [False, False, False]

    # H_1: F is a finite field of order q and characteristic p
    h1_ok = False
    try:
        # Check if F has 'order' and 'characteristic' attributes (like a SymPy GaloisField)
        q = F.order
        p = F.characteristic
        # Verify q is a prime power and p is prime
        if isprime(p) and q > 1:
            # Check if q is a power of p
            temp_q = q
            while temp_q % p == 0:
                temp_q //= p
            if temp_q == 1:
                h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: a and b are non-zero elements of F
    h2_ok = False
    try:
        if h1_ok:
            # Check if a and b are non-zero
            if a != F.zero and b != F.zero:
                # Check if a and b belong to F (by checking their type or parent)
                if hasattr(a, 'field') and a.field == F and hasattr(b, 'field') and b.field == F:
                    h2_ok = True
                elif type(a) == type(F.one) and type(b) == type(F.one):
                    h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The absolute value |K(a,b)| is NOT bounded above by 2*sqrt(q)
    # Since the dropped hypothesis is that the character is non-trivial,
    # the conjecture fails if there exists an additive character (namely the trivial one)
    # for which the bound is violated. For the trivial character, K(a,b) = q - 1.
    neg_q_ok = False
    try:
        if h1_ok and h2_ok:
            q = F.order
            # The bound is 2 * sqrt(q)
            bound = 2 * math.sqrt(q)
            # For the trivial character, the sum is exactly q - 1
            trivial_kloosterman_sum = q - 1
            if trivial_kloosterman_sum > bound:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q and characteristic p",
    "H_2: a and b are non-zero elements of F",
    "¬Q: The absolute value |K(a,b)| is not bounded above by 2*sqrt(q) for all additive characters"
]

N_HYP = 2
NEG_Q_INDEX = 2