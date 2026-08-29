import sympy
from sympy import Matrix, eye
import itertools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory.factor_ import factorint

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: G is the group of all invertible n by n upper triangular matrices with entries in F",
    "¬Q: G is not solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_mod_val(x, q):
    try:
        return int(x) % q
    except Exception:
        if hasattr(x, 'val'):
            return int(x.val) % q
        return int(x % q)

def conditions(witness):
    F = None
    n = None
    G = None
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, n, G = witness
            elif len(witness) == 2:
                F, G = witness
                if isinstance(G, list) and len(G) > 0:
                    n = G[0].shape[0]
                elif hasattr(G, 'degree'):
                    n = G.degree
        else:
            G = witness
            if isinstance(G, list) and len(G) > 0:
                n = G[0].shape[0]
            elif hasattr(G, 'degree'):
                n = G.degree
    except Exception:
        pass

    q = None
    try:
        if hasattr(F, 'order'):
            q = F.order
        elif isinstance(F, int):
            q = F
        elif F is not None:
            q = int(F)
    except Exception:
        pass

    # H1: F is a field
    h1 = False
    try:
        if hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif hasattr(F, 'is_field') and F.is_field:
            h1 = True
        elif F in [sympy.QQ, sympy.RR, sympy.CC]:
            h1 = True
        elif q is not None:
            factors = factorint(q)
            if len(factors) == 1:
                h1 = True
    except Exception:
        pass

    # H2: G is the group of all invertible n by n upper triangular matrices with entries in F
    h2 = False
    try:
        if isinstance(G, list) and q is not None and n is not None:
            is_upper = True
            for M in G:
                if M.shape != (n, n):
                    is_upper = False
                    break
                for i in range(n):
                    for j in range(i):
                        if get_mod_val(M[i, j], q) != 0:
                            is_upper = False
                            break
                if get_mod_val(M.det(), q) == 0:
                    is_upper = False
                    break
            
            if is_upper:
                expected_size = (q - 1)**n * q**(n*(n-1)//2)
                if len(G) == expected_size:
                    h2 = True
        elif hasattr(G, 'generators') and q is not None and n is not None:
            is_upper = True
            for M in G.generators:
                if M.shape != (n, n):
                    is_upper = False
                    break
                for i in range(n):
                    for j in range(i):
                        if get_mod_val(M[i, j], q) != 0:
                            is_upper = False
                            break
                if get_mod_val(M.det(), q) == 0:
                    is_upper = False
                    break
            if is_upper:
                expected_size = (q - 1)**n * q**(n*(n-1)//2)
                if hasattr(G, 'order') and G.order() == expected_size:
                    h2 = True
    except Exception:
        pass

    # neg_Q: G is not solvable
    neg_q = False
    try:
        if hasattr(G, 'is_solvable'):
            neg_q = not G.is_solvable
        elif isinstance(G, list) and q is not None and n is not None:
            if q**n <= 2000:
                elements = list(range(q))
                vectors = list(itertools.product(elements, repeat=n))
                vector_to_idx = {v: i for i, v in enumerate(vectors)}
                
                perms = []
                for M in G:
                    p = []
                    for v in vectors:
                        v_mat = Matrix(n, 1, v)
                        Mv = M * v_mat
                        Mv_tuple = tuple(get_mod_val(x, q) for x in Mv)
                        p.append(vector_to_idx[Mv_tuple])
                    perms.append(Permutation(p))
                    
                P = PermutationGroup(perms)
                neg_q = not P.is_solvable
        elif hasattr(G, 'generators') and q is not None and n is not None:
            if q**n <= 2000:
                elements = list(range(q))
                vectors = list(itertools.product(elements, repeat=n))
                vector_to_idx = {v: i for i, v in enumerate(vectors)}
                
                perms = []
                for M in G.generators:
                    p = []
                    for v in vectors:
                        v_mat = Matrix(n, 1, v)
                        Mv = M * v_mat
                        Mv_tuple = tuple(get_mod_val(x, q) for x in Mv)
                        p.append(vector_to_idx[Mv_tuple])
                    perms.append(Permutation(p))
                    
                P = PermutationGroup(perms)
                neg_q = not P.is_solvable
    except Exception:
        pass

    return [h1, h2, neg_q]