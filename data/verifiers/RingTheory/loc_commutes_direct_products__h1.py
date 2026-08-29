import itertools
import math
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Matrix, eye, zeros

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is the direct product R_1 \\times ... \\times R_n",
    "H_2: S_i is a multiplicatively closed subset of R_i for each i",
    "H_3: S is the direct product S_1 \\times ... \\times S_n",
    "¬Q: The localized ring S^{-1}R is not isomorphic to the direct product S_1^{-1}R_1 \\times ... \\times S_n^{-1}R_n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_ring(N, add, mul):
    if N <= 0: return False
    if len(add) != N or len(mul) != N: return False
    for row in add:
        if len(row) != N: return False
    for row in mul:
        if len(row) != N: return False
        
    for a in range(N):
        for b in range(N):
            if not (0 <= add[a][b] < N): return False
            if not (0 <= mul[a][b] < N): return False
            
    for a in range(N):
        for b in range(N):
            if add[a][b] != add[b][a]: return False
            
    for a in range(N):
        for b in range(N):
            for c in range(N):
                if add[add[a][b]][c] != add[a][add[b][c]]: return False
                
    zero = None
    for i in range(N):
        if all(add[i][j] == j for j in range(N)):
            zero = i
            break
    if zero is None: return False
    
    for a in range(N):
        if not any(add[a][b] == zero for b in range(N)): return False
        
    for a in range(N):
        for b in range(N):
            for c in range(N):
                if mul[mul[a][b]][c] != mul[a][mul[b][c]]: return False
                
    for a in range(N):
        for b in range(N):
            for c in range(N):
                if mul[a][add[b][c]] != add[mul[a][b]][mul[a][c]]: return False
                if mul[add[a][b]][c] != add[mul[a][c]][mul[b][c]]: return False
                
    one = None
    for i in range(N):
        if all(mul[i][j] == j and mul[j][i] == j for j in range(N)):
            one = i
            break
    if one is None: return False
    
    return True

def is_right_ore_set(N, add, mul, S):
    if not S: return False
    
    zero = None
    for i in range(N):
        if all(add[i][j] == j for j in range(N)):
            zero = i
            break
    if zero is None: return False
            
    for r in range(N):
        for s in S:
            found = False
            for r_prime in range(N):
                for s_prime in S:
                    if mul[r][s_prime] == mul[s][r_prime]:
                        found = True
                        break
                if found: break
            if not found:
                return False
                
    for r in range(N):
        has_left_annihilator = False
        for s in S:
            if mul[s][r] == zero:
                has_left_annihilator = True
                break
        if has_left_annihilator:
            has_right_annihilator = False
            for s_prime in S:
                if mul[r][s_prime] == zero:
                    has_right_annihilator = True
                    break
            if not has_right_annihilator:
                return False
                
    return True

def is_left_ore_set(N, add, mul, S):
    if not S: return False
    
    zero = None
    for i in range(N):
        if all(add[i][j] == j for j in range(N)):
            zero = i
            break
    if zero is None: return False
            
    for r in range(N):
        for s in S:
            found = False
            for r_prime in range(N):
                for s_prime in S:
                    if mul[s_prime][r] == mul[r_prime][s]:
                        found = True
                        break
                if found: break
            if not found:
                return False
                
    for r in range(N):
        has_right_annihilator = False
        for s in S:
            if mul[r][s] == zero:
                has_right_annihilator = True
                break
        if has_right_annihilator:
            has_left_annihilator = False
            for s_prime in S:
                if mul[s_prime][r] == zero:
                    has_left_annihilator = True
                    break
            if not has_left_annihilator:
                return False
                
    return True

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        R_i_list = witness.get('R_i', [])
        S_i_list = witness.get('S_i', [])
        R = witness.get('R', (0, [], []))
        S = witness.get('S', [])
        mapping = witness.get('map_to_components', [])
        n = len(R_i_list)
    except Exception:
        return [False, False, False, False]
        
    try:
        if n >= 1:
            h1 = True
            N_R, add_R, mul_R = R
            if not is_ring(N_R, add_R, mul_R):
                h1 = False
            for N_i, add_i, mul_i in R_i_list:
                if not is_ring(N_i, add_i, mul_i):
                    h1 = False
            if h1:
                if len(mapping) != N_R:
                    h1 = False
                else:
                    mapped_elements = set(tuple(m) for m in mapping)
                    expected_size = 1
                    for N_i, _, _ in R_i_list:
                        expected_size *= N_i
                    if N_R != expected_size or len(mapped_elements) != N_R:
                        h1 = False
                    if h1:
                        for x in range(N_R):
                            for y in range(N_R):
                                sum_xy = add_R[x][y]
                                prod_xy = mul_R[x][y]
                                map_x = mapping[x]
                                map_y = mapping[y]
                                map_sum = mapping[sum_xy]
                                map_prod = mapping[prod_xy]
                                for i in range(n):
                                    _, add_i, mul_i = R_i_list[i]
                                    if map_sum[i] != add_i[map_x[i]][map_y[i]]:
                                        h1 = False
                                    if map_prod[i] != mul_i[map_x[i]][map_y[i]]:
                                        h1 = False
    except Exception:
        h1 = False

    try:
        if n >= 1:
            h2 = True
            for i in range(n):
                N_i, _, mul_i = R_i_list[i]
                S_i = S_i_list[i]
                if not S_i:
                    h2 = False
                elif not all(0 <= s < N_i for s in S_i):
                    h2 = False
                else:
                    for a in S_i:
                        for b in S_i:
                            if mul_i[a][b] not in S_i:
                                h2 = False
                    one = None
                    for e in range(N_i):
                        if all(mul_i[e][j] == j and mul_i[j][e] == j for j in range(N_i)):
                            one = e
                            break
                    if one is None or one not in S_i:
                        h2 = False
    except Exception:
        h2 = False

    try:
        if n >= 1:
            h3 = True
            N_R = R[0]
            if not all(0 <= s < N_R for s in S):
                h3 = False
            else:
                S_mapped = set(tuple(mapping[s]) for s in S)
                expected_S_mapped = set(itertools.product(*S_i_list))
                if S_mapped != expected_S_mapped:
                    h3 = False
    except Exception:
        h3 = False

    try:
        N_R, add_R, mul_R = R
        if is_ring(N_R, add_R, mul_R) and all(0 <= s < N_R for s in S):
            right_ore = is_right_ore_set(N_R, add_R, mul_R, S)
            left_ore = is_left_ore_set(N_R, add_R, mul_R, S)
            # If S is neither a right nor a left Ore set, the ring of fractions does not exist,
            # so it cannot be isomorphic to the direct product of localizations.
            neg_q = not right_ore and not left_ore
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]