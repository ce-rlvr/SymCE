import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: It is not the case that M is an injective R-module if and only if M is a divisible R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False

    # Helper to safely extract boolean properties from objects or dictionaries
    def get_prop(obj, names):
        if isinstance(obj, dict):
            for name in names:
                if name in obj:
                    val = obj[name]
                    if callable(val): 
                        val = val()
                    return bool(val)
        for name in names:
            if hasattr(obj, name):
                val = getattr(obj, name)
                if callable(val): 
                    val = val()
                return bool(val)
        return None

    # Determine R and M from the witness
    R = witness
    M = witness
    if isinstance(witness, tuple) and len(witness) == 2:
        R, M = witness
    elif isinstance(witness, dict):
        if 'R' in witness and 'M' in witness:
            R = witness['R']
            M = witness['M']

    # Check H_1: R is a principal ideal domain
    try:
        h1_val = get_prop(R, ['is_PID', 'is_pid', 'is_principal_ideal_domain', 'ring_is_PID', 'ring_is_pid'])
        if h1_val is not None:
            h1 = h1_val
    except Exception:
        h1 = False

    # Check ¬Q: M is injective iff M is divisible (we want this equivalence to FAIL)
    try:
        inj = get_prop(M, ['is_injective', 'is_injective_module'])
        div = get_prop(M, ['is_divisible', 'is_divisible_module'])
        
        if inj is not None and div is not None:
            # The conclusion is (inj == div). We want the negation.
            neg_q = not (inj == div)
    except Exception:
        neg_q = False

    return [h1, neg_q]