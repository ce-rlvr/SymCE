import itertools
import functools
import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    H1: R is a Boolean ring
    neg_Q: L does not form a distributive lattice under ideal addition and ideal intersection
    """
    try:
        if hasattr(witness, 'elements'):
            R = list(witness.elements)
        else:
            R = list(witness)
        N = len(R)
        if N == 0:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        # Determine addition and multiplication functions
        if hasattr(witness, 'add') and hasattr(witness, 'mul'):
            def add(a, b): return witness.add(a, b)
            def mul(a, b): return witness.mul(a, b)
        else:
            def add(a, b): return a + b
            def mul(a, b): return a * b
            
        # Build addition and multiplication tables
        add_table = [[0] * N for _ in range(N)]
        mul_table = [[0] * N for _ in range(N)]
        
        for i in range(N):
            for j in range(N):
                s = add(R[i], R[j])
                p = mul(R[i], R[j])
                
                s_idx = -1
                for k in range(N):
                    try:
                        if R[k] == s:
                            s_idx = k
                            break
                    except Exception:
                        pass
                if s_idx == -1:
                    return [False, False]
                    
                p_idx = -1
                for k in range(N):
                    try:
                        if R[k] == p:
                            p_idx = k
                            break
                    except Exception:
                        pass
                if p_idx == -1:
                    return [False, False]
                    
                add_table[i][j] = s_idx
                mul_table[i][j] = p_idx
    except Exception:
        return [False, False]

    try:
        # 1. Commutativity of addition
        for i in range(N):
            for j in range(N):
                if add_table[i][j] != add_table[j][i]:
                    return [False, False]
                    
        # 2. Associativity of addition
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]:
                        return [False, False]
                        
        # 3. Zero element
        zero_idx = -1
        for i in range(N):
            is_zero = True
            for j in range(N):
                if add_table[i][j] != j:
                    is_zero = False
                    break
            if is_zero:
                zero_idx = i
                break
        if zero_idx == -1:
            return [False, False]
            
        # 4. Additive inverses
        neg_table = [-1] * N
        for i in range(N):
            for j in range(N):
                if add_table[i][j] == zero_idx:
                    neg_table[i] = j
                    break
            if neg_table[i] == -1:
                return [False, False]
                
        # 5. Associativity of multiplication
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]:
                        return [False, False]
                        
        # 6. Distributivity
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                        return [False, False]
                    if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]:
                        return [False, False]
                        
        # 7. Boolean ring: x^2 = x
        for i in range(N):
            if mul_table[i][i] != i:
                return [False, False]
                
        h1_ok = True
    except Exception:
        return [False, False]

    try:
        # In a finite Boolean ring, every ideal is principal.
        # We compute all principal ideals to form the lattice L.
        ideals = set()
        for i in range(N):
            ideal = set()
            for r in range(N):
                rx = mul_table[r][i]
                ideal.add(rx)
                ideal.add(add_table[rx][i])
            ideals.add(frozenset(ideal))
        
        # Safety net: explicitly add the full ring as an ideal
        ideals.add(frozenset(range(N)))
            
        L = list(ideals)
        num_ideals = len(L)
        
        # Map ideals to bitmasks for fast operations
        L_masks = []
        for I in L:
            mask = 0
            for x in I:
                mask |= (1 << x)
            L_masks.append(mask)
            
        mask_to_idx = {mask: idx for idx, mask in enumerate(L_masks)}
        L_sizes = [len(I) for I in L]
        
        # Precompute ideal addition table
        # I + J is the smallest ideal containing both I and J
        ideal_add_table = [[0] * num_ideals for _ in range(num_ideals)]
        for i in range(num_ideals):
            for j in range(num_ideals):
                target_mask = L_masks[i] | L_masks[j]
                best_idx = -1
                best_size = N + 1
                for k in range(num_ideals):
                    if (L_masks[k] & target_mask) == target_mask:
                        if L_sizes[k] < best_size:
                            best_size = L_sizes[k]
                            best_idx = k
                ideal_add_table[i][j] = best_idx
                
        # Check distributivity: I & (J + K) == (I & J) + (I & K)
        is_distributive = True
        for i in range(num_ideals):
            mask_i = L_masks[i]
            for j in range(num_ideals):
                mask_j = L_masks[j]
                i_int_j_mask = mask_i & mask_j
                i_int_j_idx = mask_to_idx.get(i_int_j_mask, -1)
                
                for k in range(num_ideals):
                    j_plus_k = ideal_add_table[j][k]
                    lhs_mask = mask_i & L_masks[j_plus_k]
                    
                    i_int_k_mask = mask_i & L_masks[k]
                    i_int_k_idx = mask_to_idx.get(i_int_k_mask, -1)
                    
                    if i_int_j_idx != -1 and i_int_k_idx != -1:
                        rhs_mask = L_masks[ideal_add_table[i_int_j_idx][i_int_k_idx]]
                    else:
                        rhs_mask = -1
                        
                    if lhs_mask != rhs_mask:
                        is_distributive = False
                        break
                if not is_distributive:
                    break
            if not is_distributive:
                break
                
        neg_q = not is_distributive
        
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: Let R be a Boolean ring",
    "¬Q: L does not form a distributive lattice under ideal addition and ideal intersection"
]

N_HYP = 1
NEG_Q_INDEX = 1