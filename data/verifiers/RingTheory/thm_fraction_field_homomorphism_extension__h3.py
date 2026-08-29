import sympy
from sympy import ZZ, QQ
from sympy.polys.domains import Domain
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard algebra objects
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis was that f: R -> S is an injective ring homomorphism.
    """
    try:
        R = witness['R']
        S = witness['S']
        K = witness['K']
        L = witness['L']
        f = witness['f']
        if not callable(f):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R and S are integral domains
    try:
        # In SymPy, ZZ, QQ, etc. are instances of Domain (which are integral domains)
        h1 = isinstance(R, Domain) and isinstance(S, Domain)
    except Exception:
        h1 = False

    # H_2: K and L are fields of fractions of R and S, respectively
    try:
        h2 = (K == R.get_field()) and (L == S.get_field())
    except Exception:
        h2 = False

    # ¬Q: There does not exist a unique injective ring homomorphism \tilde{f}: K \to L 
    # such that \tilde{f}(a/1) = f(a)/1 for all a \in R.
    # By the universal property of fields of fractions, such \tilde{f} exists, is unique, 
    # and is injective IF AND ONLY IF f is an injective ring homomorphism.
    # Therefore, the conclusion fails exactly when f is NOT an injective ring homomorphism.
    try:
        test_ints = [-2, -1, 0, 1, 2]
        test_elems = [R(x) for x in test_ints]
        
        is_homo = True
        # Check f(1) == 1
        if S(f(R(1))) != S(1):
            is_homo = False
            
        # Check addition and multiplication preservation
        for a in test_elems:
            for b in test_elems:
                if S(f(a + b)) != S(f(a)) + S(f(b)):
                    is_homo = False
                if S(f(a * b)) != S(f(a)) * S(f(b)):
                    is_homo = False
                    
        # Check injectivity
        is_injective = True
        for a in test_elems:
            for b in test_elems:
                if a != b and S(f(a)) == S(f(b)):
                    is_injective = False
                    
        neg_q = not (is_homo and is_injective)
    except Exception:
        # If f fails to evaluate properly, it cannot be extended to a valid homomorphism
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are integral domains",
    "H_2: K and L are fields of fractions of R and S, respectively",
    "¬Q: There does not exist a unique injective ring homomorphism extending f"
]

N_HYP = 2
NEG_Q_INDEX = 2