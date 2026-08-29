import sympy
from sympy import Matrix, eye, zeros, BlockMatrix, Poly, Rational, Integer
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        K_mult = witness['K_mult']
        G_K = witness['G_K']
        V_K = witness['V_K']
        G_V = witness['G_V']
        
        n = len(K_mult)
        d = len(V_K[0])
        
        if n == 0 or d == 0:
            return [False, False, False]
            
        h1 = True
        # H1: K/F is a finite Galois extension with Galois group G
        if K_mult[0] != eye(n): 
            h1 = False
            
        for i in range(n):
            for j in range(n):
                expected = zeros(n, n)
                for k in range(n):
                    expected += K_mult[i][k, j] * K_mult[k]
                if K_mult[i] * K_mult[j] != expected: 
                    h1 = False
                if K_mult[i] * K_mult[j] != K_mult[j] * K_mult[i]: 
                    h1 = False
                
        if len(G_K) != n: 
            h1 = False
        if len(set(tuple(g) for g in G_K)) != n: 
            h1 = False
        
        for i in range(n):
            for j in range(n):
                if G_K[i] * G_K[j] not in G_K:
                    h1 = False
                    
        for g in G_K:
            if g.det() == 0: 
                h1 = False
            for i in range(n):
                g_ei = g[:, i]
                K_g_ei = zeros(n, n)
                for k in range(n):
                    K_g_ei += g[k, i] * K_mult[k]
                if g * K_mult[i] != K_g_ei * g: 
                    h1 = False
            if g * Matrix([1] + [0]*(n-1)) != Matrix([1] + [0]*(n-1)): 
                h1 = False
            
        eqs = [g - eye(n) for g in G_K]
        if Matrix.vstack(*eqs).rank() != n - 1: 
            h1 = False
        
        is_f = False
        if n == 1:
            is_f = True
        else:
            for i in range(1, n):
                p = Poly(K_mult[i].charpoly(x).as_expr(), x)
                if p.is_irreducible:
                    is_f = True
                    break
            if not is_f:
                for i in range(1, n):
                    for j in range(i+1, n):
                        M = K_mult[i] + K_mult[j]
                        p = Poly(M.charpoly(x).as_expr(), x)
                        if p.is_irreducible:
                            is_f = True
                            break
        if not is_f: 
            h1 = False
        
        h2 = True
        # H2: V is a K-vector space
        if len(V_K) != n: 
            h2 = False
        if V_K[0] != eye(d): 
            h2 = False
        for i in range(n):
            for j in range(n):
                expected = zeros(d, d)
                for k in range(n):
                    expected += K_mult[i][k, j] * V_K[k]
                if V_K[i] * V_K[j] != expected: 
                    h2 = False
                
        if len(G_V) != n: 
            h2 = False
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if G_K[i] * G_K[j] == G_K[k]:
                        if G_V[i] * G_V[j] != G_V[k]: 
                            h2 = False
        
        id_idx = -1
        for i in range(n):
            if G_K[i] == eye(n):
                id_idx = i
                break
        if id_idx == -1 or G_V[id_idx] != eye(d): 
            h2 = False
        
        # Conclusion: V^G is an F-vector space, and V^G \otimes_F K -> V is an isomorphism
        eqs_V = [g - eye(d) for g in G_V]
        M_V = Matrix.vstack(*eqs_V)
        nullspace = M_V.nullspace()
        D = len(nullspace)
        
        images = []
        for u in nullspace:
            for j in range(n):
                images.append(V_K[j] * u)
                
        if len(images) == 0:
            rank = 0
        else:
            Image_Matrix = Matrix.hstack(*images)
            rank = Image_Matrix.rank()
            
        is_iso = (D * n == d) and (rank == d)
        neg_q = not is_iso
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K/F is a finite Galois extension with Galois group G",
    "H_2: V is a K-vector space",
    "¬Q: V^G is not an F-vector space, or V^G \\otimes_F K \\to V is not an isomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2