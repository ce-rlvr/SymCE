import sympy
import sympy.ntheory

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        p, k = witness
        if not isinstance(p, (int, sympy.Integer)) or not isinstance(k, (int, sympy.Integer)):
            return [False, False]
        p = int(p)
        k = int(k)
    except Exception:
        return [False, False]
    
    try:
        h1 = (k > 0) and ((p - 1) % k == 0)
    except Exception:
        h1 = False
        
    try:
        if p <= 1 or k <= 0:
            neg_q = False
        else:
            elements_of_order_k = []
            for x in range(1, p):
                if sympy.gcd(x, p) != 1:
                    continue
                if pow(x, k, p) != 1:
                    continue
                is_order_k = True
                for d in range(1, k):
                    if k % d == 0:
                        if pow(x, d, p) == 1:
                            is_order_k = False
                            break
                if is_order_k:
                    elements_of_order_k.append(x)
            
            sum_elements = sum(elements_of_order_k) % p
            mu_k = sympy.ntheory.mobius(k) % p
            
            neg_q = bool(sum_elements != mu_k)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is a positive integer that divides p - 1",
    "¬Q: The sum of elements of order k modulo p is not congruent to mu(k) modulo p"
]

N_HYP = 1
NEG_Q_INDEX = 1