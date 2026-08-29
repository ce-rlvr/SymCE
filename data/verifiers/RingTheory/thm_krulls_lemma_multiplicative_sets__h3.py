import sympy
import math

# Top-level setup
# Expected witness format:
# witness = (n, S, I)
# where:
#   n is an integer >= 2, representing the commutative ring Z/nZ
#   S is a list or set of integers, representing the multiplicative subset
#   I is a list or set of integers, representing the ideal

def conditions(witness) -> list[bool]:
    try:
        n, S, I = witness
    except Exception:
        return [False, False, False]
        
    # H1: R is a commutative ring
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and int(n) >= 2
    except Exception:
        h1 = False

    # H2: S is a multiplicative subset of R
    try:
        if h1:
            n_int = int(n)
            S_set = set(S)
            if not all(isinstance(x, (int, sympy.Integer)) for x in S_set):
                h2 = False
            else:
                S_set = {int(x) % n_int for x in S_set}
                # A multiplicative subset must contain 1 and be closed under multiplication
                if 1 not in S_set:
                    h2 = False
                else:
                    h2 = all((a * b) % n_int in S_set for a in S_set for b in S_set)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The ideal I is not a prime ideal of R
    try:
        if h1:
            n_int = int(n)
            I_set = set(I)
            if not all(isinstance(x, (int, sympy.Integer)) for x in I_set):
                is_prime_ideal = False
            else:
                I_set = {int(x) % n_int for x in I_set}
                if not I_set:
                    is_prime_ideal = False
                else:
                    # Check if I is an ideal
                    is_ideal = True
                    for a in I_set:
                        for b in I_set:
                            if (a + b) % n_int not in I_set:
                                is_ideal = False
                                break
                        if not is_ideal:
                            break
                    if is_ideal:
                        for a in I_set:
                            for r in range(n_int):
                                if (a * r) % n_int not in I_set:
                                    is_ideal = False
                                    break
                            if not is_ideal:
                                break
                    
                    if not is_ideal:
                        is_prime_ideal = False
                    elif len(I_set) == n_int:
                        is_prime_ideal = False # A prime ideal must be a proper ideal
                    else:
                        # Check if I is prime
                        is_prime = True
                        for a in range(n_int):
                            for b in range(n_int):
                                if (a * b) % n_int in I_set:
                                    if a not in I_set and b not in I_set:
                                        is_prime = False
                                        break
                            if not is_prime:
                                break
                        is_prime_ideal = is_prime
            neg_q = not is_prime_ideal
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicative subset of R",
    "¬Q: The ideal I is not a prime ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2