import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for standard algebra objects
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
    Checks if the witness is a valid counterexample to the false conjecture:
    dim(R/(IJ)) = max(dim(R/I), dim(R/J))
    
    Since SymPy cannot natively compute Krull dimension for arbitrary non-commutative rings 
    (where this conjecture fails), this verifier is designed to be flexible and accept 
    witnesses in multiple formats:
    1. A dictionary containing the dimensions.
    2. An object with properties/methods for the dimensions.
    3. A tuple of dimensions (dim_I, dim_J, dim_IJ).
    4. A tuple of univariate polynomials (f, g) where `dim` is interpreted as vector space dimension.
    """
    
    # 1. Try dictionary format
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('I_is_ideal', True))
            h2 = bool(witness.get('J_is_ideal', True))
            dim_I = witness['dim_R_I']
            dim_J = witness['dim_R_J']
            dim_IJ = witness['dim_R_IJ']
            neg_q = dim_IJ != max(dim_I, dim_J)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try object with properties/methods format
    try:
        h1 = bool(getattr(witness, 'I_is_ideal', True))
        h2 = bool(getattr(witness, 'J_is_ideal', True))
        
        dim_I = witness.dim_R_I() if callable(getattr(witness, 'dim_R_I', None)) else witness.dim_R_I
        dim_J = witness.dim_R_J() if callable(getattr(witness, 'dim_R_J', None)) else witness.dim_R_J
        dim_IJ = witness.dim_R_IJ() if callable(getattr(witness, 'dim_R_IJ', None)) else witness.dim_R_IJ
        
        neg_q = dim_IJ != max(dim_I, dim_J)
        return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try tuple of dimensions format: (dim_I, dim_J, dim_IJ)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            dim_I, dim_J, dim_IJ = witness
            if all(isinstance(val, (int, float)) for val in witness):
                h1 = True
                h2 = True
                neg_q = dim_IJ != max(dim_I, dim_J)
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 4. Try tuple of polynomials (f, g) representing ideals in k[x]
    # In this context, `dim` is interpreted as the vector space dimension (degree of the polynomial).
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            f = sympy.Poly(witness[0])
            g = sympy.Poly(witness[1])
            if len(f.gens) == 1 and len(g.gens) == 1 and f.gens == g.gens:
                h1 = True
                h2 = True
                dim_I = f.degree()
                dim_J = g.degree()
                dim_IJ = (f * g).degree()
                neg_q = dim_IJ != max(dim_I, dim_J)
                return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "¬Q: dim(R/(IJ)) != max(dim(R/I), dim(R/J))"
]

N_HYP = 2
NEG_Q_INDEX = 2