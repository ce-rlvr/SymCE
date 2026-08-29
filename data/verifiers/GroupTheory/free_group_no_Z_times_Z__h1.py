import sympy
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

F_free = FreeGroup('x, y')
x_gen, y_gen = F_free.generators
ZxZ = FpGroup(F_free, [x_gen*y_gen*x_gen**-1*y_gen**-1])

CONDITION_LABELS = [
    "¬Q: F contains a subgroup isomorphic to Z x Z"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    neg_q = False
    
    try:
        if witness == ZxZ:
            neg_q = True
    except Exception:
        pass

    if not neg_q:
        try:
            if isinstance(witness, FpGroup):
                invs = witness.abelian_invariants()
                if invs.count(0) >= 2:
                    gens = witness.generators
                    is_ab = True
                    for i in range(len(gens)):
                        for j in range(i+1, len(gens)):
                            try:
                                if gens[i] * gens[j] != gens[j] * gens[i]:
                                    is_ab = False
                                    break
                            except Exception:
                                is_ab = False
                                break
                        if not is_ab:
                            break
                    if is_ab:
                        neg_q = True
        except Exception:
            pass

    if not neg_q:
        try:
            if isinstance(witness, (list, tuple)) and len(witness) == 2:
                A, B = witness
                if hasattr(A, 'is_Matrix') and hasattr(B, 'is_Matrix'):
                    if A.shape == B.shape and A.shape[0] == A.shape[1]:
                        if A * B == B * A:
                            I = sympy.eye(A.shape[0])
                            if (A - I).is_nilpotent() and (B - I).is_nilpotent():
                                def mat_log(M):
                                    N = M - I
                                    res = sympy.zeros(*M.shape)
                                    term = N
                                    sign = 1
                                    for i in range(1, M.shape[0] + 1):
                                        res += sign * term / i
                                        term = term * N
                                        sign *= -1
                                    return res
                                
                                logA = mat_log(A)
                                logB = mat_log(B)
                                
                                vecA = list(logA)
                                vecB = list(logB)
                                
                                indep = False
                                for i in range(len(vecA)):
                                    for j in range(i+1, len(vecA)):
                                        if vecA[i]*vecB[j] - vecA[j]*vecB[i] != 0:
                                            indep = True
                                            break
                                    if indep:
                                        break
                                
                                if indep:
                                    neg_q = True
        except Exception:
            pass

    return [neg_q]