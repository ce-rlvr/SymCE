import sympy
import math

def get_k(p):
    """
    Computes the 2-rank of the multiplicative group (Z/pZ)^*.
    This is exactly the number of independent generators of its Sylow 2-subgroup.
    The number of quadratic subfields of Q(zeta_p) is 2^k - 1.
    """
    if p <= 1:
        return 0
    temp = p
    a = 0
    while temp % 2 == 0:
        a += 1
        temp //= 2
    
    r = 0
    d = 3
    while d * d <= temp:
        if temp % d == 0:
            r += 1
            while temp % d == 0:
                temp //= d
        d += 2
    if temp > 1:
        r += 1
        
    k = r
    if a == 2:
        k += 1
    elif a >= 3:
        k += 2
    return k

def squarefree_part(n):
    """
    Returns the squarefree part of an integer n.
    """
    if n == 0: 
        return 0
    sign = -1 if n < 0 else 1
    n = abs(n)
    res = 1
    d = 2
    while d * d <= n:
        count = 0
        while n % d == 0:
            count += 1
            n //= d
        if count % 2 == 1:
            res *= d
        d += 1
    if n > 1:
        res *= n
    return sign * res

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        # The witness is expected to be the integer p
        p = int(witness)
        if p != witness:
            h1 = False
        else:
            h1 = (p >= 1)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_Q = False
        else:
            k = get_k(p)
            # If k != 1, the number of quadratic subfields is 2^k - 1 != 1.
            # Thus, it does not contain EXACTLY ONE quadratic subfield.
            if k != 1:
                neg_Q = True
            else:
                # If k == 1, there is exactly one quadratic subfield.
                # We must check if it matches the formula Q(sqrt((-1)^((p-1)/2) p)).
                if p % 2 == 0:
                    # If p is even, the formula exponent (p-1)/2 is not an integer,
                    # so it does not generate a valid quadratic subfield over Q.
                    neg_Q = True
                else:
                    # If p is odd and k == 1, p must be a prime power p1^a.
                    temp = p
                    d = 3
                    p1 = p
                    while d * d <= temp:
                        if temp % d == 0:
                            p1 = d
                            break
                        d += 2
                    
                    # The formula given in the conclusion
                    D_form = ((-1)**((p - 1) // 2)) * p
                    
                    # The actual unique quadratic subfield of Q(zeta_{p1^a}) is the same as Q(zeta_{p1})
                    d_actual = ((-1)**((p1 - 1) // 2)) * p1
                    
                    sq_form = squarefree_part(D_form)
                    sq_actual = squarefree_part(d_actual)
                    
                    # If sq_form == 1, the formula generates Q, not a quadratic field.
                    if sq_form == 1:
                        neg_Q = True
                    else:
                        # The fields are equal iff their squarefree parts match
                        neg_Q = (sq_form != sq_actual)
    except Exception:
        neg_Q = False

    return [h1, neg_Q]

CONDITION_LABELS = [
    "H_1: zeta_p is a primitive p-th root of unity",
    "¬Q: Q(zeta_p) does not contain exactly one quadratic subfield, or it is not equal to Q(sqrt((-1)^((p-1)/2) p))"
]

N_HYP = 1
NEG_Q_INDEX = 1