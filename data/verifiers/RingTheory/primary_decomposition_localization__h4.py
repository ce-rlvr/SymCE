import math
from sympy import factorint

# Top-level setup
# The witness should be a dictionary representing an example in the ring of integers Z.
# Format:
# witness = {
#     "ring": "Z",
#     "I": 6,             # Generator of the ideal I (integer > 1)
#     "Q": [2, 3],        # Generators of the primary ideals Q_i (list of integers > 1)
#     "S": [2]            # Generators of the multiplicatively closed subset S (list of integers)
# }

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, dict):
            return [False, False, False, False]
            
        if witness.get("ring", "Z") != "Z":
            return [False, False, False, False]
            
        I = abs(witness.get('I', 0))
        Q = [abs(q) for q in witness.get('Q', [])]
        S = [abs(s) for s in witness.get('S', [])]
        
        if I == 0 or not Q or not S:
            return [False, False, False, False]
            
        # H1: R is a commutative ring with identity
        h1 = True
        
        # H2: S is a multiplicatively closed subset of R
        h2 = True
        
        # H3: I is a proper ideal of R with a minimal primary decomposition I = ∩_{i=1}^n Q_i
        h3 = False
        if I > 1:
            is_primary = True
            for q in Q:
                if q <= 1:
                    is_primary = False
                    break
                factors = factorint(q)
                if len(factors) != 1:
                    is_primary = False
                    break
            
            if is_primary:
                lcm_Q = 1
                for q in Q:
                    lcm_Q = (lcm_Q * q) // math.gcd(lcm_Q, q)
                if lcm_Q == I:
                    radicals = set()
                    for q in Q:
                        p = list(factorint(q).keys())[0]
                        radicals.add(p)
                    if len(radicals) == len(Q):
                        is_minimal = True
                        for i in range(len(Q)):
                            lcm_without_i = 1
                            for j in range(len(Q)):
                                if i != j:
                                    lcm_without_i = (lcm_without_i * Q[j]) // math.gcd(lcm_without_i, Q[j])
                            if lcm_without_i == I:
                                is_minimal = False
                                break
                        if is_minimal:
                            h3 = True
                            
        # Conclusion: S^{-1}I has a minimal primary decomposition S^{-1}I = ∩_{i=1}^m S^{-1}Q_i
        if 0 in S:
            is_proper = False
            S_primes = set()
        else:
            S_primes = set()
            for s in S:
                S_primes.update(factorint(abs(s)).keys())
            I_primes = set(factorint(I).keys()) if I > 1 else set()
            is_proper = not I_primes.issubset(S_primes)
        
        conclusion_holds = False
        if is_proper:
            for m in range(1, len(Q) + 1):
                valid_components = True
                for i in range(m):
                    p = list(factorint(Q[i]).keys())[0]
                    if p in S_primes:
                        valid_components = False
                        break
                if not valid_components:
                    continue
                    
                lcm_m = 1
                for i in range(m):
                    lcm_m = (lcm_m * Q[i]) // math.gcd(lcm_m, Q[i])
                
                equal_ideals = True
                for p in I_primes - S_primes:
                    val_I = 0
                    temp = I
                    while temp % p == 0:
                        val_I += 1
                        temp //= p
                        
                    val_lcm = 0
                    temp = lcm_m
                    while temp % p == 0:
                        val_lcm += 1
                        temp //= p
                        
                    if val_I != val_lcm:
                        equal_ideals = False
                        break
                
                if equal_ideals:
                    conclusion_holds = True
                    break
                    
        neg_q = not conclusion_holds
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: I is a proper ideal of R with a minimal primary decomposition I = ∩_{i=1}^n Q_i",
    "¬Q: The extended ideal S^{-1}I does not have a minimal primary decomposition S^{-1}I = ∩_{i=1}^m S^{-1}Q_i"
]

N_HYP = 3
NEG_Q_INDEX = 3