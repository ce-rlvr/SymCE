import sympy
import itertools

# Witness should be a tuple (n, S) where n is an integer >= 2 representing the ring ZZ/nZZ,
# and S is a list of integers representing the subset S.

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: There is no inclusion-preserving bijection between the prime ideals of S^{-1}R and the prime ideals of R that do not intersect S"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        n, S = witness
        if not isinstance(n, int) or n < 2 or n > 100:
            return [False, False]
        if not isinstance(S, (list, set, tuple)):
            return [False, False]
        S = list(set(S))
        for s in S:
            if not isinstance(s, int) or s < 0 or s >= n:
                return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: R = ZZ/nZZ is always a commutative ring with identity
    h1 = True
    
    try:
        # 1. Prime ideals of R not intersecting S
        prime_factors = sympy.primefactors(n)
        prime_ideals_R = []
        for p in prime_factors:
            ideal = set(range(0, n, p))
            prime_ideals_R.append(ideal)
            
        prime_ideals_not_S = [P for P in prime_ideals_R if P.isdisjoint(S)]
        
        # 2. Construct S^{-1}R
        if not S:
            # S is empty, S^-1 R is empty, not a ring
            return [h1, True]
            
        # Check if S is multiplicatively closed
        is_mult_closed = True
        for s1 in S:
            for s2 in S:
                if (s1 * s2) % n not in S:
                    is_mult_closed = False
                    break
            if not is_mult_closed:
                break
                
        if not is_mult_closed:
            # S is not multiplicatively closed, standard construction fails to form a ring
            return [h1, True]
            
        # Equivalence relation
        elements = [(r, s) for r in range(n) for s in S]
        classes = []
        for e in elements:
            found = False
            for c in classes:
                r1, s1 = e
                r2, s2 = c[0]
                if any((u * (r1 * s2 - r2 * s1)) % n == 0 for u in S):
                    c.append(e)
                    found = True
                    break
            if not found:
                classes.append([e])
                
        # Check addition
        add_table = {}
        for i, C1 in enumerate(classes):
            for j, C2 in enumerate(classes):
                r1, s1 = C1[0]
                r2, s2 = C2[0]
                s_new = (s1 * s2) % n
                if s_new not in S:
                    return [h1, True]
                r_new = (r1 * s2 + r2 * s1) % n
                class_idx = -1
                for k, C3 in enumerate(classes):
                    r3, s3 = C3[0]
                    if any((u * (r_new * s3 - r3 * s_new)) % n == 0 for u in S):
                        class_idx = k
                        break
                if class_idx == -1:
                    return [h1, True]
                add_table[(i, j)] = class_idx
                
        # Check multiplication
        mul_table = {}
        for i, C1 in enumerate(classes):
            for j, C2 in enumerate(classes):
                r1, s1 = C1[0]
                r2, s2 = C2[0]
                s_new = (s1 * s2) % n
                if s_new not in S:
                    return [h1, True]
                r_new = (r1 * r2) % n
                class_idx = -1
                for k, C3 in enumerate(classes):
                    r3, s3 = C3[0]
                    if any((u * (r_new * s3 - r3 * s_new)) % n == 0 for u in S):
                        class_idx = k
                        break
                if class_idx == -1:
                    return [h1, True]
                mul_table[(i, j)] = class_idx
                
        # Find zero element
        zero_idx = -1
        for i in range(len(classes)):
            if all(add_table[(i, j)] == j for j in range(len(classes))):
                zero_idx = i
                break
        if zero_idx == -1:
            return [h1, True]
            
        # Find all ideals (S^-1 R is a principal ideal ring)
        n_classes = len(classes)
        ideals = []
        for a in range(n_classes):
            ideal = set()
            for x in range(n_classes):
                ideal.add(mul_table[(a, x)])
            if ideal not in ideals:
                ideals.append(ideal)
                
        # Find prime ideals
        prime_ideals_S_inv_R = []
        all_elements = set(range(n_classes))
        for I in ideals:
            if I == all_elements:
                continue
            is_prime = True
            for a in all_elements - I:
                for b in all_elements - I:
                    if mul_table[(a, b)] in I:
                        is_prime = False
                        break
                if not is_prime:
                    break
            if is_prime:
                prime_ideals_S_inv_R.append(I)
                
        # Check bijection
        if len(prime_ideals_S_inv_R) != len(prime_ideals_not_S):
            return [h1, True]
            
        def get_poset(ideals_list):
            poset = []
            for i, I1 in enumerate(ideals_list):
                for j, I2 in enumerate(ideals_list):
                    if i != j and I1.issubset(I2):
                        poset.append((i, j))
            return set(poset)
            
        poset_R = get_poset(prime_ideals_not_S)
        poset_S = get_poset(prime_ideals_S_inv_R)
        
        k = len(prime_ideals_not_S)
        bijection_exists = False
        for p in itertools.permutations(range(k)):
            valid = True
            for i, j in poset_R:
                if (p[i], p[j]) not in poset_S:
                    valid = False
                    break
            if valid:
                for i, j in poset_S:
                    inv_i = p.index(i)
                    inv_j = p.index(j)
                    if (inv_i, inv_j) not in poset_R:
                        valid = False
                        break
            if valid:
                bijection_exists = True
                break
                
        neg_q = not bijection_exists
        return [h1, neg_q]
        
    except Exception:
        return [False, False]