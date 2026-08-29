import sympy
from sympy import symbols, Rational, Integer
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

# Standard group bindings
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

# Linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for any commutative Noetherian local ring (R, m),
    an arbitrary integer d is equal to the minimum number of elements required 
    to generate an m-primary ideal of R.
    """
    h1_ok = False
    neg_q = False
    
    R = None
    d = None
    
    # 1. Extract R and d from the witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, m, d = witness
            elif len(witness) == 2:
                R, d = witness
        elif isinstance(witness, dict):
            R = witness.get('R', witness.get('ring', witness))
            d = witness.get('d')
        else:
            R = witness
            try:
                d = witness.d
            except AttributeError:
                pass
    except Exception:
        pass

    # If d couldn't be extracted, check if the witness itself is a mock object containing everything
    if d is None:
        try:
            if witness.is_commutative and witness.is_Noetherian and witness.is_local:
                h1_ok = True
                min_gens = int(witness.min_gens_m_primary)
                d_val = int(witness.d)
                neg_q = bool(d_val != min_gens)
                return [h1_ok, neg_q]
        except Exception:
            pass
        return [False, False]

    min_gens = None

    # 2. Evaluate if R is a commutative Noetherian local ring and find min_gens
    
    # Case A: R is a SymPy Field (fields are local rings with Krull dimension 0)
    try:
        if hasattr(R, 'is_Field') and R.is_Field:
            h1_ok = True
            min_gens = 0
    except Exception:
        pass

    try:
        if not h1_ok and hasattr(R, 'is_field') and R.is_field:
            h1_ok = True
            min_gens = 0
    except Exception:
        pass

    # Case B: R is an integer representing Z/p^k Z
    try:
        if not h1_ok and isinstance(R, int) and R > 1:
            factors = factorint(R)
            if len(factors) == 1:  # Prime power -> local ring
                h1_ok = True
                min_gens = 0
    except Exception:
        pass

    # Case C: R is a string like "Z/8Z"
    try:
        if not h1_ok and isinstance(R, str):
            s = R.replace(' ', '')
            if s.startswith('Z/') and s.endswith('Z'):
                n_str = s[2:-1]
                if n_str.isdigit():
                    n = int(n_str)
                    factors = factorint(n)
                    if len(factors) == 1:
                        h1_ok = True
                        min_gens = 0
    except Exception:
        pass

    # Case D: Duck-typing for a mock object
    try:
        if not h1_ok and hasattr(R, 'is_commutative'):
            if R.is_commutative and R.is_Noetherian and R.is_local:
                min_gens = int(R.min_gens_m_primary)
                h1_ok = True
    except Exception:
        pass

    # Case E: Duck-typing for a dictionary
    try:
        if not h1_ok and isinstance(R, dict):
            if R.get('is_commutative') and R.get('is_Noetherian') and R.get('is_local'):
                min_gens = int(R.get('min_gens_m_primary'))
                h1_ok = True
    except Exception:
        pass

    # 3. Evaluate the negated conclusion
    if h1_ok and min_gens is not None and d is not None:
        try:
            d_val = int(d)
            neg_q = bool(d_val != min_gens)
        except Exception:
            neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: (R, m) is a commutative Noetherian local ring",
    "¬Q: d is not equal to the minimum number of elements required to generate an m-primary ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1