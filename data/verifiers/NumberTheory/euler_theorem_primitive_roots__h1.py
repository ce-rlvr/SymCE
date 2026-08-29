import sympy
import sympy.ntheory as ntheory

def conditions(witness):
    try:
        if isinstance(witness, bool):
            return [False]
        n = int(witness)
        if n != witness:
            return [False]
    except Exception:
        return [False]
    
    try:
        # Check if n has a primitive root
        # A primitive root exists modulo n iff n is in {1, 2, 4, p^k, 2p^k} for odd prime p, k >= 1
        if n < 1:
            has_prim = False
        elif n in (1, 2, 4):
            has_prim = True
        else:
            m = n // 2 if n % 2 == 0 else n
            if m % 2 == 0 or m == 1:
                has_prim = False
            else:
                factors = ntheory.factorint(m)
                has_prim = (len(factors) == 1)
        
        # Check if n is in the set {2, 4, p^k, 2p^k} for odd prime p, k >= 1
        if n in (2, 4):
            in_set = True
        elif n <= 1:
            in_set = False
        else:
            m = n // 2 if n % 2 == 0 else n
            if m % 2 == 0 or m == 1:
                in_set = False
            else:
                factors = ntheory.factorint(m)
                in_set = (len(factors) == 1)
                
        # The conclusion fails if the equivalence does not hold
        neg_q = (has_prim != in_set)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The equivalence (n has a primitive root iff n is in {2, 4, p^k, 2p^k}) fails"
]
N_HYP = 0
NEG_Q_INDEX = 0