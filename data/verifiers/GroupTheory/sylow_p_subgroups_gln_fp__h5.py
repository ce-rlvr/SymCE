import sympy
from sympy import Matrix, eye, zeros
from sympy.ntheory import isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def extract_vars(witness):
    p, n, U = None, None, None
    if isinstance(witness, dict):
        p = witness.get('p')
        n = witness.get('n')
        U = witness.get('U')
    elif isinstance(witness, (list, tuple)):
        if len(witness) >= 1:
            p = witness[0]
        if len(witness) >= 2:
            n = witness[1]
        if len(witness) >= 3:
            U = witness[-1]
    return p, n, U

def is_sylow_p_subgroup(p, n, U):
    if not isinstance(U, (list, tuple, set)):
        return False
        
    try:
        p = int(p)
        n = int(n)
        expected_order = p**(n*(n-1)//2)
    except Exception:
        return False
        
    if len(U) != expected_order:
        return False
        
    U_set = set()
    for M in U:
        try:
            if hasattr(M, 'shape') and M.shape == (n, n):
                tup = tuple(tuple(int(x) % p for x in row) for row in M.tolist())
            elif isinstance(M, (list, tuple)) and len(M) == n and all(len(row) == n for row in M):
                tup = tuple(tuple(int(x) % p for x in row) for row in M)
            else:
                return False
            U_set.add(tup)
        except Exception:
            return False
            
    if len(U_set) != expected_order:
        return False
        
    def mul(A, B):
        return tuple(
            tuple(
                sum(A[i][k] * B[k][j] for k in range(n)) % p
                for j in range(n)
            )
            for i in range(n)
        )
        
    I = tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))
    if I not in U_set:
        return False
        
    gens = []
    generated = {I}
    for M in U_set:
        if M not in generated:
            try:
                if Matrix(M).det() % p == 0:
                    return False
            except Exception:
                return False
            gens.append(M)
            queue = [M]
            generated.add(M)
            while queue:
                curr = queue.pop(0)
                for g in gens:
                    for nxt in (mul(curr, g), mul(g, curr)):
                        if nxt not in generated:
                            if nxt not in U_set:
                                return False
                            generated.add(nxt)
                            queue.append(nxt)
                            
    return True

def conditions(witness) -> list[bool]:
    p, n, U = extract_vars(witness)
    
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h2 = False
        
    # H3 and H4 are definitional properties of the objects F_p and G
    # which are uniquely determined by p and n.
    h3 = True
    h4 = True
    
    try:
        neg_q = not is_sylow_p_subgroup(p, n, U)
    except Exception:
        neg_q = True
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: n is a positive integer",
    "H_3: \\mathbb{F}_p is the finite field of p elements",
    "H_4: G is the general linear group GL_n(\\mathbb{F}_p)",
    "¬Q: U is not a Sylow p-subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4