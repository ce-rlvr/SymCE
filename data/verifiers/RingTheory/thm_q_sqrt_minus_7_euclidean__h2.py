import sympy
from sympy import sqrt, I
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def extract_d(obj):
    """Helper to extract the square-free integer d from representations of Q(sqrt(d))."""
    if isinstance(obj, int):
        return obj
    
    try:
        if hasattr(obj, 'has') and obj.has(I):
            sq = obj**2
            if sq.is_Integer:
                return int(sq)
    except Exception:
        pass

    s = str(obj).replace(' ', '')
    
    # Match I*sqrt(d)
    idx = s.find('I*sqrt(')
    if idx != -1:
        start = idx + 7
        end = s.find(')', start)
        if end != -1:
            num_str = s[start:end]
            try:
                return -int(num_str)
            except ValueError:
                pass

    # Match sqrt(d)*I
    idx = s.find('sqrt(')
    if idx != -1:
        start = idx + 5
        end = s.find(')', start)
        if end != -1 and s[end:end+3] == ')*I':
            num_str = s[start:end]
            try:
                return -int(num_str)
            except ValueError:
                pass

    # Match sqrt(d) or sqrt(-d)
    idx = s.find('sqrt(')
    if idx != -1:
        start = idx + 5
        end = s.find(')', start)
        if end != -1:
            num_str = s[start:end]
            try:
                return int(num_str)
            except ValueError:
                pass

    return None

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypothesis and fails the conclusion.
    The witness can be a field K, or a dictionary specifying K and an order O_K.
    """
    try:
        K = witness.get('K', witness) if isinstance(witness, dict) else witness
        O_K = witness.get('O_K', witness) if isinstance(witness, dict) else witness
        
        d = extract_d(K)
        h1 = (d == -7)
    except Exception:
        h1 = False

    try:
        d_O = extract_d(O_K)
        if d_O is None:
            d_O = d
            
        if d_O is None:
            neg_q = False
        else:
            O_K_str = str(O_K).replace(' ', '')
            
            # If O_K is explicitly a non-maximal order like Z[sqrt(-7)], it is not Euclidean.
            # The maximal order for d = -3, -7, -11 is Z[(1+sqrt(d))/2].
            if d_O in [-3, -7, -11]:
                if ("Z[" in O_K_str or "ZZ[" in O_K_str) and "1+" not in O_K_str and "/2" not in O_K_str:
                    neg_q = True
                else:
                    # Assume maximal order (ring of integers)
                    is_euclidean = d_O in [-1, -2, -3, -7, -11]
                    neg_q = not is_euclidean
            else:
                # For other d, the maximal order is Euclidean iff d in {-1, -2}
                is_euclidean = d_O in [-1, -2, -3, -7, -11]
                neg_q = not is_euclidean
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is the imaginary quadratic field Q(sqrt(-7))",
    "¬Q: O_K is not a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1