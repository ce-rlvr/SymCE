import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Matrix

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
    try:
        # Extract G and B from the witness
        if isinstance(witness, dict):
            G = witness.get('G', witness.get('g', []))
            B = witness.get('B', witness.get('b', []))
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                G, B = witness
            elif len(witness) == 4:
                _, _, G, B = witness
            else:
                return [False, False, False, False]
        else:
            G = getattr(witness, 'G', getattr(witness, 'g', []))
            B = getattr(witness, 'B', getattr(witness, 'b', []))
            
        if not G or not B:
            return [False, False, False, False]
            
        # Convert to SymPy matrices
        G_mats = []
        for g in G:
            if not isinstance(g, sympy.MatrixBase):
                G_mats.append(sympy.Matrix(g))
            else:
                G_mats.append(g)
        G = G_mats
        
        B_mats = []
        for b in B:
            if not isinstance(b, sympy.MatrixBase):
                B_mats.append(sympy.Matrix(b))
            else:
                B_mats.append(b)
        B = B_mats
        
        n = G[0].shape[0]
        
        # H1: V is a vector space over a field F
        h1 = True
        try:
            for g in G:
                if g.shape != (n, n):
                    h1 = False
            for b in B:
                if b.shape != (n, 1):
                    h1 = False
        except Exception:
            h1 = False

        # H2: G is a subgroup of GL(V) acting naturally on V by linear transformations
        h2 = True
        try:
            I = sympy.eye(n)
            if not any(g == I for g in G):
                h2 = False
            else:
                for g in G:
                    if g.shape[0] != g.shape[1] or g.det() == 0:
                        h2 = False
                        break
                if h2:
                    # Check closure under multiplication
                    G_set = {tuple(tuple(row) for row in g.tolist()) for g in G}
                    for g1 in G:
                        for g2 in G:
                            prod = g1 * g2
                            prod_tuple = tuple(tuple(row) for row in prod.tolist())
                            if prod_tuple not in G_set:
                                h2 = False
                                break
                        if not h2:
                            break
        except Exception:
            h2 = False

        # H3: B is a basis for the vector space V
        h3 = False
        try:
            if len(B) == n:
                B_mat = sympy.Matrix.hstack(*B)
                if B_mat.shape == (n, n) and B_mat.det() != 0:
                    h3 = True
        except Exception:
            h3 = False

        # ¬Q: The pointwise stabilizer of the set B in G is NOT the trivial subgroup
        # i.e., there exists g in G, g != I, such that g * b == b for all b in B
        neg_q = False
        try:
            I = sympy.eye(n)
            for g in G:
                if g != I:
                    fixes_all = True
                    for b in B:
                        if g * b != b:
                            fixes_all = False
                            break
                    if fixes_all:
                        neg_q = True
                        break
        except Exception:
            neg_q = False

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: G is a subgroup of GL(V) acting naturally on V by linear transformations",
    "H_3: B is a basis for the vector space V",
    "¬Q: The pointwise stabilizer of B in G contains a non-identity transformation"
]

N_HYP = 3
NEG_Q_INDEX = 3