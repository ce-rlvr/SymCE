import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint, n_order

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
    "H_1: F_{q^n} is an extension field of degree n over F_q",
    "H_2: alpha is a non-zero element of F_{q^n} with multiplicative order m",
    "¬Q: The smallest positive integer k such that alpha^{q^k} = alpha is NOT equal to the multiplicative order of q modulo m"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # Extract parameters from the witness
    q, n, m, alpha = None, None, None, None
    try:
        if isinstance(witness, tuple):
            if len(witness) >= 4:
                q, n, m, alpha = witness[:4]
            elif len(witness) == 3:
                q, n, m = witness
        elif isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
            m = witness.get('m')
            alpha = witness.get('alpha')
        else:
            q = getattr(witness, 'q', None)
            n = getattr(witness, 'n', None)
            m = getattr(witness, 'm', None)
            alpha = getattr(witness, 'alpha', None)
    except Exception:
        pass

    if q is None or n is None or m is None:
        return [False, False, False]

    # H_1: F_{q^n} is an extension field of degree n over F_q
    try:
        q_int = int(q)
        n_int = int(n)
        factors = factorint(q_int)
        # q must be a prime power (exactly one prime factor) and n >= 1
        h1 = (len(factors) == 1) and (q_int >= 2) and (n_int >= 1)
    except Exception:
        h1 = False

    # H_2: alpha is a non-zero element of F_{q^n} with multiplicative order m
    try:
        m_int = int(m)
        if alpha is not None:
            h2 = False
            if alpha != 0:
                if alpha**m_int == 1:
                    is_order_m = True
                    for i in range(1, m_int):
                        if alpha**i == 1:
                            is_order_m = False
                            break
                    h2 = is_order_m
        else:
            # If alpha is not explicitly provided, check if such an element exists in F_{q^n}
            # An element of order m exists iff m divides q^n - 1
            h2 = (m_int >= 1) and ((q_int**n_int - 1) % m_int == 0)
    except Exception:
        h2 = False

    # ¬Q: The smallest positive integer k such that alpha^{q^k} = alpha is NOT equal to the multiplicative order of q modulo m
    try:
        if alpha is not None:
            k = 1
            while alpha**(q_int**k) != alpha:
                k += 1
                if k > n_int + 100:  # Safety bound
                    break
        else:
            # Implicit alpha of order m: alpha^{q^k} = alpha <=> q^k = 1 mod m
            k = 1
            while (q_int**k) % m_int != 1 % m_int:
                k += 1
                if k > n_int + 100:  # Safety bound
                    break
                    
        try:
            d = n_order(q_int, m_int)
        except ValueError:
            # If n_order raises ValueError (e.g., not coprime or m=1), it is undefined
            d = None
            
        neg_q = (k != d)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]