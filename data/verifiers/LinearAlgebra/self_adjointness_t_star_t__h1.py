import sympy as sp
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

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: The adjoint operator T^* exists",
    "¬Q: The composition operator T^*T is not self-adjoint"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks whether the given witness is a counterexample to the conjecture.
    The witness can be provided as:
      - A dictionary or mock object with boolean properties (for infinite-dimensional unbounded operators).
      - A tuple (T, G) where T is a matrix and G is a non-degenerate sesquilinear form matrix.
      - A tuple (T, T_star, G) explicitly providing the adjoint.
      - A single matrix T (assumes standard inner product, which will never be a counterexample).
    """
    
    # 1. Try dictionary mock
    if isinstance(witness, dict):
        try:
            if 'is_linear_operator' in witness:
                h1 = bool(witness['is_linear_operator'])
                h2 = bool(witness['adjoint_exists'])
                q = bool(witness['T_star_T_is_self_adjoint'])
                return [h1, h2, not q]
        except Exception:
            pass

    # 2. Try object mock
    try:
        if hasattr(witness, 'is_linear_operator'):
            h1 = bool(witness.is_linear_operator)
            h2 = bool(witness.adjoint_exists)
            q = bool(witness.T_star_T_is_self_adjoint)
            return [h1, h2, not q]
    except Exception:
        pass

    # 3. Try (T, T_star, G)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            T, T_star, G = witness
            h1 = T.is_square
            
            det_G = G.det()
            is_det_zero = False
            if hasattr(det_G, 'is_zero') and det_G.is_zero is not None:
                is_det_zero = det_G.is_zero
            else:
                is_det_zero = (det_G == 0)
                
            if G.is_square and G.shape == T.shape and not is_det_zero:
                # Adjoint definition w.r.t sesquilinear form G: G.H * T_star == T.H * G.H
                diff_adj = G.H * T_star - T.H * G.H
                if hasattr(diff_adj, 'is_zero_matrix') and diff_adj.is_zero_matrix is not None:
                    is_adj = diff_adj.is_zero_matrix
                else:
                    is_adj = (G.H * T_star == T.H * G.H)
                h2 = is_adj
            else:
                h2 = False
                
            if h1 and h2:
                M = T_star * T
                # Self-adjoint w.r.t G means M_star == M, so G.H * M == M.H * G.H
                diff_q = G.H * M - M.H * G.H
                if hasattr(diff_q, 'is_zero_matrix') and diff_q.is_zero_matrix is not None:
                    q = diff_q.is_zero_matrix
                else:
                    q = (G.H * M == M.H * G.H)
            else:
                q = True
                
            return [bool(h1), bool(h2), not bool(q)]
    except Exception:
        pass

    # 4. Try (T, G)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            T, G = witness
            h1 = T.is_square
            
            det_G = G.det()
            is_det_zero = False
            if hasattr(det_G, 'is_zero') and det_G.is_zero is not None:
                is_det_zero = det_G.is_zero
            else:
                is_det_zero = (det_G == 0)
                
            h2 = G.is_square and G.shape == T.shape and not is_det_zero
            
            if h1 and h2:
                T_star = (G.H).inv() * T.H * G.H
                M = T_star * T
                M_star = (G.H).inv() * M.H * G.H
                
                diff = M - M_star
                if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix is not None:
                    q = diff.is_zero_matrix
                else:
                    q = (M == M_star)
            else:
                q = True
                
            return [bool(h1), bool(h2), not bool(q)]
    except Exception:
        pass

    # 5. Try single matrix T (assumes standard inner product G = I)
    try:
        if hasattr(witness, 'is_square') and witness.is_square:
            h1 = True
            h2 = True
            M = witness.H * witness
            diff = M - M.H
            if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix is not None:
                q = diff.is_zero_matrix
            else:
                q = (M == M.H)
            return [h1, h2, not q]
    except Exception:
        pass

    return [False, False, False]