import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Symbol, ZZ

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

# Standard symbols for infinitely generated groups
F_infty = Symbol('F_infty')
Z_infty = Symbol('Z_infty')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, k) where F is the group and k is the index.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            a, b = witness
            # Robust unpacking in case the order is (k, F) instead of (F, k)
            if isinstance(a, (int, sympy.Integer)) and not isinstance(b, (int, sympy.Integer)):
                k, F = a, b
            else:
                F, k = a, b
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: k is a positive integer
    try:
        h1 = False
        if isinstance(k, (int, sympy.Integer)):
            if k >= 1:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: There are infinitely many distinct subgroups of F that have index k
    try:
        neg_q = False
        if h1 and k >= 2:
            is_polyring_zz = False
            try:
                # A polynomial ring over ZZ (like ZZ[x]) as an additive group is 
                # free abelian on countably many generators, thus having infinitely 
                # many subgroups of index k for any k >= 2.
                if F.__class__.__name__ == 'PolyRing' and F.domain == ZZ and len(F.gens) >= 1:
                    is_polyring_zz = True
            except Exception:
                pass
            
            if is_polyring_zz:
                neg_q = True
            else:
                # Check if F is a string or symbol indicating an infinitely generated group
                name = ''
                if isinstance(F, str):
                    name = F
                elif hasattr(F, 'name'):
                    name = str(F.name)
                else:
                    name = str(F)
                
                name_lower = name.lower()
                indicators = ['inf', 'z[x]', 'countably generated', 'free abelian']
                if any(ind in name_lower for ind in indicators):
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "¬Q: There are infinitely many distinct subgroups of F that have index k"
]

N_HYP = 1
NEG_Q_INDEX = 1