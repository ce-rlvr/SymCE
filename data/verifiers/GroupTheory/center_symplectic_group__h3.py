import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.abc import x

# Top-level setup: named object bindings
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
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok].
    """
    F = None
    n = None
    G = None
    
    # Extract F, n, G from the witness
    if isinstance(witness, dict):
        F = witness.get('F')
        n = witness.get('n')
        G = witness.get('G')
    elif isinstance(witness, (list, tuple)):
        for item in witness:
            if getattr(item, 'is_Field', False):
                F = item
            elif isinstance(item, int) or (hasattr(item, 'is_integer') and item.is_integer):
                n = item
            elif isinstance(item, (list, tuple)) or hasattr(item, 'generate') or (hasattr(item, 'shape') and len(item.shape) == 2):
                G = item
    else:
        F = getattr(witness, 'F', None)
        n = getattr(witness, 'n', None)
        G = getattr(witness, 'G', None)

    # H_1: F is a field with characteristic not equal to 2
    try:
        h1 = False
        if getattr(F, 'is_Field', False):
            char = getattr(F, 'characteristic', None)
            if callable(char):
                char = char()
            if char is not None and char != 2:
                h1 = True
            elif char is None:
                # Fallback for common SymPy fields that might not explicitly define characteristic
                if F in (sympy.QQ, sympy.RR, sympy.CC):
                    h1 = True
    except Exception:
        h1 = False

    # H_2: n >= 1
    try:
        h2 = False
        if n is not None:
            if isinstance(n, int) or (hasattr(n, 'is_integer') and n.is_integer):
                h2 = int(n) >= 1
    except Exception:
        h2 = False

    # ¬Q: The center of G does NOT consist exactly of the identity matrix I and its negative -I
    try:
        neg_q = False
        if G is not None:
            if hasattr(G, 'shape') and len(G.shape) == 2:
                elements = [G]
            elif hasattr(G, 'generate'):
                elements = list(G.generate())
            else:
                elements = list(G)
                
            if not elements:
                neg_q = True
            else:
                k = elements[0].shape[0]
                I = eye(k)
                neg_I = -I
                
                # Compute the center of G
                center = []
                for g in elements:
                    commutes = True
                    for h in elements:
                        if g * h != h * g:
                            commutes = False
                            break
                    if commutes:
                        center.append(g)
                        
                # Check if the center is exactly {I, -I}
                if len(center) != 2:
                    neg_q = True
                else:
                    has_I = any(c == I for c in center)
                    has_neg_I = any(c == neg_I for c in center)
                    if has_I and has_neg_I:
                        neg_q = False
                    else:
                        neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field with characteristic not equal to 2",
    "H_2: n >= 1",
    "¬Q: The center of G does NOT consist exactly of I and -I"
]

N_HYP = 2
NEG_Q_INDEX = 2