import sympy
import math

# Top-level setup
Z = sympy.S.Integers

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be a PID, M and N be arbitrary R-modules. Then Tor_n^R(M, N) is identically zero."
    
    The witness can be an integer `n`, or a tuple `(R, M, N, n)` where:
    - R is a string like 'Z' or sympy.S.Integers
    - M and N are lists of non-negative integers representing invariant factors of finitely generated Z-modules
      (e.g., [2] for Z/2Z, [0] for Z, [] for 0)
    - n is the index of the Tor functor
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            R, M, N, n = witness
        elif isinstance(witness, dict):
            R = witness.get('R', 'Z')
            M = witness.get('M', [2])
            N = witness.get('N', [2])
            n = witness.get('n', 1)
        elif isinstance(witness, int):
            # If only n is provided, we supply a default counterexample Z-module pair (Z/2Z, Z/2Z)
            R, M, N, n = 'Z', [2], [2], witness
        else:
            R, M, N, n = 'Z', [2], [2], 1
    except Exception:
        return [False, False, False]

    # H1: R is a principal ideal domain
    try:
        h1 = (R in ['Z', 'ZZ', Z, sympy.S.Integers])
    except Exception:
        h1 = False

    # H2: M and N are arbitrary R-modules
    try:
        h2 = (isinstance(M, list) and isinstance(N, list) and 
              all(isinstance(x, int) and x >= 0 for x in M) and 
              all(isinstance(x, int) and x >= 0 for x in N))
    except Exception:
        h2 = False

    # neg_Q: The Tor functor Tor_n^R(M, N) is NOT identically zero
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            if n >= 2:
                # Over a PID, Tor_n is 0 for n >= 2
                neg_q = False
            elif n == 1:
                # Tor_1^Z(M, N) computation
                is_zero = True
                for a in M:
                    for b in N:
                        if a != 0 and b != 0:
                            if math.gcd(a, b) > 1:
                                is_zero = False
                neg_q = not is_zero
            elif n == 0:
                # Tor_0^Z(M, N) is the tensor product M \otimes N
                is_zero = True
                for a in M:
                    for b in N:
                        if a == 0 and b == 0:
                            is_zero = False
                        elif a == 0 and b > 1:
                            is_zero = False
                        elif b == 0 and a > 1:
                            is_zero = False
                        elif a != 0 and b != 0 and math.gcd(a, b) > 1:
                            is_zero = False
                neg_q = not is_zero
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M and N are arbitrary R-modules",
    "¬Q: The Tor functor Tor_n^R(M, N) is not identically zero"
]

N_HYP = 2
NEG_Q_INDEX = 2