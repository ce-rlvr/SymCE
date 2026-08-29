import itertools

CONDITION_LABELS = [
    "H_1: I1 and J1 are ideals of R1 such that I1 + J1 = R1",
    "H_2: I2 and J2 are ideals of R2 such that I2 + J2 = R2",
    "¬Q: The product ideals I1 x I2 and J1 x J2 are NOT comaximal in R1 x R2"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_ideal(I, R, add, mul):
    if not I:
        return False
    if not all(x in R for x in I):
        return False
    
    # Find additive identity (zero) in R
    zeros = [z for z in R if all(add(x, z) == x and add(z, x) == x for x in R)]
    if not zeros:
        return False
    zero = zeros[0]
    
    if zero not in I:
        return False
    
    # Check closure under addition
    for x in I:
        for y in I:
            if add(x, y) not in I:
                return False
                
    # Check existence of additive inverses in I
    for x in I:
        if not any(add(x, y) == zero and add(y, x) == zero for y in I):
            return False
            
    # Check closure under multiplication by any element in R (absorbing property)
    for x in I:
        for r in R:
            if mul(r, x) not in I:
                return False
            if mul(x, r) not in I:
                return False
                
    return True

def is_sum_R(I, J, R, add):
    sums = set()
    for x in I:
        for y in J:
            sums.add(add(x, y))
    return set(sums) == set(R)

def conditions(witness):
    """
    witness is expected to be a dictionary with the following keys:
    'R1', 'R2': lists of elements representing the rings
    'I1', 'J1': lists of elements representing ideals in R1
    'I2', 'J2': lists of elements representing ideals in R2
    'add1', 'mul1': callable functions (x, y) -> z for operations in R1
    'add2', 'mul2': callable functions (x, y) -> z for operations in R2
    """
    try:
        R1 = witness['R1']
        R2 = witness['R2']
        I1 = witness['I1']
        J1 = witness['J1']
        I2 = witness['I2']
        J2 = witness['J2']
        add1 = witness['add1']
        mul1 = witness['mul1']
        add2 = witness['add2']
        mul2 = witness['mul2']
    except (KeyError, TypeError):
        return [False, False, False]

    # Check H_1
    try:
        h1 = is_ideal(I1, R1, add1, mul1) and is_ideal(J1, R1, add1, mul1) and is_sum_R(I1, J1, R1, add1)
    except Exception:
        h1 = False

    # Check H_2
    try:
        h2 = is_ideal(I2, R2, add2, mul2) and is_ideal(J2, R2, add2, mul2) and is_sum_R(I2, J2, R2, add2)
    except Exception:
        h2 = False

    # Check ¬Q
    # Q: The product ideals I1 x I2 and J1 x J2 are comaximal in R1 x R2.
    # Comaximal means their sum equals the entire ring R1 x R2.
    # ¬Q: Their sum does NOT equal R1 x R2.
    try:
        sums = set()
        for i1 in I1:
            for j1 in J1:
                for i2 in I2:
                    for j2 in J2:
                        # Sum of (i1, i2) in I1xI2 and (j1, j2) in J1xJ2
                        sums.add((add1(i1, j1), add2(i2, j2)))
                        
        R_prod = set()
        for r1 in R1:
            for r2 in R2:
                R_prod.add((r1, r2))
                
        neg_q = sums != R_prod
        
        # Fallback check in case the conjecture intended the ideal products I1*I2 and J1*J2 in a single ring R
        # (A common false conjecture that might have been mistranslated into the prompt's text)
        if not neg_q and R1 == R2:
            try:
                ideal_prod_I = set(add1(i1, i2) for i1 in I1 for i2 in I2)
                ideal_prod_J = set(add1(j1, j2) for j1 in J1 for j2 in J2)
                sum_ideal_prods = set(add1(x, y) for x in ideal_prod_I for y in ideal_prod_J)
                if set(sum_ideal_prods) != set(R1):
                    neg_q = True
            except Exception:
                pass
                
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]