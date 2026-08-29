import sympy
from sympy import Matrix, eye, zeros
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

CONDITION_LABELS = [
    "H_1: T is a diagonalizable linear operator on V",
    "H_2: W is a subspace of V that is invariant under T",
    "¬Q: The restriction operator T|_W is not diagonalizable on W"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_diagonalizable_over_Z(M):
    if not M.is_square:
        return False
    if not M.is_diagonalizable():
        return False
    evals = M.eigenvals()
    for val in evals:
        if val.is_integer != True:
            return False
    
    vects = M.eigenvects()
    basis = []
    for val, mult, evects in vects:
        for v in evects:
            v_int = v
            lcm = 1
            for i in range(v.rows):
                if v_int[i].is_Rational:
                    lcm = sympy.lcm(lcm, v_int[i].q)
            v_int = v_int * lcm
            g = v_int[0]
            for i in range(1, v_int.rows):
                g = sympy.gcd(g, v_int[i])
            if g != 0:
                v_int = v_int / g
            basis.append(v_int)
            
    if len(basis) != M.rows:
        return False
        
    P = sympy.Matrix.hstack(*basis)
    return abs(P.det()) == 1

def conditions(witness):
    try:
        if hasattr(witness, 'T_is_diagonalizable'):
            h1 = bool(witness.T_is_diagonalizable)
            h2 = bool(witness.W_is_invariant)
            neg_q = not bool(witness.restriction_is_diagonalizable)
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            W = witness.get('W')
        else:
            T, W = witness
            
        if not isinstance(T, sympy.Matrix) or not isinstance(W, sympy.Matrix):
            T = sympy.Matrix(T)
            W = sympy.Matrix(W)
            
        if not T.is_square:
            return [False, False, False]
            
        is_Z = all(x.is_integer == True for x in T) and all(x.is_integer == True for x in W)
        
        if is_Z:
            h1 = is_diagonalizable_over_Z(T)
        else:
            h1 = T.is_diagonalizable()
            
        try:
            if W.rank() != W.cols:
                h2 = False
                C = None
            else:
                C = W.solve(T * W)
                if W * C != T * W:
                    h2 = False
                else:
                    if is_Z:
                        h2 = all(x.is_integer == True for x in C)
                    else:
                        h2 = True
        except Exception:
            h2 = False
            C = None
            
        if C is None:
            neg_q = False
        else:
            if is_Z:
                neg_q = not is_diagonalizable_over_Z(C)
            else:
                neg_q = not C.is_diagonalizable()
                
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass
        
    return [False, False, False]