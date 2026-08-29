import itertools
from sympy import Matrix, eye, zeros

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Define M2_Z2: Ring of 2x2 matrices over Z_2
M2_Z2 = [Matrix(2, 2, [a, b, c, d]) for a, b, c, d in itertools.product([0, 1], repeat=4)]

def add(a, b, mod):
    if mod:
        try:
            return (a + b).applyfunc(lambda x: x % mod)
        except AttributeError:
            return (a + b) % mod
    else:
        return a + b

def mul(a, b, mod):
    if mod:
        try:
            return (a * b).applyfunc(lambda x: x % mod)
        except AttributeError:
            return (a * b) % mod
    else:
        return a * b

def get_str(a):
    try:
        return str(a.tolist())
    except AttributeError:
        return str(a)

def get_sqrt_I(I, R, mod):
    I_str = set(get_str(m) for m in I)
    sqrt_I = []
    for x in R:
        curr = x
        found = False
        for _ in range(len(R) + 1):
            if get_str(curr) in I_str:
                found = True
                break
            curr = mul(curr, x, mod)
        if found:
            sqrt_I.append(x)
    return sqrt_I

def conditions(witness):
    """
    witness should be a tuple (R, I, mod) or (R, I)
    where R is a list of ring elements, I is a list of ideal elements,
    and mod is an optional integer for modular arithmetic.
    """
    try:
        if len(witness) == 3:
            R, I, mod = witness
        elif len(witness) == 2:
            R, I = witness
            mod = 0
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: I is an ideal of R
    try:
        h1 = False
        if R and I:
            R_str = set(get_str(m) for m in R)
            I_str = set(get_str(m) for m in I)
            if I_str.issubset(R_str):
                is_ring = True
                for a in R:
                    for b in R:
                        if get_str(add(a, b, mod)) not in R_str: is_ring = False
                        if get_str(mul(a, b, mod)) not in R_str: is_ring = False
                
                zeros_list = [x for x in R if get_str(add(x, x, mod)) == get_str(x)]
                if not zeros_list:
                    is_ring = False
                else:
                    zero_str = get_str(zeros_list[0])
                    for a in R:
                        if not any(get_str(add(a, b, mod)) == zero_str for b in R):
                            is_ring = False
                            
                is_ideal = True
                if is_ring:
                    if zero_str not in I_str:
                        is_ideal = False
                    for a in I:
                        if not any(get_str(add(a, b, mod)) == zero_str for b in I):
                            is_ideal = False
                        for b in I:
                            if get_str(add(a, b, mod)) not in I_str: is_ideal = False
                    for i in I:
                        for r in R:
                            if get_str(mul(i, r, mod)) not in I_str: is_ideal = False
                            if get_str(mul(r, i, mod)) not in I_str: is_ideal = False
                
                h1 = is_ring and is_ideal
    except Exception:
        h1 = False

    # H2: definition of sqrt_I
    h2 = True

    # neg_Q: sqrt_I is not an ideal of R
    try:
        sqrt_I = get_sqrt_I(I, R, mod)
        sqrt_I_str = set(get_str(m) for m in sqrt_I)
        
        is_sqrt_ideal = True
        if not sqrt_I:
            is_sqrt_ideal = False
        else:
            zeros_list = [x for x in R if get_str(add(x, x, mod)) == get_str(x)]
            if zeros_list:
                zero_str = get_str(zeros_list[0])
                if zero_str not in sqrt_I_str:
                    is_sqrt_ideal = False
                
                for a in sqrt_I:
                    if not any(get_str(add(a, b, mod)) == zero_str for b in sqrt_I):
                        is_sqrt_ideal = False
            
            for a in sqrt_I:
                for b in sqrt_I:
                    if get_str(add(a, b, mod)) not in sqrt_I_str:
                        is_sqrt_ideal = False
            
            for s in sqrt_I:
                for r in R:
                    if get_str(mul(s, r, mod)) not in sqrt_I_str:
                        is_sqrt_ideal = False
                    if get_str(mul(r, s, mod)) not in sqrt_I_str:
                        is_sqrt_ideal = False
                        
        neg_q = not is_sqrt_ideal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: sqrt(I) is the set of all x in R such that x^n in I for some n >= 1",
    "¬Q: sqrt(I) is not an ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2