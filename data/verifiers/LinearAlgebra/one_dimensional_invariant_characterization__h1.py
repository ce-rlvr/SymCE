import sympy
from sympy.matrices import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    if isinstance(witness, dict):
        try:
            h1 = witness.get('is_linear_operator', False)
            h2 = witness.get('is_one_dimensional_subspace', False)
            is_inv = witness.get('is_invariant', False)
            any_eigen = witness.get('any_non_zero_is_eigenvector', False)
            neg_q = is_inv != any_eigen
            return [bool(h1), bool(h2), bool(neg_q)]
        except Exception:
            pass

    try:
        h1 = witness.is_linear_operator()
        h2 = witness.is_one_dimensional_subspace()
        is_inv = witness.is_invariant()
        any_eigen = witness.any_non_zero_is_eigenvector()
        neg_q = is_inv != any_eigen
        return [bool(h1), bool(h2), bool(neg_q)]
    except AttributeError:
        pass
    except Exception:
        pass

    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                T, u, v = witness
            elif len(witness) == 2:
                T, u = witness
                v = u
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if isinstance(u, list) and len(u) == 1:
            u = u[0]
        if isinstance(v, list) and len(v) == 1:
            v = v[0]
            
        h1 = getattr(T, 'is_square', False)
        
        if hasattr(u, 'shape') and hasattr(T, 'shape'):
            h2 = (u.shape[0] == T.shape[0] and u.shape[1] == 1 and not getattr(u, 'is_zero_matrix', True))
        else:
            h2 = False
            
        Tu = T * u
        M_inv = u.row_join(Tu)
        is_inv = (M_inv.rank() == 1)
        
        M_v = u.row_join(v)
        v_in_U = (M_v.rank() == 1)
        v_non_zero = not getattr(v, 'is_zero_matrix', True)
        
        Tv = T * v
        M_ev = v.row_join(Tv)
        v_is_eigenvector = (M_ev.rank() == 1)
        
        if v_in_U and v_non_zero and not v_is_eigenvector:
            any_eigen = False
        else:
            any_eigen = is_inv
            
        neg_q = is_inv != any_eigen
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: U is a one-dimensional subspace of V",
    "¬Q: U is T-invariant XOR any non-zero vector in U is an eigenvector of T"
]

N_HYP = 2
NEG_Q_INDEX = 2