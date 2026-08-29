import sympy
import sympy.combinatorics.named_groups
import sympy.ntheory
from itertools import product
from sympy.matrices import Matrix

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is a positive integer",
    "H_3: GL_n(F) is the general linear group of degree n over F",
    "H_4: SL_n(F) is the special linear group of degree n over F",
    "¬Q: The commutator subgroup of GL_n(F) is NOT SL_n(F)"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            n, q = witness
        else:
            n = witness
            q = 2
            
        n = int(n)
        
        if hasattr(q, 'order'):
            q = int(q.order)
        else:
            q = int(q)
    except Exception:
        return [False, False, False, False, False]
        
    try:
        factors = sympy.ntheory.factorint(q)
        h1 = len(factors) == 1
        is_prime = (sum(factors.values()) == 1)
    except Exception:
        h1 = False
        is_prime = False
        
    try:
        h2 = (n > 0)
    except Exception:
        h2 = False
        
    h3 = True
    h4 = True
    
    neg_q = False
    if h1 and h2 and is_prime:
        try:
            gl_size = 1
            for i in range(n):
                gl_size *= (q**n - q**i)
                
            if gl_size <= 1000:
                GL = []
                SL = []
                for entries in product(range(q), repeat=n*n):
                    M = Matrix(n, n, entries)
                    det = M.det() % q
                    if det != 0:
                        GL.append(M)
                        if det == 1:
                            SL.append(M)
                
                commutators = []
                seen = set()
                for A in GL:
                    A_inv = A.inv_mod(q)
                    for B in GL:
                        B_inv = B.inv_mod(q)
                        C = (A * B * A_inv * B_inv) % q
                        tC = tuple(C)
                        if tC not in seen:
                            seen.add(tC)
                            commutators.append(C)
                
                elements = {tuple(M): M for M in commutators}
                queue = list(commutators)
                while queue:
                    A = queue.pop(0)
                    for B in commutators:
                        C = (A * B) % q
                        tC = tuple(C)
                        if tC not in elements:
                            elements[tC] = C
                            queue.append(C)
                
                SL_set = {tuple(M) for M in SL}
                Comm_set = set(elements.keys())
                
                neg_q = (SL_set != Comm_set)
        except Exception:
            neg_q = False
            
    return [h1, h2, h3, h4, neg_q]