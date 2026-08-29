import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
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
    B = []
    G = []
    try:
        if isinstance(witness, dict):
            B = witness.get('B', [])
            if 'G' in witness:
                G.extend(witness['G'] if isinstance(witness['G'], list) else [witness['G']])
            if 'g' in witness:
                G.append(witness['g'])
        elif isinstance(witness, tuple) and len(witness) == 2:
            B, g = witness
            G.append(g)
        else:
            if hasattr(witness, 'B'):
                B = witness.B
            if hasattr(witness, 'G'):
                G.extend(witness.G if isinstance(witness.G, list) else [witness.G])
            if hasattr(witness, 'g'):
                G.append(witness.g)
    except Exception:
        pass

    # H1: V is a vector space over a field F
    h1 = False
    try:
        if isinstance(B, list) and len(B) > 0:
            B_mat = []
            for v in B:
                if isinstance(v, (list, tuple)):
                    m = Matrix(v)
                    if m.shape[1] != 1:
                        m = m.T
                    if m.shape[1] == 1:
                        B_mat.append(m)
                elif isinstance(v, Matrix):
                    if v.shape[1] != 1:
                        B_mat.append(v.T)
                    else:
                        B_mat.append(v)
            if len(B_mat) == len(B):
                B = B_mat
                n = B[0].shape[0]
                if all(v.shape == (n, 1) for v in B):
                    h1 = True
    except Exception:
        pass

    # H2: GL(V) is the general linear group of V
    # This is definitional; if V is valid, GL(V) exists.
    h2 = h1

    # H3: B is a basis for the vector space V
    h3 = False
    try:
        if h1:
            n = len(B)
            if B[0].shape[0] == n:
                M = Matrix.hstack(*B)
                if M.det() != 0:
                    h3 = True
    except Exception:
        pass

    # neg_Q: The pointwise stabilizer of the set B in G is not the trivial subgroup
    # i.e., there exists a transformation g in G that fixes B pointwise but is not the identity.
    neg_q = False
    try:
        if h1 and h3:
            n = len(B)
            zero_vec = zeros(n, 1)
            for g in G:
                fixes_B = False
                is_not_id = False
                
                if callable(g):
                    try:
                        fixes_B = all(Matrix(g(v)) == v for v in B)
                        if Matrix(g(zero_vec)) != zero_vec:
                            is_not_id = True
                        elif Matrix(g(2 * B[0])) != 2 * B[0]:
                            is_not_id = True
                        elif Matrix(g(sum(B, zero_vec))) != sum(B, zero_vec):
                            is_not_id = True
                    except Exception:
                        pass
                elif isinstance(g, tuple) and len(g) == 2:
                    try:
                        A, b = g
                        A = Matrix(A)
                        b = Matrix(b)
                        if b.shape[1] != 1: 
                            b = b.T
                        fixes_B = all(A * v + b == v for v in B)
                        if A != eye(n) or b != zero_vec:
                            is_not_id = True
                    except Exception:
                        pass
                elif isinstance(g, dict):
                    try:
                        fixes_B = True
                        for v in B:
                            matched = False
                            for k, val in g.items():
                                km = Matrix(k)
                                if km.shape[1] != 1: km = km.T
                                if km == v:
                                    vm = Matrix(val)
                                    if vm.shape[1] != 1: vm = vm.T
                                    if vm == v:
                                        matched = True
                                    break
                            if not matched:
                                fixes_B = False
                                break
                        if fixes_B:
                            for k, val in g.items():
                                km = Matrix(k)
                                if km.shape[1] != 1: km = km.T
                                vm = Matrix(val)
                                if vm.shape[1] != 1: vm = vm.T
                                if km != vm:
                                    is_not_id = True
                                    break
                    except Exception:
                        pass
                
                if fixes_B and is_not_id:
                    neg_q = True
                    break
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: GL(V) is the general linear group of V",
    "H_3: B is a basis for the vector space V",
    "¬Q: The pointwise stabilizer of the set B in G is not the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3