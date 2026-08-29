import sympy
import itertools
import math

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        K, L, S = witness
    except Exception:
        return [False, False]
        
    try:
        K = list(K)
        L = list(L)
        S = list(S)
    except Exception:
        return [False, False]

    # Find zero in K
    try:
        zeros_K = [x for x in K if x + x == x]
        if not zeros_K:
            h1 = False
        else:
            zero = zeros_K[0]
            
            # Find identity in K
            identities = [x for x in K if x * x == x and x != zero]
            if not identities:
                h1 = False
            else:
                I = identities[0]
                
                # Check if S is a subset of L
                S_is_subset = all(any(s == l for l in L) for s in S)
                if not S_is_subset:
                    h1 = False
                else:
                    if len(L) == 0:
                        max_degree = 1
                    else:
                        max_degree = int(math.ceil(math.log(len(L)) / math.log(len(K)))) + 1
                        
                    # Cap max_degree to ensure fast execution while being mathematically sufficient for finite rings
                    max_degree = max(1, min(max_degree, 10))
                    
                    def is_algebraic(x):
                        for d in range(1, max_degree + 1):
                            for coeffs in itertools.product(K, repeat=d + 1):
                                # Skip the zero polynomial
                                if all(c == zero for c in coeffs):
                                    continue
                                
                                val = zero
                                x_pow = I
                                for c in coeffs:
                                    val = val + c * x_pow
                                    x_pow = x_pow * x
                                
                                if val == zero:
                                    return True
                        return False

                    h1 = True
                    for l in L:
                        in_S = any(l == s for s in S)
                        alg = is_algebraic(l)
                        if in_S != alg:
                            h1 = False
                            break
    except Exception:
        h1 = False

    # neg_Q: S is not a subfield of L
    try:
        if not zeros_K or not identities:
            neg_q = False
        else:
            zero = zeros_K[0]
            I = identities[0]
            is_field = True
            
            if len(S) < 2:
                is_field = False
            else:
                # Check closure and commutativity
                for a in S:
                    for b in S:
                        if not any(a + b == s for s in S):
                            is_field = False
                        if not any(a * b == s for s in S):
                            is_field = False
                        if a * b != b * a:
                            is_field = False
                
                # Check inverses
                if is_field:
                    for a in S:
                        if a == zero:
                            continue
                        has_inv = False
                        for b in S:
                            if a * b == I:
                                has_inv = True
                                break
                        if not has_inv:
                            is_field = False
                            break
                        
            neg_q = not is_field
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S is the set of all elements in L that are algebraic over K",
    "¬Q: S is not a subfield of L"
]

N_HYP = 1
NEG_Q_INDEX = 1