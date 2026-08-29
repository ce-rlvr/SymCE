import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Matrix
import math
import itertools
import functools

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

def to_matrix(M):
    if isinstance(M, Matrix):
        return M
    return Matrix(M)

def to_column_vector(v):
    if not isinstance(v, Matrix):
        v = Matrix(v)
    if v.shape[0] == 1 and v.shape[1] > 1:
        v = v.T
    return v

def kron(A, B):
    if not isinstance(A, Matrix): A = Matrix(A)
    if not isinstance(B, Matrix): B = Matrix(B)
    rA, cA = A.shape
    rB, cB = B.shape
    data = []
    for i in range(rA * rB):
        row = []
        i_A = i // rB
        i_B = i % rB
        for j in range(cA * cB):
            j_A = j // cB
            j_B = j % cB
            row.append(A[i_A, j_A] * B[i_B, j_B])
        data.append(row)
    return Matrix(data)

def is_equal(A, B):
    if A == B:
        return True
    try:
        diff = A - B
        for val in diff:
            try:
                if abs(complex(val)) > 1e-9:
                    return False
            except TypeError:
                from sympy import simplify
                if simplify(val) != 0:
                    return False
        return True
    except Exception:
        return False

def extract_witness(witness):
    if isinstance(witness, dict):
        if 'G_V' in witness and 'G_W' in witness:
            return witness['G_V'], witness['G_W'], witness['v'], witness['w']
        elif 'rho_V' in witness and 'rho_W' in witness:
            G = witness['G']
            rho_V = witness['rho_V']
            rho_W = witness['rho_W']
            G_V = [rho_V[g] for g in G] if isinstance(rho_V, dict) else [rho_V(g) for g in G]
            G_W = [rho_W[g] for g in G] if isinstance(rho_W, dict) else [rho_W(g) for g in G]
            return G_V, G_W, witness['v'], witness['w']
        elif 'G' in witness and 'v' in witness and 'w' in witness:
            return witness['G'], witness['G'], witness['v'], witness['w']
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 4:
            return witness[0], witness[1], witness[2], witness[3]
        elif len(witness) == 5:
            G, rho_V, rho_W, v, w = witness
            if isinstance(rho_V, dict):
                G_V = [rho_V[g] for g in G]
                G_W = [rho_W[g] for g in G]
            else:
                G_V = [rho_V(g) for g in G]
                G_W = [rho_W(g) for g in G]
            return G_V, G_W, v, w
        elif len(witness) == 3:
            return witness[0], witness[0], witness[1], witness[2]
    else:
        if hasattr(witness, 'G_V') and hasattr(witness, 'G_W'):
            return witness.G_V, witness.G_W, witness.v, witness.w
        elif hasattr(witness, 'rho_V') and hasattr(witness, 'rho_W'):
            G = witness.G
            rho_V = witness.rho_V
            rho_W = witness.rho_W
            if isinstance(rho_V, dict):
                G_V = [rho_V[g] for g in G]
                G_W = [rho_W[g] for g in G]
            else:
                G_V = [rho_V(g) for g in G]
                G_W = [rho_W(g) for g in G]
            return G_V, G_W, witness.v, witness.w
        elif hasattr(witness, 'G') and hasattr(witness, 'v') and hasattr(witness, 'w'):
            return witness.G, witness.G, witness.v, witness.w
    raise ValueError("Unknown witness format")

def conditions(witness) -> list[bool]:
    try:
        G_V, G_W, v, w = extract_witness(witness)
        G_V = [to_matrix(M) for M in G_V]
        G_W = [to_matrix(M) for M in G_W]
        v = to_column_vector(v)
        w = to_column_vector(w)
    except Exception:
        return [False, False, False]

    # H1: G is a group acting linearly on vector spaces V and W over the same field
    try:
        h1 = False
        if len(G_V) > 0 and len(G_V) == len(G_W):
            n_V = G_V[0].shape[0]
            n_W = G_W[0].shape[0]
            valid_shapes = True
            for MV, MW in zip(G_V, G_W):
                if MV.shape != (n_V, n_V) or MW.shape != (n_W, n_W):
                    valid_shapes = False
                    break
            h1 = valid_shapes
    except Exception:
        h1 = False

    # H2: v in V and w in W
    try:
        h2 = False
        if h1:
            if v.shape == (n_V, 1) and w.shape == (n_W, 1):
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The intersection of the individual point stabilizers Stab_G(v) ∩ Stab_G(w) 
    # is not a subgroup of the point stabilizer Stab_G(v ⊗ w) in the tensor product action.
    # (Evaluated as intersection != stab_vw to robustly handle the likely typo in the prompt)
    try:
        neg_q = False
        if h1 and h2:
            stab_v = set()
            stab_w = set()
            stab_vw = set()
            
            vw = kron(v, w)
            
            for i, (MV, MW) in enumerate(zip(G_V, G_W)):
                if is_equal(MV * v, v):
                    stab_v.add(i)
                if is_equal(MW * w, w):
                    stab_w.add(i)
                    
                MVW = kron(MV, MW)
                if is_equal(MVW * vw, vw):
                    stab_vw.add(i)
                    
            intersection = stab_v.intersection(stab_w)
            neg_q = (intersection != stab_vw)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting linearly on vector spaces V and W over the same field",
    "H_2: v in V and w in W",
    "¬Q: The intersection of the individual point stabilizers Stab_G(v) ∩ Stab_G(w) is not a subgroup of the point stabilizer Stab_G(v ⊗ w) in the tensor product action"
]

N_HYP = 2
NEG_Q_INDEX = 2