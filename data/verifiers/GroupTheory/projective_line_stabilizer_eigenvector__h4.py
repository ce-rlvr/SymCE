import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    Checks the hypotheses and negated conclusion for the conjecture.
    The witness is expected to be a tuple (T, v) where:
      - T is a sympy Matrix representing a linear transformation in GL(V)
      - v is a sympy column Matrix representing the non-zero vector spanning L
    """
    try:
        T, v = witness
        
        # H_1: V is a vector space over a field F
        # Implicitly true for the vector space F^n where T and v reside.
        h1 = True
        
        # H_2: GL(V) is the general linear group of V
        # T must be an invertible square matrix.
        h2 = T.is_square and T.det() != 0
        
        # H_3: P(V) is the projective space of V, consisting of all 1-dimensional subspaces
        # Implicitly true by definition of the spaces.
        h3 = True
        
        # H_4: L is a 1-dimensional subspace in P(V) spanned by a non-zero vector v in V
        # v must be a non-zero column vector of the correct dimension.
        h4 = getattr(v, 'is_zero', True) == False and v.shape[1] == 1 and v.shape[0] == T.shape[0]
        
        # ¬Q: The stabilizer of L in GL(V) does NOT consist exactly of those linear 
        # transformations in GL(V) for which v is an eigenvector.
        
        # Check if T stabilizes L (i.e., T*v is in the span of v)
        Tv = T * v
        M = v.row_join(Tv)
        stabilizes = (M.rank() == 1)
        
        # Check if v is an eigenvector of T (i.e., T*v = lambda * v for some lambda)
        is_eig = False
        for i in range(v.rows):
            if v[i, 0] != 0:
                # Cross-multiply to avoid division issues: v_i * (T*v) == (T*v)_i * v
                if (v[i, 0] * Tv) == (Tv[i, 0] * v):
                    is_eig = True
                break
                
        # The conclusion states that the set of stabilizers equals the set of transformations 
        # where v is an eigenvector. The negation is that these two conditions differ for T.
        neg_q = stabilizes != is_eig
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: GL(V) is the general linear group of V",
    "H_3: P(V) is the projective space of V",
    "H_4: L is a 1-dimensional subspace spanned by a non-zero vector v",
    "¬Q: The stabilizer of L in GL(V) does not consist exactly of those linear transformations for which v is an eigenvector"
]

N_HYP = 4
NEG_Q_INDEX = 4