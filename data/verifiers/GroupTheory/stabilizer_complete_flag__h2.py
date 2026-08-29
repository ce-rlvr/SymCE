import sympy
from sympy.matrices import Matrix, eye, zeros
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
    # H_1: V is an n-dimensional vector space over a field F with a chosen basis e_1, ..., e_n
    # We interpret this as the witness being a collection of n x n matrices representing a group G acting on V.
    h1_ok = False
    try:
        if type(witness).__name__ == 'MatrixGroup':
            n = witness.degree
            h1_ok = n >= 1
        elif isinstance(witness, (list, tuple, set)):
            witness_list = list(witness)
            if len(witness_list) > 0:
                n = witness_list[0].rows
                if n >= 1 and all(isinstance(m, Matrix) and m.rows == n and m.cols == n for m in witness_list):
                    h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: ℱ is the standard complete flag 0 = V_0 ⊂ V_1 ⊂ ... ⊂ V_n = V, where V_i = span(e_1, ..., e_i)
    # We interpret this as the witness being a valid group (closed under multiplication, contains identity, all invertible).
    h2_ok = False
    try:
        if h1_ok:
            if type(witness).__name__ == 'MatrixGroup':
                h2_ok = True
            else:
                witness_list = list(witness)
                n = witness_list[0].rows
                witness_set = {tuple(m) for m in witness_list}
                I_tup = tuple(eye(n))
                has_id = I_tup in witness_set
                all_inv = all(m.det() != 0 for m in witness_list)
                closed = True
                if has_id and all_inv:
                    for a in witness_list:
                        for b in witness_list:
                            if tuple(a * b) not in witness_set:
                                closed = False
                                break
                        if not closed:
                            break
                    h2_ok = closed
    except Exception:
        h2_ok = False

    # ¬Q: The stabilizer of ℱ in G is NOT the subgroup of upper-triangular invertible matrices.
    # If Stab_G(ℱ) is the set of ALL upper-triangular invertible matrices, then G must contain all of them.
    # We construct specific upper-triangular invertible matrices (U1, U2). 
    # If they are not in G, then Stab_G(ℱ) cannot be the full subgroup of upper-triangular invertible matrices.
    neg_q = False
    try:
        if h1_ok and h2_ok:
            if type(witness).__name__ == 'MatrixGroup':
                n = witness.degree
            else:
                witness_list = list(witness)
                n = witness_list[0].rows
            
            U1 = eye(n)
            if n > 1:
                U1[0, 1] = 1
            else:
                U1[0, 0] = 2
                
            U2 = eye(n)
            if n > 1:
                U2[0, 1] = 2
            else:
                U2[0, 0] = 3

            if type(witness).__name__ == 'MatrixGroup':
                if U1 not in witness:
                    neg_q = True
                elif U2 not in witness:
                    neg_q = True
            else:
                witness_set = {tuple(m) for m in witness_list}
                if tuple(U1) not in witness_set:
                    neg_q = True
                elif tuple(U2) not in witness_set:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: V is an n-dimensional vector space over a field F with a chosen basis e_1, ..., e_n",
    "H_2: ℱ is the standard complete flag 0 = V_0 ⊂ V_1 ⊂ ... ⊂ V_n = V, where V_i = span(e_1, ..., e_i)",
    "¬Q: The stabilizer of ℱ in G is not the subgroup of upper-triangular invertible matrices with respect to the basis e_1, ..., e_n"
]

N_HYP = 2
NEG_Q_INDEX = 2