import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Named object bindings for the witness namespace
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
    "H_1: G is a group acting linearly on a vector space V",
    "H_2: W_1 and W_2 are subspaces of V",
    "¬Q: The intersection Stab_G(W_1) \cap Stab_G(W_2) is not a subgroup of the setwise stabilizer Stab_G(W_1 + W_2)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G, W1, W2 = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group acting linearly on a vector space V
    h1_ok = False
    G_full = []
    try:
        if isinstance(G, (list, tuple)) and len(G) > 0:
            first = G[0]
            if isinstance(first, Matrix):
                n = first.shape[0]
            elif isinstance(first, (list, tuple)) and len(first) > 0:
                n = len(first)
            else:
                n = -1
                
            if n > 0:
                I = eye(n)
                is_group = True
                G_mats = []
                for g in G:
                    if isinstance(g, (list, tuple)):
                        try:
                            g_mat = Matrix(g)
                        except Exception:
                            is_group = False
                            break
                    else:
                        g_mat = g
                    
                    if not isinstance(g_mat, Matrix) or g_mat.shape != (n, n) or g_mat.det() == 0:
                        is_group = False
                        break
                    G_mats.append(g_mat)
                
                if is_group:
                    G_elements = set()
                    queue = []
                    for g in G_mats:
                        t_g = tuple(g)
                        if t_g not in G_elements:
                            G_elements.add(t_g)
                            queue.append(g)
                    
                    head = 0
                    # Generate the full group (up to a reasonable finite limit)
                    while head < len(queue):
                        if len(queue) > 1024:
                            is_group = False
                            break
                        current = queue[head]
                        head += 1
                        for g in G_mats:
                            nxt = current * g
                            t_nxt = tuple(nxt)
                            if t_nxt not in G_elements:
                                G_elements.add(t_nxt)
                                queue.append(nxt)
                                
                if is_group and tuple(I) in G_elements:
                    h1_ok = True
                    G_full = queue
    except Exception:
        h1_ok = False

    # H_2: W_1 and W_2 are subspaces of V
    h2_ok = False
    try:
        if h1_ok:
            n = G_full[0].shape[0]
            def check_W(W):
                if isinstance(W, (list, tuple)):
                    for w in W:
                        if isinstance(w, Matrix):
                            if w.shape[0] != n or w.shape[1] != 1:
                                return False
                        elif isinstance(w, (list, tuple)):
                            if len(w) != n:
                                return False
                        else:
                            return False
                    return True
                elif isinstance(W, Matrix):
                    return W.shape[0] == n
                return False
            
            if check_W(W1) and check_W(W2):
                h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The intersection Stab_G(W_1) \cap Stab_G(W_2) is not a subgroup of the setwise stabilizer Stab_G(W_1 + W_2)
    neg_q_ok = False
    try:
        if h1_ok and h2_ok:
            n = G_full[0].shape[0]
            
            def to_mat(W):
                if isinstance(W, (list, tuple)):
                    if len(W) == 0:
                        return zeros(n, 1)
                    cols = []
                    for w in W:
                        if isinstance(w, Matrix):
                            cols.append(w)
                        else:
                            cols.append(Matrix(w))
                    return Matrix.hstack(*cols)
                return W
                
            M1 = to_mat(W1)
            M2 = to_mat(W2)
            M_sum = Matrix.hstack(M1, M2)
            
            rank_M1 = M1.rank()
            rank_M2 = M2.rank()
            rank_M_sum = M_sum.rank()
            
            def stabilizes(g, M, rank_M):
                if rank_M == n or rank_M == 0:
                    return True
                combined = Matrix.hstack(M, g * M)
                return combined.rank() == rank_M
                
            stab_W1 = [g for g in G_full if stabilizes(g, M1, rank_M1)]
            stab_W2 = [g for g in G_full if stabilizes(g, M2, rank_M2)]
            stab_sum = [g for g in G_full if stabilizes(g, M_sum, rank_M_sum)]
            
            intersection = [g for g in stab_W1 if g in stab_W2]
            
            # Check if intersection is a subgroup (subset) of stab_sum
            is_subgroup = all(g in stab_sum for g in intersection)
            neg_q_ok = not is_subgroup
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]