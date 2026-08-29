import sympy
from sympy import MatrixBase, eye, zeros, Matrix
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

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the conjecture:
    "The kernel of P and the image of P are orthogonal complements if and only if P = P^*"
    
    The witness can be a single matrix P (assuming standard inner product) 
    or a tuple (P, G) where G is the Gram matrix of the inner product.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            P, G = witness
        else:
            P = witness
            G = eye(P.shape[0])
            
        H1 = isinstance(P, MatrixBase) and P.is_square
        if isinstance(witness, tuple):
            H1 = H1 and isinstance(G, MatrixBase) and G.is_square and G.shape == P.shape
    except Exception:
        H1 = False

    try:
        H2 = (P**2 == P)
    except Exception:
        H2 = False

    try:
        # Check if kernel and image are orthogonal complements
        null_basis = P.nullspace()
        col_basis = P.columnspace()
        
        # Im(P)^\perp = { x | x^H G y = 0 for all y in Im(P) }
        # Let C be the matrix whose columns are col_basis.
        # x^H G C = 0 => C^H G^H x = 0.
        # So Im(P)^\perp is the nullspace of C^H G^H.
        if col_basis:
            C_mat = col_basis[0].row_join(*col_basis[1:])
            im_perp_basis = (C_mat.adjoint() * G.adjoint()).nullspace()
        else:
            im_perp_basis = eye(P.shape[0]).columnspace()
            
        if null_basis:
            N_mat = null_basis[0].row_join(*null_basis[1:])
        else:
            N_mat = zeros(P.shape[0], 1)
            
        if im_perp_basis:
            Im_perp_mat = im_perp_basis[0].row_join(*im_perp_basis[1:])
        else:
            Im_perp_mat = zeros(P.shape[0], 1)
            
        # Check if Ker(P) and Im(P)^\perp are the same subspace
        rank_N = N_mat.rank()
        rank_Im_perp = Im_perp_mat.rank()
        rank_both = N_mat.row_join(Im_perp_mat).rank()
        
        is_ortho_comp = (rank_N == rank_Im_perp == rank_both)
        
        # Check P == P^*
        # P is self-adjoint with respect to G if <Pu, v> = <u, Pv> for all u, v.
        # (Pu)^H G v = u^H P^H G v
        # <u, Pv> = u^H G P v
        # So P^H G == G P
        is_self_adjoint = (P.adjoint() * G == G * P)
        
        Q = (is_ortho_comp == is_self_adjoint)
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: P is a linear operator",
    "H_2: P^2 = P",
    "¬Q: (Ker(P) and Im(P) are orthogonal complements) XOR (P = P^*)"
]

N_HYP = 2
NEG_Q_INDEX = 2