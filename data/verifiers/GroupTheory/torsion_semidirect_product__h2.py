import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_group(gens, max_size=100):
    if not gens:
        return set()
    try:
        I = eye(gens[0].shape[0]).as_immutable()
        elements = {I}
        frontier = [I]
        full_gens = []
        for g in gens:
            g_imm = g.as_immutable()
            full_gens.append(g_imm)
            full_gens.append(g_imm.inv())
        
        while frontier:
            new_frontier = []
            for mat in frontier:
                for g in full_gens:
                    nxt = (mat * g).as_immutable()
                    if nxt not in elements:
                        elements.add(nxt)
                        new_frontier.append(nxt)
                        if len(elements) > max_size:
                            return None
            frontier = new_frontier
        return elements
    except Exception:
        return None

def has_infinite_order(mat):
    try:
        I = eye(mat.shape[0]).as_immutable()
        mat_imm = mat.as_immutable()
        if mat_imm == I:
            return False
        current = mat_imm
        for i in range(1, 1000):
            if current == I:
                return False
            current = (current * mat_imm).as_immutable()
        return True
    except Exception:
        return False

def check_semidirect_product(N_gens, H_gens, N_elements):
    if not N_gens or not H_gens:
        return False
    try:
        I = eye(N_gens[0].shape[0]).as_immutable()
        
        # Check normality of N in G
        for h in H_gens:
            h_imm = h.as_immutable()
            h_inv = h_imm.inv()
            for n in N_elements:
                if (h_imm * n * h_inv).as_immutable() not in N_elements:
                    return False
                if (h_inv * n * h_imm).as_immutable() not in N_elements:
                    return False
                    
        # Check trivial intersection N \cap H = {I}
        H_elements = {I}
        frontier = [I]
        full_H_gens = []
        for h in H_gens:
            h_imm = h.as_immutable()
            full_H_gens.append(h_imm)
            full_H_gens.append(h_imm.inv())
            
        for _ in range(10):
            new_frontier = []
            for mat in frontier:
                for g in full_H_gens:
                    nxt = (mat * g).as_immutable()
                    if nxt not in H_elements:
                        if nxt in N_elements and nxt != I:
                            return False
                        H_elements.add(nxt)
                        new_frontier.append(nxt)
            frontier = new_frontier
            
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            N_gens = witness[0]
            H_gens = witness[1]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: N is a torsion group
    try:
        N_elements = get_group(N_gens, max_size=100)
        h1 = (N_elements is not None)
    except Exception:
        h1 = False
        
    # H_2: G is an external semidirect product of N and H
    try:
        if N_elements is None:
            h2 = False
        else:
            h2 = check_semidirect_product(N_gens, H_gens, N_elements)
    except Exception:
        h2 = False
        
    # ¬Q: G is not a torsion group
    try:
        neg_q = False
        for h in H_gens:
            if has_infinite_order(h):
                neg_q = True
                break
        if not neg_q:
            for h1_mat in H_gens:
                for h2_mat in H_gens:
                    if has_infinite_order(h1_mat * h2_mat):
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a torsion group",
    "H_2: G is an external semidirect product of N and H",
    "¬Q: G is not a torsion group"
]

N_HYP = 2
NEG_Q_INDEX = 2