import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def additive_closure(elements, R):
    closure = []
    for e in elements:
        if e not in closure and e in R:
            closure.append(e)
    
    queue = list(closure)
    while queue:
        curr = queue.pop(0)
        for e in elements:
            nxt = curr + e
            if nxt not in closure and nxt in R:
                closure.append(nxt)
                queue.append(nxt)
            nxt2 = curr - e
            if nxt2 not in closure and nxt2 in R:
                closure.append(nxt2)
                queue.append(nxt2)
    return closure

def ideal_generated_by(x, R):
    gens = [x]
    for r in R:
        val1 = r * x
        if val1 not in gens: gens.append(val1)
        val2 = x * r
        if val2 not in gens: gens.append(val2)
        rx = r * x
        for s in R:
            val3 = rx * s
            if val3 not in gens:
                gens.append(val3)
    return additive_closure(gens, R)

def is_nilpotent_ideal(I, K, R):
    if not I: return True
    if all(x in K for x in I): return True
    
    current_power = list(I)
    prev_len = -1
    
    while True:
        if all(x in K for x in current_power):
            return True
            
        if len(current_power) == prev_len:
            return False
            
        prev_len = len(current_power)
        
        next_gens = []
        for a in current_power:
            for b in I:
                val = a * b
                if val not in next_gens:
                    next_gens.append(val)
        
        current_power = additive_closure(next_gens, R)

def compute_nilradical(R):
    zero = R[0] - R[0]
    N = []
    for x in R:
        I_x = ideal_generated_by(x, R)
        if is_nilpotent_ideal(I_x, [zero], R):
            N.append(x)
    return N

def check_neg_Q(R, S, N):
    if not R or not S: return False
    zero = R[0] - R[0]
    
    # Check Ore condition (required for localization to be well-behaved)
    for r in R:
        for s in S:
            found = False
            for rp in R:
                s_rp = s * rp
                for sp in S:
                    if r * sp == s_rp:
                        found = True
                        break
                if found: break
            if not found: return False
            
            if s * r == zero:
                found2 = False
                for sp in S:
                    if r * sp == zero:
                        found2 = True
                        break
                if not found2: return False

    # Compute the kernel of the localization map
    K = []
    for x in R:
        for s in S:
            if x * s == zero:
                K.append(x)
                break
                
    # Compute the preimage of the nilradical of S^{-1}R
    J_max = []
    for x in R:
        I_x = ideal_generated_by(x, R)
        if is_nilpotent_ideal(I_x, K, R):
            J_max.append(x)
            
    # Compute the preimage of S^{-1}N
    N_plus_K = []
    for n in N:
        for k in K:
            val = n + k
            if val not in N_plus_K:
                N_plus_K.append(val)
                
    # If the preimages are not equal, the ideals in the localization are not equal
    if len(J_max) != len(N_plus_K):
        return True
        
    for x in J_max:
        if x not in N_plus_K: return True
        
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False]
        R, S, N = witness
        
        if not R: return [False, False, False]
        zero = R[0] - R[0]
        if zero not in R: return [False, False, False]
        
        # Verify R is a valid ring
        for a in R:
            for b in R:
                if a + b not in R: return [False, False, False]
                if a * b not in R: return [False, False, False]
                if a - b not in R: return [False, False, False]
        
        # H1: S is a multiplicatively closed subset of R
        h1 = True
        if not S:
            h1 = False
        else:
            for s in S:
                if s not in R:
                    h1 = False
                    break
            if h1:
                for a in S:
                    for b in S:
                        if a * b not in S:
                            h1 = False
                            break
                    if not h1: break

        # H2: N is the nilradical of R
        h2 = True
        try:
            N_true = compute_nilradical(R)
            if len(N) != len(N_true):
                h2 = False
            else:
                for x in N:
                    if x not in N_true:
                        h2 = False
                        break
        except Exception:
            h2 = False

        # neg_Q: The nilradical of S^{-1}R is NOT equal to S^{-1}N
        neg_q = False
        try:
            if h1 and h2:
                neg_q = check_neg_Q(R, S, N)
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: N is the nilradical of R",
    "¬Q: The nilradical of the localization S^{-1}R is not equal to S^{-1}N"
]

N_HYP = 2
NEG_Q_INDEX = 2