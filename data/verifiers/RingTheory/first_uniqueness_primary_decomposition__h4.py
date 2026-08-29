import sympy
from sympy import eye, zeros
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

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the First Uniqueness Theorem 
    for Primary Decomposition.
    
    The witness can be:
      - An ideal I
      - A tuple (R, I)
      - A tuple (I, decomp1, decomp2)
      - A tuple (R, I, decomp1, decomp2)
    where decomp1 and decomp2 are lists of primary ideals representing two minimal 
    primary decompositions.
    """
    R = None
    I = None
    decomp1 = None
    decomp2 = None
    
    if isinstance(witness, tuple):
        if len(witness) == 2:
            R, I = witness
        elif len(witness) == 3:
            I, decomp1, decomp2 = witness
            R = getattr(I, 'ring', None)
        elif len(witness) == 4:
            R, I, decomp1, decomp2 = witness
        else:
            I = witness
            R = getattr(I, 'ring', None)
    else:
        I = witness
        R = getattr(I, 'ring', None)

    # H_1: R is a commutative ring
    h1 = False
    try:
        if R is not None:
            # Polynomial rings in sympy are commutative
            h1 = getattr(R, 'is_commutative', True)
    except Exception:
        pass

    # H_2: R is a Noetherian ring
    h2 = False
    try:
        if R is not None:
            # Polynomial rings over fields/integers (standard in sympy) are Noetherian
            h2 = True
    except Exception:
        pass

    # H_3: I is a proper ideal of R
    h3 = False
    try:
        if R is not None and I is not None:
            if not hasattr(I, 'ring'):
                I = R.ideal(*I) if isinstance(I, (list, tuple)) else R.ideal(I)
            h3 = I != R.ideal(1)
    except Exception:
        pass

    # neg_Q: The set of prime ideals is NOT uniquely determined by I
    # (i.e., it depends on the choice of minimal primary decomposition)
    neg_q = False
    try:
        if decomp1 is not None and decomp2 is not None:
            def get_radicals(decomp):
                rads = set()
                for q in decomp:
                    if hasattr(q, 'radical'):
                        rads.add(frozenset(q.radical().gens))
                    else:
                        rads.add(frozenset(q.gens))
                return rads
            
            rads1 = get_radicals(decomp1)
            rads2 = get_radicals(decomp2)
            
            if rads1 != rads2:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a Noetherian ring",
    "H_3: I is a proper ideal of R",
    "¬Q: The set of prime ideals is not uniquely determined by I"
]

N_HYP = 3
NEG_Q_INDEX = 3