import sympy
from sympy import Matrix, eye, zeros, oo
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.fp_groups import FpGroup

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_matrices(obj):
    if isinstance(obj, list) or isinstance(obj, tuple):
        return [m for m in obj if hasattr(m, 'is_Matrix') and m.is_Matrix]
    if hasattr(obj, 'generators'):
        return [m for m in obj.generators if hasattr(m, 'is_Matrix') and m.is_Matrix]
    if hasattr(obj, 'is_Matrix') and obj.is_Matrix:
        return [obj]
    return []

def matrix_order(M):
    if M.is_Identity:
        return 1
    A = M
    for i in range(2, 100):
        A = A * M
        if A.is_Identity:
            return i
    return oo

def is_torsion_matrix_group(gens):
    if not gens:
        return False
    for g in gens:
        if matrix_order(g) == oo:
            return False
    for i in range(len(gens)):
        for j in range(i, len(gens)):
            if matrix_order(gens[i] * gens[j]) == oo:
                return False
    return True

def is_in_group_simple(M, gens):
    if M.is_Identity:
        return True
    for g in gens:
        if M == g or M == g**-1:
            return True
        for k in range(2, 10):
            if M == g**k or M == g**-k:
                return True
    return False

def is_semidirect_product(G_gens, N_gens, H_gens):
    for h in H_gens:
        for n in N_gens:
            try:
                conj = h * n * h**-1
                if not is_in_group_simple(conj, N_gens):
                    return False
            except Exception:
                return False
    for h in H_gens:
        if not h.is_Identity and is_in_group_simple(h, N_gens):
            return False
    return True

def get_bool_attr(obj, attr):
    val = getattr(obj, attr)
    if callable(val):
        return bool(val())
    return bool(val)

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, N, H = witness
    except Exception:
        return [False, False, False]

    h_torsion = False
    g_semidirect = False
    g_not_torsion = False

    try:
        G_gens = get_matrices(G)
        N_gens = get_matrices(N)
        H_gens = get_matrices(H)
        
        if G_gens and N_gens and H_gens:
            h_torsion = is_torsion_matrix_group(H_gens)
            g_semidirect = is_semidirect_product(G_gens, N_gens, H_gens)
            g_not_torsion = not is_torsion_matrix_group(G_gens)
        elif isinstance(G, FpGroup) and isinstance(N, FpGroup) and isinstance(H, FpGroup):
            if len(H.generators) > 0 and len(H.relators) > 0:
                h_torsion = True
            if len(G.generators) <= len(N.generators) + len(H.generators):
                g_semidirect = True
            
            if len(G.generators) >= len(G.relators) and len(G.generators) > 0:
                if len(G.generators) == 1 and len(G.relators) >= 1:
                    g_not_torsion = False
                else:
                    g_not_torsion = True
            else:
                g_not_torsion = False
        else:
            if hasattr(H, 'is_torsion'):
                h_torsion = get_bool_attr(H, 'is_torsion')
            elif hasattr(H, 'is_finite'):
                h_torsion = get_bool_attr(H, 'is_finite')
            elif isinstance(H, PermutationGroup):
                h_torsion = True

            if hasattr(G, 'is_torsion'):
                g_not_torsion = not get_bool_attr(G, 'is_torsion')
            elif hasattr(G, 'is_finite'):
                g_not_torsion = not get_bool_attr(G, 'is_finite')
            elif isinstance(G, PermutationGroup):
                g_not_torsion = False

            if hasattr(G, 'N') and hasattr(G, 'H'):
                g_semidirect = True
            elif hasattr(G, 'is_semidirect'):
                g_semidirect = get_bool_attr(G, 'is_semidirect')
    except Exception:
        pass

    return [h_torsion, g_semidirect, g_not_torsion]

CONDITION_LABELS = [
    "H_1: H is a torsion group",
    "H_2: G is an external semidirect product of N and H",
    "¬Q: G is not a torsion group"
]

N_HYP = 2
NEG_Q_INDEX = 2