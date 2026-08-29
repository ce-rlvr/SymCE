import sympy as sp
import math

def conditions(witness):
    try:
        # H_1: x is in the interval (0, 1)
        h1 = bool(witness > 0 and witness < 1)
    except Exception:
        h1 = False

    try:
        # ¬Q: The limit as n -> infinity of (q_n)^{1/n} does not exist or does not equal e^{\pi^2 / (12 \ln 2)}
        # We evaluate the continued fraction of the witness up to 200 terms.
        val = witness.evalf(400)
        cf = []
        for _ in range(200):
            f = sp.floor(val)
            cf.append(int(f))
            val = val - f
            # If the remaining value is extremely small, the continued fraction terminates (rational number)
            if val < 1e-200:
                break
            val = 1 / val
            
        if len(cf) < 200:
            # Finite continued fraction means the sequence q_n is finite, so the limit does not exist.
            neg_q = True
        else:
            n = len(cf)
            periodic = False
            # Check if the continued fraction is periodic (quadratic irrational)
            for p in range(1, n // 4 + 1):
                reps = max(5, 80 // p)
                if reps * p >= n:
                    continue
                
                is_p = True
                for i in range(1, reps):
                    if cf[-p:] != cf[-(i + 1) * p : -i * p]:
                        is_p = False
                        break
                if is_p:
                    periodic = True
                    break
            
            if periodic:
                # Quadratic irrationals have algebraic limits, which differ from the transcendental Lévy constant.
                neg_q = True
            else:
                # For other irrationals, we numerically estimate the limit at n=200.
                q_prev2 = 0
                q_prev1 = 1
                for a in cf:
                    q_curr = a * q_prev1 + q_prev2
                    q_prev2 = q_prev1
                    q_prev1 = q_curr
                
                q_n = q_curr
                if q_n > 0:
                    # Use math.log to safely handle arbitrarily large integers without OverflowError
                    val_limit = math.exp(math.log(q_n) / len(cf))
                    levy = math.exp(math.pi**2 / (12 * math.log(2)))
                    
                    # If the numerical estimate is far from Lévy's constant, it's a valid counterexample.
                    if abs(val_limit - levy) > 0.5:
                        neg_q = True
                    else:
                        # If it's close, we cannot rigorously confirm it as a counterexample.
                        neg_q = False
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a real number chosen uniformly at random from the interval (0,1) with respect to the Lebesgue measure",
    "¬Q: The limit as n -> infinity of (q_n)^{1/n} does not exist or does not equal e^{\pi^2 / (12 \ln 2)}"
]

N_HYP = 1
NEG_Q_INDEX = 1