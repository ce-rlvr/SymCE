import sympy
import math

# Top-level setup
# (No specific named objects are required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        n, a, k = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = (int(n) == n) and (n > 1)
    except Exception:
        h1 = False

    try:
        h2 = (int(a) == a)
    except Exception:
        h2 = False

    try:
        h3 = False
        if h1 and h2:
            h3 = math.gcd(int(a), int(n)) == 1
    except Exception:
        h3 = False

    try:
        Q = False
        if h1 and h2:
            n_val = int(n)
            a_val = int(a)
            
            try:
                is_k_int = (int(k) == k)
            except Exception:
                is_k_int = False

            if is_k_int:
                k_int = int(k)
                if k_int >= 0:
                    A_int = a_val ** k_int
                    if math.gcd(A_int, n_val) == 1:
                        inv_A = pow(A_int, -1, n_val)
                        inv_a = pow(a_val, -1, n_val)
                        B_int = inv_a ** k_int
                        if inv_A % n_val == B_int % n_val:
                            Q = True
                else:
                    if a_val in (1, -1):
                        A_int = int(a_val ** k_int)
                        if math.gcd(A_int, n_val) == 1:
                            inv_A = pow(A_int, -1, n_val)
                            inv_a = pow(a_val, -1, n_val)
                            B_int = int(inv_a ** k_int)
                            if inv_A % n_val == B_int % n_val:
                                Q = True
            else:
                # Fractional k
                A = a_val ** k
                A_float = float(A)
                if A_float.is_integer():
                    A_int = int(A_float)
                    if math.gcd(A_int, n_val) == 1:
                        inv_A = pow(A_int, -1, n_val)
                        inv_a = pow(a_val, -1, n_val)
                        B = inv_a ** k
                        B_float = float(B)
                        if B_float.is_integer():
                            B_int = int(B_float)
                            if inv_A % n_val == B_int % n_val:
                                Q = True
    except Exception:
        Q = False

    neg_q = not Q

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: a is an integer",
    "H_3: a is invertible modulo n",
    "¬Q: a^k is not invertible modulo n, or its modular inverse is not congruent to (a^-1)^k (mod n)"
]

N_HYP = 3
NEG_Q_INDEX = 3