import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
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
    h1 = False
    neg_q = False
    
    try:
        # The witness might be a tuple (R, P) or just the ideal P.
        if isinstance(witness, tuple):
            P = witness[-1]
            R = witness[0] if len(witness) > 1 else None
        else:
            P = witness
            R = None
            
        # If R or P is explicitly given as a matrix (n > 1), it's generally not a commutative ring.
        if hasattr(R, 'is_Matrix') and R.is_Matrix:
            if R.shape[0] > 1:
                return [False, False]
        if hasattr(P, 'is_Matrix') and P.is_Matrix:
            if P.shape[0] > 1:
                return [False, False]
                
        # Handle string representations of rings/ideals
        if isinstance(P, str):
            s = P.strip().lower()
            if s in ['z', 'r', '1', 'whole ring', 'entire ring', 'zero ring']:
                return [True, True]
            elif s == '0':
                return [True, False]
                
        # Handle rational numbers (non-integers generate the whole ring in a field)
        if hasattr(P, 'is_Rational') and P.is_Rational and not P.is_Integer:
            return [True, True]
                
        # Try to interpret P as an integer representing the ideal nZ in Z
        try:
            n = abs(int(P))
            h1 = True
            # In Z, nZ is a prime ideal iff n is prime or n == 0
            lhs = sympy.isprime(n) or n == 0
            # There exists an integral domain D and homomorphism phi with ker(phi) = nZ
            # iff n is prime, n == 0, or n == 1 (using the zero map to Z)
            rhs = sympy.isprime(n) or n == 0 or n == 1
            neg_q = (lhs != rhs)
            return [h1, neg_q]
        except (ValueError, TypeError):
            pass
            
        # If P is a group object representing a ring (e.g., Z6 for Z/6Z)
        if hasattr(P, 'is_abelian'):
            h1 = bool(P.is_abelian)
            # If the witness is the ring itself, the ideal is the whole ring, so the equivalence fails.
            neg_q = True
            return [h1, neg_q]
            
        # Handle sympy expressions (e.g., polynomials)
        if isinstance(P, sympy.Expr):
            h1 = True
            if P.is_constant():
                if P == 0:
                    lhs = True
                    rhs = True
                else:
                    lhs = False
                    rhs = True
            else:
                lhs = False
                rhs = False
            neg_q = (lhs != rhs)
            return [h1, neg_q]
            
    except Exception:
        pass
        
    return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The equivalence (P is a prime ideal iff exists integral domain D and homomorphism phi with ker(phi)=P) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1