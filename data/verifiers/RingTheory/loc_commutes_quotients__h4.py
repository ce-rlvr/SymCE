import itertools

# Top-level setup: Standard finite rings Z/nZ for witness construction.
# A witness should be a tuple: (size, add_table, mul_table, S, I)
# where S and I are lists of elements (integers 0 to size-1).
# Example witness: (*Z6, [], [0, 3])

def make_Zn(n):
    add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
    mul_table = [[(i * j) % n for j in range(n)] for i in range(n)]
    return (n, add_table, mul_table)

Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z5 = make_Zn(5)
Z6 = make_Zn(6)
Z8 = make_Zn(8)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 5:
            return [False, False, False, False]
        size, add_table, mul_table, S, I = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring with identity
    def check_H1():
        if not isinstance(size, int) or size < 1: return False
        if len(add_table) != size or len(mul_table) != size: return False
        for row in add_table:
            if len(row) != size: return False
        for row in mul_table:
            if len(row) != size: return False
            
        # Commutativity
        for i in range(size):
            for j in range(size):
                if add_table[i][j] != add_table[j][i]: return False
                if mul_table[i][j] != mul_table[j][i]: return False
                
        # Associativity and Distributivity
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False

        # Additive identity
        zero = -1
        for i in range(size):
            if all(add_table[i][j] == j for j in range(size)):
                zero = i
                break
        if zero == -1: return False
        
        # Additive inverses
        neg = {}
        for i in range(size):
            has_inv = False
            for j in range(size):
                if add_table[i][j] == zero:
                    neg[i] = j
                    has_inv = True
                    break
            if not has_inv: return False
            
        # Multiplicative identity
        one = -1
        for i in range(size):
            if all(mul_table[i][j] == j for j in range(size)):
                one = i
                break
        if one == -1: return False
        
        return True, zero, one, neg

    try:
        h1_ok, zero, one, neg = check_H1()
    except Exception:
        h1_ok = False
        zero = one = neg = None
        
    if not h1_ok:
        return [False, False, False, False]

    # H2: S is a multiplicatively closed subset of R
    def check_H2():
        if not isinstance(S, (list, set, tuple)): return False
        for s in S:
            if s < 0 or s >= size: return False
        for a in S:
            for b in S:
                if mul_table[a][b] not in S: return False
        return True

    try:
        h2_ok = check_H2()
    except Exception:
        h2_ok = False

    # H3: I is an ideal of R
    def check_H3():
        if not isinstance(I, (list, set, tuple)): return False
        if len(I) == 0: return False
        for x in I:
            if x < 0 or x >= size: return False
        for a in I:
            for b in I:
                if add_table[a][neg[b]] not in I: return False
        for r in range(size):
            for a in I:
                if mul_table[r][a] not in I: return False
        return True

    try:
        h3_ok = check_H3()
    except Exception:
        h3_ok = False

    # Conclusion: The ring (S^{-1}R)/(S^{-1}I) is isomorphic to \bar{S}^{-1}(R/I)
    def check_conclusion():
        # If S is empty, S^-1 R is empty, which is not a valid ring.
        if len(S) == 0:
            return False

        # Compute S^-1 R
        classes = []
        for a in range(size):
            for s in S:
                found = False
                for cls in classes:
                    b, t = cls[0]
                    at = mul_table[a][t]
                    bs = mul_table[b][s]
                    diff = add_table[at][neg[bs]]
                    equiv = False
                    for u in S:
                        if mul_table[u][diff] == zero:
                            equiv = True
                            break
                    if equiv:
                        cls.append((a, s))
                        found = True
                        break
                if not found:
                    classes.append([(a, s)])
                    
        # Find indices of classes in S^-1 I
        S_inv_I_indices = []
        for i, cls in enumerate(classes):
            in_ideal = False
            for (a, s) in cls:
                if a in I:
                    in_ideal = True
                    break
            if in_ideal:
                S_inv_I_indices.append(i)
                
        # Quotient ring A = (S^-1 R) / (S^-1 I)
        A_classes = []
        for i in range(len(classes)):
            found = False
            for q_cls in A_classes:
                j = q_cls[0]
                a, s = classes[i][0]
                b, t = classes[j][0]
                
                at = mul_table[a][t]
                bs = mul_table[b][s]
                diff_num = add_table[at][neg[bs]]
                diff_den = mul_table[s][t]
                
                diff_idx = -1
                for k, cls in enumerate(classes):
                    if (diff_num, diff_den) in cls:
                        diff_idx = k
                        break
                if diff_idx in S_inv_I_indices:
                    q_cls.append(i)
                    found = True
                    break
            if not found:
                A_classes.append([i])
                
        # Compute R/I
        R_bar_classes = []
        for i in range(size):
            found = False
            for q_cls in R_bar_classes:
                j = q_cls[0]
                if add_table[i][neg[j]] in I:
                    q_cls.append(i)
                    found = True
                    break
            if not found:
                R_bar_classes.append([i])
                
        # Compute \bar{S}
        S_bar = []
        for s in S:
            for i, q_cls in enumerate(R_bar_classes):
                if s in q_cls:
                    if i not in S_bar:
                        S_bar.append(i)
                    break
                    
        # Localized ring B = \bar{S}^{-1}(R/I)
        B_classes = []
        for a_bar in range(len(R_bar_classes)):
            for s_bar in S_bar:
                found = False
                for cls in B_classes:
                    b_bar, t_bar = cls[0]
                    
                    a = R_bar_classes[a_bar][0]
                    s = R_bar_classes[s_bar][0]
                    b = R_bar_classes[b_bar][0]
                    t = R_bar_classes[t_bar][0]
                    
                    at = mul_table[a][t]
                    bs = mul_table[b][s]
                    diff = add_table[at][neg[bs]]
                    
                    equiv = False
                    for u_bar in S_bar:
                        u = R_bar_classes[u_bar][0]
                        val = mul_table[u][diff]
                        if val in I:
                            equiv = True
                            break
                    if equiv:
                        cls.append((a_bar, s_bar))
                        found = True
                        break
                if not found:
                    B_classes.append([(a_bar, s_bar)])
                    
        if len(A_classes) != len(B_classes):
            return False
            
        if len(A_classes) == 0:
            return False
            
        sizeA = len(A_classes)
        addA = [[0]*sizeA for _ in range(sizeA)]
        mulA = [[0]*sizeA for _ in range(sizeA)]
        for i in range(sizeA):
            for j in range(sizeA):
                c1 = A_classes[i][0]
                c2 = A_classes[j][0]
                a, s = classes[c1][0]
                b, t = classes[c2][0]
                
                num_add = add_table[mul_table[a][t]][mul_table[b][s]]
                den_add = mul_table[s][t]
                idx_add = -1
                for k, cls in enumerate(classes):
                    if (num_add, den_add) in cls:
                        idx_add = k
                        break
                for k, q_cls in enumerate(A_classes):
                    if idx_add in q_cls:
                        addA[i][j] = k
                        break
                        
                num_mul = mul_table[a][b]
                den_mul = mul_table[s][t]
                idx_mul = -1
                for k, cls in enumerate(classes):
                    if (num_mul, den_mul) in cls:
                        idx_mul = k
                        break
                for k, q_cls in enumerate(A_classes):
                    if idx_mul in q_cls:
                        mulA[i][j] = k
                        break
                        
        sizeB = len(B_classes)
        addB = [[0]*sizeB for _ in range(sizeB)]
        mulB = [[0]*sizeB for _ in range(sizeB)]
        for i in range(sizeB):
            for j in range(sizeB):
                a_bar, s_bar = B_classes[i][0]
                b_bar, t_bar = B_classes[j][0]
                
                a = R_bar_classes[a_bar][0]
                s = R_bar_classes[s_bar][0]
                b = R_bar_classes[b_bar][0]
                t = R_bar_classes[t_bar][0]
                
                num_add = add_table[mul_table[a][t]][mul_table[b][s]]
                den_add = mul_table[s][t]
                
                num_add_bar = -1
                for k, q_cls in enumerate(R_bar_classes):
                    if num_add in q_cls:
                        num_add_bar = k
                        break
                den_add_bar = -1
                for k, q_cls in enumerate(R_bar_classes):
                    if den_add in q_cls:
                        den_add_bar = k
                        break
                        
                for k, cls in enumerate(B_classes):
                    if (num_add_bar, den_add_bar) in cls:
                        addB[i][j] = k
                        break
                        
                num_mul = mul_table[a][b]
                den_mul = mul_table[s][t]
                
                num_mul_bar = -1
                for k, q_cls in enumerate(R_bar_classes):
                    if num_mul in q_cls:
                        num_mul_bar = k
                        break
                den_mul_bar = -1
                for k, q_cls in enumerate(R_bar_classes):
                    if den_mul in q_cls:
                        den_mul_bar = k
                        break
                        
                for k, cls in enumerate(B_classes):
                    if (num_mul_bar, den_mul_bar) in cls:
                        mulB[i][j] = k
                        break
                        
        # Check if the natural map is an isomorphism
        natural_map = {}
        map_ok = True
        for i in range(sizeA):
            c_A = A_classes[i][0]
            a, s = classes[c_A][0]
            
            a_bar = -1
            for k, q_cls in enumerate(R_bar_classes):
                if a in q_cls:
                    a_bar = k
                    break
            s_bar = -1
            for k, q_cls in enumerate(R_bar_classes):
                if s in q_cls:
                    s_bar = k
                    break
                    
            b_idx = -1
            for k, cls in enumerate(B_classes):
                if (a_bar, s_bar) in cls:
                    b_idx = k
                    break
                    
            if b_idx == -1:
                map_ok = False
                break
            natural_map[i] = b_idx
            
        if map_ok and len(set(natural_map.values())) == sizeA:
            is_homo = True
            for i in range(sizeA):
                for j in range(sizeA):
                    if natural_map[addA[i][j]] != addB[natural_map[i]][natural_map[j]]:
                        is_homo = False
                        break
                    if natural_map[mulA[i][j]] != mulB[natural_map[i]][natural_map[j]]:
                        is_homo = False
                        break
                if not is_homo:
                    break
            if is_homo:
                return True

        if sizeA > 6:
            return False
            
        # Fallback to exhaustive permutation check
        for p in itertools.permutations(range(sizeA)):
            add_ok = True
            for i in range(sizeA):
                for j in range(sizeA):
                    if p[addA[i][j]] != addB[p[i]][p[j]]:
                        add_ok = False
                        break
                if not add_ok:
                    break
            if not add_ok:
                continue
                
            mul_ok = True
            for i in range(sizeA):
                for j in range(sizeA):
                    if p[mulA[i][j]] != mulB[p[i]][p[j]]:
                        mul_ok = False
                        break
                if not mul_ok:
                    break
            if mul_ok:
                return True
                
        return False

    try:
        q_ok = check_conclusion()
    except Exception:
        q_ok = True

    neg_Q = not q_ok

    return [h1_ok, h2_ok, h3_ok, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: I is an ideal of R",
    "¬Q: The ring (S^{-1}R)/(S^{-1}I) is NOT isomorphic to the localized ring \\bar{S}^{-1}(R/I)"
]

N_HYP = 3
NEG_Q_INDEX = 3