import sympy
from sympy import Matrix, eye
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
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            A = witness.get('A')
            B = witness.get('B')
            H = witness.get('H')
        elif hasattr(witness, 'G') and hasattr(witness, 'A') and hasattr(witness, 'B') and hasattr(witness, 'H'):
            G = witness.G
            A = witness.A
            B = witness.B
            H = witness.H
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            G, A, B, H = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is the special linear group SL(2, Z)
    try:
        g_str = str(G).replace(' ', '').replace('\\mathbb{Z}', 'Z').replace('ZZ', 'Z').upper()
        h1 = g_str in ['SL(2,Z)', 'SPECIALLINEARGROUP(2,Z)', 'SL_2(Z)', 'SL2(Z)']
    except Exception:
        h1 = False

    # H_2: A is the matrix [[1, 2], [0, 1]] in G
    A_mat = None
    try:
        if isinstance(A, (list, tuple)):
            A_mat = Matrix(A)
        else:
            A_mat = A
        h2 = bool(A_mat == Matrix([[1, 2], [0, 1]]))
    except Exception:
        h2 = False

    # H_3: B is the matrix [[1, 0], [2, 1]] in G
    B_mat = None
    try:
        if isinstance(B, (list, tuple)):
            B_mat = Matrix(B)
        else:
            B_mat = B
        h3 = bool(B_mat == Matrix([[1, 0], [2, 1]]))
    except Exception:
        h3 = False

    # neg_Q: H is not isomorphic to the free group of rank 2
    try:
        is_f2 = False
        
        if hasattr(H, 'generators'):
            try:
                gens = list(H.generators)
                if len(gens) == 2:
                    if A_mat is not None and B_mat is not None and ((gens[0] == A_mat and gens[1] == B_mat) or (gens[0] == B_mat and gens[1] == A_mat)):
                        is_f2 = True
                    elif type(H).__name__ == 'FreeGroup':
                        is_f2 = True
            except Exception:
                pass
        
        if not is_f2 and isinstance(H, str):
            h_str = H.replace(' ', '').replace('_', '').upper()
            if h_str in ['F2', 'FREEGROUP(2)', 'FREEGROUPOFRANK2']:
                is_f2 = True
                
        if not is_f2 and isinstance(H, (list, tuple, set)):
            try:
                if len(H) == 2:
                    h_list = list(H)
                    h0_mat = Matrix(h_list[0]) if isinstance(h_list[0], (list, tuple)) else h_list[0]
                    h1_mat = Matrix(h_list[1]) if isinstance(h_list[1], (list, tuple)) else h_list[1]
                    if A_mat is not None and B_mat is not None and ((h0_mat == A_mat and h1_mat == B_mat) or (h0_mat == B_mat and h1_mat == A_mat)):
                        is_f2 = True
            except Exception:
                pass
                
        neg_q = not is_f2
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is the special linear group SL(2, Z)",
    "H_2: A is the matrix with rows (1, 2) and (0, 1)",
    "H_3: B is the matrix with rows (1, 0) and (2, 1)",
    "¬Q: H is not isomorphic to the free group of rank 2"
]

N_HYP = 3
NEG_Q_INDEX = 3