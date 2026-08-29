import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    """
    Given a witness, checks whether it is a valid counterexample to the false conjecture.
    The witness is expected to be an object or dictionary providing the properties,
    as infinite posets and incidence algebras are not natively represented in sympy.
    """
    h1 = False
    h2 = False
    h3 = False
    q = True

    try:
        if isinstance(witness, Matrix):
            # For a finite matrix, P is implicitly a finite linear order (locally finite poset)
            h1 = True
            # R is implicitly the commutative ring of sympy expressions
            h2 = True
            # f \in I(P, R) means the matrix is upper triangular
            h3 = witness.is_upper
            # For finite matrices over commutative rings, f is a unit iff its diagonal entries are units.
            # Thus the conclusion Q is always True for finite matrices.
            q = True
            return [h1, h2, h3, not q]
            
        if isinstance(witness, dict):
            h1 = bool(witness.get('P_is_locally_finite', False))
            h2 = bool(witness.get('R_is_commutative_ring_with_identity', False))
            h3 = bool(witness.get('f_in_I_P_R', False))
            is_unit = bool(witness.get('f_is_unit', True))
            diag_unit = bool(witness.get('f_xx_is_unit', True))
            q = (is_unit == diag_unit)
        else:
            h1 = bool(getattr(witness, 'P_is_locally_finite', False))
            h2 = bool(getattr(witness, 'R_is_commutative_ring_with_identity', False))
            h3 = bool(getattr(witness, 'f_in_I_P_R', False))
            is_unit = bool(getattr(witness, 'f_is_unit', True))
            diag_unit = bool(getattr(witness, 'f_xx_is_unit', True))
            q = (is_unit == diag_unit)
    except Exception:
        pass

    return [h1, h2, h3, not q]

CONDITION_LABELS = [
    "H_1: P is a locally finite partially ordered set",
    "H_2: R is a commutative ring with identity",
    "H_3: f \\in I(P, R)",
    "¬Q: f is a unit in I(P, R) if and only if f(x, x) is a unit in R for all x \\in P fails"
]

N_HYP = 3
NEG_Q_INDEX = 3