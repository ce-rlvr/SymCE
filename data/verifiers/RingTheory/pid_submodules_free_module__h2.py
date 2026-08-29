import sympy
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_form
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys:
      'R': string representing the ring (e.g., 'ZZ')
      'F_gens': int, number of generators of F
      'F_rels': list of lists of ints, relations of F
      'N_gens': list of lists of ints, generators of N (expressed in F's generators)
      'n': int, the rank parameter in the conclusion
    """
    try:
        h1 = False
        if isinstance(witness, dict):
            R = witness.get('R', '')
            # We accept common string representations of PIDs.
            if str(R) in ['ZZ', 'Z', 'QQ', 'Q', 'RR', 'R', 'CC', 'C']:
                h1 = True
    except Exception:
        h1 = False

    try:
        h2 = False
        if isinstance(witness, dict):
            F_gens = witness.get('F_gens', -1)
            N_gens = witness.get('N_gens', [])
            F_rels = witness.get('F_rels', [])
            
            if isinstance(F_gens, int) and F_gens >= 0:
                valid = True
                for gen in N_gens:
                    if not isinstance(gen, list) or len(gen) != F_gens:
                        valid = False
                for rel in F_rels:
                    if not isinstance(rel, list) or len(rel) != F_gens:
                        valid = False
                if valid:
                    if N_gens and not all(x.is_Integer for x in Matrix(N_gens)):
                        valid = False
                    if F_rels and not all(x.is_Integer for x in Matrix(F_rels)):
                        valid = False
                h2 = valid
    except Exception:
        h2 = False

    try:
        neg_q = False
        if isinstance(witness, dict):
            F_gens = witness.get('F_gens', 0)
            F_rels = witness.get('F_rels', [])
            N_gens = witness.get('N_gens', [])
            n = witness.get('n', 0)
            
            if isinstance(n, int) and isinstance(F_gens, int) and F_gens >= 0:
                A_mat = Matrix(N_gens) if N_gens else Matrix(0, F_gens, [])
                B_mat = Matrix(F_rels) if F_rels else Matrix(0, F_gens, [])
                
                M = Matrix(A_mat.tolist() + B_mat.tolist())
                if M.rows == 0 or M.cols == 0:
                    is_free = True
                    rank = 0
                    neg_q = not (is_free and rank <= n)
                else:
                    H = hermite_normal_form(M)
                    H_rows = []
                    for i in range(H.rows):
                        if any(H[i, j] != 0 for j in range(H.cols)):
                            H_rows.append(list(H.row(i)))
                            
                    if not H_rows:
                        is_free = True
                        rank = 0
                        neg_q = not (is_free and rank <= n)
                    else:
                        H_V = Matrix(H_rows)
                        k = H_V.rows
                        
                        if B_mat.rows == 0:
                            is_free = True
                            rank = k
                            neg_q = not (is_free and rank <= n)
                        else:
                            C = B_mat * H_V.T * (H_V * H_V.T).inv()
                            is_integer = True
                            for i in range(C.rows):
                                for j in range(C.cols):
                                    if not C[i, j].is_Integer:
                                        is_integer = False
                            if is_integer:
                                C = C.applyfunc(lambda x: int(x))
                                S = smith_normal_form(C)
                                
                                d_list = []
                                for i in range(min(S.rows, S.cols)):
                                    d_list.append(abs(S[i, i]))
                                    
                                is_free = all(d in (0, 1) for d in d_list)
                                rank = (k - min(C.rows, C.cols)) + sum(1 for d in d_list if d == 0)
                                
                                neg_q = not (is_free and rank <= n)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: N is a submodule of F",
    "¬Q: N is not a free R-module of rank m <= n"
]

N_HYP = 2
NEG_Q_INDEX = 2