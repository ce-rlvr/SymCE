import sympy
import math
import itertools
import functools
import z3

# Top-level setup (empty for Number Theory)

def conditions(witness) -> list[bool]:
    def evaluate(a, k):
        # H1: k >= 3
        try:
            h1 = bool(k >= 3)
        except Exception:
            h1 = False
            
        # H2: a is an odd integer
        try:
            h2 = False
            if int(a) == a:
                h2 = bool(int(a) % 2 != 0)
        except Exception:
            h2 = False
            
        # Neg_Q: a^{2^{k-2}} \not\equiv 1 \pmod{2^k}
        try:
            # If k is an exact integer, we can use fast modular exponentiation
            if int(k) == k and int(a) == a and k >= 2:
                if k > 100000:  # Prevent denial of service from maliciously large k
                    neg_q = False
                else:
                    neg_q = bool(pow(int(a), 2**(int(k)-2), 2**int(k)) != 1)
            else:
                # If k is a float/fractional (the likely dropped hypothesis), use float arithmetic
                kf = float(k)
                af = float(a)
                exponent = 2.0**(kf - 2.0)
                modulus = 2.0**kf
                
                # Avoid complex numbers if base is negative and exponent is fractional
                if af < 0 and not exponent.is_integer():
                    neg_q = False
                else:
                    res = (af ** exponent) % modulus
                    # Check if it is not congruent to 1 (allowing for floating point inaccuracies)
                    neg_q = bool(abs(res - 1.0) > 1e-9)
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]

    # Handle dictionary witnesses
    if isinstance(witness, dict):
        return evaluate(witness.get('a'), witness.get('k'))
    
    # Handle tuple/list witnesses
    elif isinstance(witness, (tuple, list)) and len(witness) == 2:
        # Try both (a, k) and (k, a) assignments and pick the one that satisfies more hypotheses
        res1 = evaluate(witness[0], witness[1])
        res2 = evaluate(witness[1], witness[0])
        
        score1 = res1[0] + res1[1]
        score2 = res2[0] + res2[1]
        if score2 > score1:
            return res2
        return res1
        
    else:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: k >= 3",
    "H_2: a is an odd integer",
    "¬Q: a^{2^{k-2}} is not congruent to 1 mod 2^k"
]

N_HYP = 2
NEG_Q_INDEX = 2