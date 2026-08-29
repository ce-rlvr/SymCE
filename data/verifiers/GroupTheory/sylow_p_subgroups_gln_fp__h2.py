import sympy
import sympy.combinatorics.named_groups
import sympy.matrices

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: F_p is the finite field of p elements",
    "H_3: G is the general linear group GL_n(F_p)",
    "H_4: U is the subgroup of G consisting of all upper unitriangular matrices",
    "¬Q: U is not a Sylow p-subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        p, n, G, U = witness
    except Exception:
        return [False] * 5
        
    # H1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    # H2: F_p is the finite field of p elements
    # This is a definitional hypothesis. If p is prime, F_p exists.
    h2 = h1
    
    # H3: G is the general linear group GL_n(F_p)
    try:
        if not h1 or n < 0:
            h3 = False
        else:
            expected_size = 1
            for i in range(n):
                expected_size *= (p**n - p**i)
            
            unique_G = []
            h3_valid = True
            for M in G:
                try:
                    mat = sympy.Matrix(M) if not isinstance(M, sympy.Matrix) else M
                    if mat.shape != (n, n):
                        h3_valid = False
                        break
                    if n > 0 and int(mat.det()) % p == 0:
                        h3_valid = False
                        break
                    mat_mod_p = mat.applyfunc(lambda x: x % p)
                    tup = tuple(mat_mod_p)
                    if tup not in unique_G:
                        unique_G.append(tup)
                except Exception:
                    h3_valid = False
                    break
            
            if h3_valid and len(unique_G) == expected_size and len(G) == expected_size:
                h3 = True
            else:
                h3 = False
    except Exception:
        h3 = False
        
    # H4: U is the subgroup of G consisting of all upper unitriangular matrices
    try:
        if not h1 or n < 0:
            h4 = False
        else:
            expected_u_size = p**(n*(n-1)//2) if n >= 1 else 1
            
            unique_U = []
            h4_valid = True
            for M in U:
                try:
                    mat = sympy.Matrix(M) if not isinstance(M, sympy.Matrix) else M
                    if mat.shape != (n, n):
                        h4_valid = False
                        break
                    mat_mod_p = mat.applyfunc(lambda x: x % p)
                    for i in range(n):
                        for j in range(n):
                            val = mat_mod_p[i, j]
                            if i == j:
                                if val != 1:
                                    h4_valid = False
                                    break
                            elif i > j:
                                if val != 0:
                                    h4_valid = False
                                    break
                        if not h4_valid: break
                    if not h4_valid: break
                    
                    tup = tuple(mat_mod_p)
                    if tup not in unique_U:
                        unique_U.append(tup)
                except Exception:
                    h4_valid = False
                    break
                    
            if h4_valid and len(unique_U) == expected_u_size and len(U) == expected_u_size:
                h4 = True
            else:
                h4 = False
    except Exception:
        h4 = False
        
    # neg_Q: U is NOT a Sylow p-subgroup of G
    try:
        order_G = len(G)
        order_U = len(U)
        
        is_p_group = True
        temp = order_U
        while temp > 1:
            if temp % p != 0:
                is_p_group = False
                break
            temp //= p
            
        if order_U == 1:
            is_p_group = True
            
        if order_G % order_U != 0:
            is_sylow = False
        else:
            index = order_G // order_U
            # Under the strict definition, a Sylow p-subgroup only exists if p divides |G|.
            # If p does not divide |G|, the group has no Sylow p-subgroups.
            is_sylow = is_p_group and (index % p != 0) and (order_G % p == 0)
            
        neg_q = not is_sylow
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]