import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.rings import PolyRing

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

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The dropped hypothesis is that I is an ideal of R.
    """
    # Extract k, R, I
    if isinstance(witness, dict):
        k = witness.get('k')
        R = witness.get('R')
        I = witness.get('I')
    else:
        k = getattr(witness, 'k', None)
        R = getattr(witness, 'R', None)
        I = getattr(witness, 'I', None)

    # H1: k is a field
    try:
        h1 = hasattr(k, 'is_Field') and k.is_Field
    except Exception:
        h1 = False

    # H2: R is a commutative k-algebra
    try:
        if isinstance(R, PolyRing) and R.domain == k:
            h2 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative and hasattr(R, 'domain') and R.domain == k:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: R is finitely generated as a k-algebra
    try:
        if hasattr(R, 'gens') and len(R.gens) >= 0:
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: R/I is not finitely generated as a k-algebra
    # This happens if I is not an ideal, making R/I not a valid quotient ring.
    try:
        is_ideal = False
        if hasattr(I, 'is_ideal'):
            is_ideal = I.is_ideal(R)
        elif type(I).__name__ == 'Ideal':
            is_ideal = True
        elif isinstance(I, PolyRing):
            is_ideal = False
        elif isinstance(I, (list, set, tuple)):
            if len(I) == 0:
                is_ideal = False
            else:
                if not any(a == R.zero for a in I):
                    is_ideal = False
                else:
                    is_ideal = True
                    # Check closure under addition
                    for a in I:
                        for b in I:
                            if (a + b) not in I:
                                is_ideal = False
                                break
                        if not is_ideal:
                            break
                    # Check closure under multiplication by generators
                    if is_ideal:
                        for a in I:
                            for g in R.gens:
                                if (a * g) not in I:
                                    is_ideal = False
                                    break
                            if not is_ideal:
                                break
        else:
            is_ideal = False
            
        neg_q = not is_ideal
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: R is a commutative k-algebra",
    "H_3: R is finitely generated as a k-algebra",
    "¬Q: The quotient ring R/I is not finitely generated as a k-algebra"
]

N_HYP = 3
NEG_Q_INDEX = 3