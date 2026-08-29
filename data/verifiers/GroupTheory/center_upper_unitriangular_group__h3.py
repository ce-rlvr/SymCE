import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            n = witness.get('n')
            G = witness.get('G')
        elif isinstance(witness, tuple) and len(witness) == 3:
            F, n, G = witness
        else:
            F, n, G = None, None, None
    except Exception:
        F, n, G = None, None, None

    # H_1: F is a field
    try:
        if hasattr(F, 'is_Field'):
            h1 = bool(F.is_Field)
        elif F in [sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes]:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: n is an integer such that n >= 3
    try:
        h2 = isinstance(n, int) and n >= 3
    except Exception:
        h2 = False

    # ¬Q: Z(G) does not consist exactly of those matrices in G whose non-diagonal entries are zero except possibly the entry in the first row and n-th column
    try:
        if hasattr(G, 'generators'):
            gens = G.generators
            if callable(getattr(G, 'generate', None)):
                G_elements = list(G.generate())
            elif hasattr(G, 'elements'):
                G_elements = list(G.elements)
            else:
                G_elements = list(G)
        else:
            G_elements = list(G)
            gens = G_elements

        # Convert elements to SymPy matrices if they aren't already
        G_mats = []
        for A in G_elements:
            if hasattr(A, 'is_Matrix') and A.is_Matrix:
                G_mats.append(A)
            else:
                G_mats.append(sympy.Matrix(A))
        G_elements = G_mats

        gens_mats = []
        for A in gens:
            if hasattr(A, 'is_Matrix') and A.is_Matrix:
                gens_mats.append(A)
            else:
                gens_mats.append(sympy.Matrix(A))
        gens = gens_mats

        # Compute the center Z(G)
        Z_G = []
        for A in G_elements:
            is_center = True
            for B in gens:
                if A * B != B * A:
                    is_center = False
                    break
            if is_center:
                Z_G.append(A)

        # Compute the expected set of matrices
        expected_Z = []
        for A in G_elements:
            ok = True
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    # 0-indexed: first row is 0, n-th column is n-1
                    if i == 0 and j == n - 1:
                        continue
                    if A[i, j] != 0:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                expected_Z.append(A)

        def is_subset(list1, list2):
            return all(any(X == Y for Y in list2) for X in list1)

        # Check if Z_G and expected_Z are exactly the same set of matrices
        q = is_subset(Z_G, expected_Z) and is_subset(expected_Z, Z_G)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is an integer such that n >= 3",
    "¬Q: Z(G) does not consist exactly of those matrices in G whose non-diagonal entries are zero except possibly the entry in the first row and n-th column"
]

N_HYP = 2
NEG_Q_INDEX = 2