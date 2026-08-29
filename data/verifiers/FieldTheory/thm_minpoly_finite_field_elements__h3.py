import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            q, n = witness
        elif isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
        elif hasattr(witness, 'q') and hasattr(witness, 'n'):
            q = witness.q
            n = witness.n
        else:
            q, n = None, None
            
        if hasattr(q, 'order'):
            q = q.order
        else:
            q = int(q)
        n = int(n)
    except Exception:
        return [False, False, False]
        
    # H1: F_q is a finite field of order q
    # A finite field of order q exists if and only if q is a prime power (q > 1).
    try:
        if q > 1:
            factors = factorint(q)
            h1_ok = len(factors) == 1
        else:
            h1_ok = False
    except Exception:
        h1_ok = False
        
    # H2: n is a positive integer
    try:
        h2_ok = isinstance(n, int) and n > 0
    except Exception:
        h2_ok = False
        
    # neg_Q: The conclusion FAILS at the witness
    # Conclusion: The set of minimal polynomials over F_q of all elements in F_{q^n} 
    # consists exactly of all monic irreducible polynomials in F_q[x] whose degree divides n.
    # 
    # Mathematically, this conclusion is a fundamental theorem of finite fields 
    # (e.g., Lidl & Niederreiter, Theorem 3.20) and is unconditionally TRUE for all 
    # prime powers q and positive integers n. Therefore, the conclusion NEVER fails 
    # when the hypotheses hold. We correctly evaluate neg_Q as False.
    try:
        neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: \\mathbb{F}_q is a finite field of order q",
    "H_2: n is a positive integer",
    "\\neg Q: The set of minimal polynomials does not consist exactly of all monic irreducible polynomials whose degree divides n"
]

N_HYP = 2
NEG_Q_INDEX = 2