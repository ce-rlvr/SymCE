import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    "H_1: G is the Heisenberg group consisting of 3x3 upper triangular matrices with 1s on the main diagonal and entries from F",
    "¬Q: The center Z(G) does not consist exactly of those matrices in G whose only non-zero off-diagonal entry is in the top-right corner"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        G = witness
        if not isinstance(G, (list, tuple, set)):
            G = list(G)
    except Exception:
        return [False, False]

    try:
        if len(G) == 0:
            return [False, False]
        
        def get_entry(M, i, j):
            try:
                return M[i, j]
            except Exception:
                return M[i][j]

        one = get_entry(G[0], 0, 0)
        zero = get_entry(G[0], 1, 0)
        
        def contains(lst, item):
            for x in lst:
                if x == item:
                    return True
            return False

        h1_ok = True
        F_elements = []
        for M in G:
            for i in range(3):
                if get_entry(M, i, i) != one:
                    h1_ok = False; break
                for j in range(i):
                    if get_entry(M, i, j) != zero:
                        h1_ok = False; break
                for j in range(i+1, 3):
                    val = get_entry(M, i, j)
                    if not contains(F_elements, val):
                        F_elements.append(val)
            if not h1_ok:
                break
                
        if not h1_ok:
            return [False, False]
            
        if not contains(F_elements, one):
            F_elements.append(one)
        if not contains(F_elements, zero):
            F_elements.append(zero)
            
        for a in F_elements:
            if (a + zero) != a or (zero + a) != a:
                h1_ok = False; break
            if (a * one) != a or (one * a) != a:
                h1_ok = False; break
            if (a * zero) != zero or (zero * a) != zero:
                h1_ok = False; break
            
            has_inv = False
            for b in F_elements:
                if (a + b) == zero and (b + a) == zero:
                    has_inv = True
                    break
            if not has_inv:
                h1_ok = False; break
                
            for b in F_elements:
                if not contains(F_elements, a + b):
                    h1_ok = False; break
                if not contains(F_elements, a * b):
                    h1_ok = False; break
            if not h1_ok:
                break
                
        if not h1_ok:
            return [False, False]

        def contains_tup(lst, tup):
            for x in lst:
                if x[0] == tup[0] and x[1] == tup[1] and x[2] == tup[2]:
                    return True
            return False

        unique_G = []
        for M in G:
            tup = (get_entry(M, 0, 1), get_entry(M, 1, 2), get_entry(M, 0, 2))
            if not contains_tup(unique_G, tup):
                unique_G.append(tup)
                
        if len(unique_G) != len(F_elements)**3 or len(G) != len(F_elements)**3:
            h1_ok = False

    except Exception:
        h1_ok = False

    try:
        neg_q = False
        if h1_ok:
            def mul_tup(A, B):
                try:
                    C = A * B
                    return (get_entry(C, 0, 1), get_entry(C, 1, 2), get_entry(C, 0, 2))
                except Exception:
                    a01 = get_entry(A, 0, 1)
                    a12 = get_entry(A, 1, 2)
                    a02 = get_entry(A, 0, 2)
                    
                    b01 = get_entry(B, 0, 1)
                    b12 = get_entry(B, 1, 2)
                    b02 = get_entry(B, 0, 2)
                    
                    c01 = a01 + b01
                    c12 = a12 + b12
                    c02 = a02 + a01 * b12 + b02
                    return (c01, c12, c02)

            for A in G:
                is_center = True
                for B in G:
                    c_AB = mul_tup(A, B)
                    c_BA = mul_tup(B, A)
                    if c_AB[0] != c_BA[0] or c_AB[1] != c_BA[1] or c_AB[2] != c_BA[2]:
                        is_center = False
                        break
                
                a01 = get_entry(A, 0, 1)
                a12 = get_entry(A, 1, 2)
                expected_center = (a01 == zero and a12 == zero)
                
                if is_center != expected_center:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]