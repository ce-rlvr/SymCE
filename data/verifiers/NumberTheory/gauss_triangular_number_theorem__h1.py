import sympy
import sympy.ntheory
from sympy import Integer, Rational

CONDITION_LABELS = [
    "¬Q: n cannot be written as the sum of three triangular numbers"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        if isinstance(witness, int):
            n = witness
        else:
            if hasattr(witness, 'is_integer') and not callable(witness.is_integer):
                if witness.is_integer:
                    n = int(witness)
                else:
                    return [True]
            else:
                n_float = float(witness)
                if not n_float.is_integer():
                    return [True]
                n = int(n_float)
                
        if n < 0:
            neg_q = True
        else:
            if n <= 100000:
                triangulars = []
                k = 0
                while True:
                    t = k * (k + 1) // 2
                    if t > n:
                        break
                    triangulars.append(t)
                    k += 1
                
                t_set = set(triangulars)
                found = False
                for i in range(len(triangulars)):
                    t1 = triangulars[i]
                    for j in range(i, len(triangulars)):
                        t2 = triangulars[j]
                        if t1 + t2 > n:
                            break
                        if (n - t1 - t2) in t_set:
                            found = True
                            break
                    if found:
                        break
                neg_q = not found
            else:
                # By Gauss's Eureka Theorem, every non-negative integer is the sum of 3 triangular numbers.
                neg_q = False
    except Exception:
        neg_q = False

    return [neg_q]