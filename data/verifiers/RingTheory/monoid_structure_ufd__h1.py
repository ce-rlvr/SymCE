import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
Z = sympy.ZZ
Q = sympy.QQ
R = sympy.RR
C = sympy.CC

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

def conditions(witness) -> list[bool]:
    try:
        s = str(witness).lower()
        
        h1_ok = True
        
        domain_keywords = [
            "quaternion", "division ring", "skew field", "weyl", "domain", 
            "field", "integer", "rational", "real", "complex", "z[", "q["
        ]
        exact_matches = ["z", "zz", "q", "qq", "r", "rr", "c", "cc"]
        
        is_domain = False
        if any(w in s for w in domain_keywords) or s in exact_matches:
            is_domain = True
            
        if hasattr(witness, "is_domain") and witness.is_domain:
            is_domain = True
        if hasattr(witness, "is_Field") and witness.is_Field:
            is_domain = True
            
        h2_ok = is_domain
        
        is_ufd = False
        is_rhs_true = False
        
        if any(w in s for w in ["quaternion", "division ring", "skew field"]):
            is_ufd = False
            is_rhs_true = True
        elif any(w in s for w in ["weyl", "free algebra"]):
            is_ufd = False
            is_rhs_true = False
        elif any(w in s for w in ["field", "integer", "rational", "real", "complex"]) or s in exact_matches:
            is_ufd = True
            is_rhs_true = True
        elif hasattr(witness, "is_UFD") and witness.is_UFD:
            is_ufd = True
            is_rhs_true = True
        elif hasattr(witness, "is_Field") and witness.is_Field:
            is_ufd = True
            is_rhs_true = True
            
        q = (is_ufd == is_rhs_true)
        neg_q_ok = not q
        
        return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R^{\\times} is the group of units of R",
    "H_2: R^* is the monoid of non-zero elements of R under multiplication",
    "¬Q: R is a Unique Factorization Domain if and only if R^* is isomorphic to the direct product of R^{\\times} and a free commutative monoid fails"
]

N_HYP = 2
NEG_Q_INDEX = 2