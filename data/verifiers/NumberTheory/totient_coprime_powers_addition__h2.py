import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def conditions(witness):
    try:
        m, n = witness
    except Exception:
        return [False, False, False]
        
    # H1: m is a positive integer
    try:
        m_sym = sympy.S(m)
        h1 = bool(m_sym.is_integer and m_sym > 0)
    except Exception:
        h1 = False
        
    # H2: \gcd(m, n) = 1
    try:
        h2 = bool(sympy.gcd(m, n) == 1)
    except Exception:
        h2 = False
        
    # neg_Q: m^{\phi(n)} + n^{\phi(m)} \not\equiv 1 \pmod{mn}
    try:
        m_sym = sympy.S(m)
        n_sym = sympy.S(n)
        
        # Euler's totient function phi(x) is mathematically defined only for positive integers.
        # If n is not a positive integer, the expression is undefined, making the conclusion false.
        if not (m_sym.is_integer and m_sym > 0 and n_sym.is_integer and n_sym > 0):
            q_ok = False
        else:
            m_int = int(m)
            n_int = int(n)
            mod = m_int * n_int
            
            # Use modular exponentiation for performance and to avoid huge numbers
            term1 = pow(m_int, int(sympy.totient(n_int)), mod)
            term2 = pow(n_int, int(sympy.totient(m_int)), mod)
            
            q_ok = ((term1 + term2 - 1) % mod == 0)
            
        neg_q = not q_ok
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: gcd(m, n) == 1",
    "¬Q: m^phi(n) + n^phi(m) != 1 mod mn"
]

N_HYP = 2
NEG_Q_INDEX = 2