import math

# Top-level setup
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z10 = 10
Z12 = 12

I2_6 = [0, 2, 4]
I3_6 = [0, 3]

I2_8 = [0, 2, 4, 6]

I2_10 = [0, 2, 4, 6, 8]
I5_10 = [0, 5]

I2_12 = [0, 2, 4, 6, 8, 10]
I3_12 = [0, 3, 6, 9]
I4_12 = [0, 4, 8]
I6_12 = [0, 6]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n', witness.get('R', None))
            M_list = witness.get('M_list', witness.get('ideals', []))
        elif isinstance(witness, tuple) and len(witness) == 2:
            n, M_list = witness
        else:
            return [False, False]
            
        n = int(n)
        if n < 2:
            return [False, False]
            
        if isinstance(M_list, int):
            M_list = [M_list]
            
        R = set(range(n))
        union_M = set()
        for M in M_list:
            try:
                m_val = int(M)
                union_M.update((m_val * k) % n for k in range(n))
            except (TypeError, ValueError):
                union_M.update(int(x) % n for x in M)
                
        S = R - union_M
        
        # H1: S is a multiplicative subset
        if 1 not in S:
            h1 = False
        else:
            h1 = True
            for a in S:
                for b in S:
                    if (a * b) % n not in S:
                        h1 = False
                        break
                if not h1:
                    break
                    
        # neg_Q: R -> S^{-1}R is not an isomorphism
        # For finite rings Z/nZ, the canonical map is an isomorphism 
        # if and only if S consists entirely of units.
        neg_q = False
        for s in S:
            if math.gcd(s, n) > 1:
                neg_q = True
                break
                
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: S = R \\ union(M_i) is a multiplicative subset",
    "¬Q: The canonical homomorphism R -> S^{-1}R is not an isomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1