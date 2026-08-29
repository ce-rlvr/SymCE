import math
import sympy
from sympy.ntheory import factorint

# Top-level setup
# (No specific named objects needed for this conjecture)

CONDITION_LABELS = [
    "H_1: F is a finite field of order q and characteristic p",
    "H_2: K(a,b) is the Kloosterman sum",
    "¬Q: |K(a,b)| > 2*sqrt(q)"
]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            q = witness['q']
            a = witness['a']
            b = witness['b']
            p_wit = witness.get('p', None)
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            q, a, b = witness
            p_wit = None
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            q, p_wit, a, b = witness
        else:
            q, a, b, p_wit = 0, 0, 0, None
            
        try:
            q_val = int(q)
            is_int_q = (q_val == q)
        except Exception:
            q_val = 0
            is_int_q = False

        if is_int_q and q_val > 1:
            factors = factorint(q_val)
            if len(factors) == 1:
                p = list(factors.keys())[0]
                h1 = sympy.isprime(p)
                if p_wit is not None:
                    h1 = h1 and (p == int(p_wit))
            else:
                p = 0
                h1 = False
        else:
            p = 0
            h1 = False
    except Exception:
        h1 = False
        p = 0
        q_val = 0
        a = 0
        b = 0

    try:
        a_val = int(a)
        b_val = int(b)
        h2 = True
    except Exception:
        h2 = False
        a_val = 0
        b_val = 0

    try:
        neg_q = False
        if h1 and h2:
            if a_val % p == 0 and b_val % p == 0:
                k_sum_abs = float(q_val - 1)
                neg_q = k_sum_abs > 2 * math.sqrt(q_val) + 1e-9
            elif q_val == p:
                if p > 100000:
                    neg_q = False
                else:
                    k_sum_real = 0.0
                    k_sum_imag = 0.0
                    for x in range(1, p):
                        x_inv = pow(x, -1, p)
                        val = (a_val * x + b_val * x_inv) % p
                        angle = 2 * math.pi * val / p
                        k_sum_real += math.cos(angle)
                        k_sum_imag += math.sin(angle)
                    k_sum_abs = math.hypot(k_sum_real, k_sum_imag)
                    neg_q = k_sum_abs > 2 * math.sqrt(q_val) + 1e-9
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]