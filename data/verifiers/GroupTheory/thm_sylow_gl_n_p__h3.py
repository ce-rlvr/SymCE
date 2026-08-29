import sympy
from sympy import isprime
from sympy.ntheory import factorint
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    # Parse witness
    p = n = q = G = U = None
    if isinstance(witness, dict):
        p = witness.get('p')
        n = witness.get('n')
        q = witness.get('q')
        G = witness.get('G')
        U = witness.get('U')
    elif isinstance(witness, (tuple, list)):
        if len(witness) >= 1: p = witness[0]
        if len(witness) >= 2: n = witness[1]
        if len(witness) == 3:
            if isinstance(witness[2], int):
                q = witness[2]
            else:
                G = witness[2]
        elif len(witness) >= 4:
            G = witness[2]
            U = witness[3]
            if len(witness) >= 5:
                q = witness[4]

    # Try to extract n and q from a string like "GL(2, 3)"
    if q is None and isinstance(G, str):
        s = G.replace("GL", "").replace("(", "").replace(")", "").replace(" ", "")
        parts = s.split(",")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            parsed_n = int(parts[0])
            if n is None or parsed_n == n:
                n = parsed_n
                q = int(parts[1])

    # Try to deduce q from the order of G
    if q is None and isinstance(G, int) and isinstance(n, int) and n > 0:
        for test_q in range(2, 1000):
            expected_G = 1
            for i in range(n):
                expected_G *= (test_q**n - test_q**i)
            if expected_G == G:
                q = test_q
                break

    # Compute expected orders
    G_order = None
    U_order = None
    if q is not None and isinstance(n, int) and n > 0:
        G_order = 1
        for i in range(n):
            G_order *= (q**n - q**i)
        U_order = q**(n*(n-1)//2)
    else:
        if isinstance(G, int): G_order = G
        if isinstance(U, int): U_order = U

    # H_1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # H_2: n is a positive integer
    try:
        h2_ok = isinstance(n, int) and n > 0
    except Exception:
        h2_ok = False

    # H_3: U is the subgroup of G consisting of all upper unitriangular matrices
    try:
        h3_ok = False
        if q is not None:
            factors = factorint(q)
            # q must be a prime power for GL(n, q) to be well-defined
            if len(factors) == 1 and q >= 2:
                h3_ok = True
                if isinstance(G, int) and G != G_order: h3_ok = False
                if isinstance(U, int) and U != U_order: h3_ok = False
    except Exception:
        h3_ok = False

    # ¬Q: U is not a Sylow p-subgroup of G
    try:
        def count_p_factor(num, p_val):
            if num == 0 or p_val <= 1: return 0
            c = 0
            while num % p_val == 0:
                c += 1
                num //= p_val
            return c
            
        if U_order == 1:
            is_p_group = True
        else:
            factors = factorint(U_order)
            is_p_group = (list(factors.keys()) == [p])
            
        max_p_power = p ** count_p_factor(G_order, p)
        
        is_sylow = is_p_group and (U_order == max_p_power)
        neg_q_ok = not is_sylow
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: n is a positive integer",
    "H_3: U is the subgroup of G consisting of all upper unitriangular matrices",
    "¬Q: U is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3