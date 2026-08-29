import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def get_order(obj):
    if isinstance(obj, (int, sympy.Integer)):
        return int(obj)
    if hasattr(obj, 'order'):
        if callable(obj.order):
            return int(obj.order())
        return int(obj.order)
    if isinstance(obj, (list, tuple, set)):
        return len(obj)
    raise ValueError("Cannot determine order")

def is_upper_unitriangular(M, p):
    n = M.rows
    if M.cols != n: 
        return False
    for i in range(n):
        for j in range(n):
            val = M[i, j] % p
            if i == j:
                if val != 1: 
                    return False
            elif i > j:
                if val != 0: 
                    return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            n = witness.get('n')
            G = witness.get('G', None)
            U = witness.get('U', None)
        elif isinstance(witness, (list, tuple)):
            if len(witness) >= 2:
                p = witness[0]
                n = witness[1]
                G = witness[2] if len(witness) > 2 else None
                U = witness[3] if len(witness) > 3 else None
            else:
                return [False] * 5
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H2: n is a positive integer
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h2 = False

    g_order = None
    u_order = None

    # H3: G is the general linear group GL_n(\mathbb{F}_p)
    try:
        if h1 and h2:
            expected_G_order = 1
            for i in range(n):
                expected_G_order *= (p**n - p**i)
            
            if G is None:
                h3 = True
                g_order = expected_G_order
            else:
                g_order = get_order(G)
                h3 = (g_order == expected_G_order)
                
                if h3 and isinstance(G, (list, tuple, set)):
                    for M in G:
                        if hasattr(M, 'det'):
                            if M.det() % p == 0:
                                h3 = False
                                break
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: U is the subgroup of G consisting of all upper unitriangular matrices
    try:
        if h1 and h2:
            expected_U_order = p**(n*(n-1)//2)
            if U is None:
                h4 = True
                u_order = expected_U_order
            else:
                u_order = get_order(U)
                h4 = (u_order == expected_U_order)
                
                if h4 and isinstance(U, (list, tuple, set)):
                    for M in U:
                        if hasattr(M, 'rows'):
                            if not is_upper_unitriangular(M, p):
                                h4 = False
                                break
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: U is NOT a Sylow p-subgroup of G
    try:
        if h1 and h2 and g_order is not None and u_order is not None:
            temp = u_order
            if temp < 1:
                is_sylow = False
            else:
                while temp % p == 0 and temp > 1:
                    temp //= p
                is_p_group = (temp == 1)
                
                divides = (g_order % u_order == 0)
                if u_order > 0:
                    index_coprime = ((g_order // u_order) % p != 0)
                else:
                    index_coprime = False
                
                is_sylow = is_p_group and divides and index_coprime
            neg_q = not is_sylow
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: n is a positive integer",
    "H_3: G is the general linear group GL_n(\\mathbb{F}_p)",
    "H_4: U is the subgroup of G consisting of all upper unitriangular matrices",
    "¬Q: U is not a Sylow p-subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4