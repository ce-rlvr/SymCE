import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_subgroup(subgroup, group):
    try:
        return subgroup.is_subgroup(group)
    except AttributeError:
        try:
            for g in subgroup.generators:
                if not group.contains(g):
                    return False
            return True
        except Exception:
            return False

def is_normal(subgroup, group):
    try:
        return subgroup.is_normal(group)
    except AttributeError:
        try:
            if not is_subgroup(subgroup, group):
                return False
            for g in group.generators:
                for h in subgroup.generators:
                    if not subgroup.contains(~g * h * g):
                        return False
            return True
        except Exception:
            return False

def conditions(witness):
    try:
        G, N, H, K = witness
    except Exception:
        return [False] * 6

    def check_h1():
        try:
            return is_normal(N, G)
        except Exception:
            return False

    def check_h2():
        try:
            return is_subgroup(H, G)
        except Exception:
            return False

    def check_h3():
        try:
            if not is_normal(N, G): return False
            if not is_subgroup(H, G): return False
            if N.intersect(H).order() != 1: return False
            if N.order() * H.order() != G.order(): return False
            return True
        except Exception:
            return False

    def check_h4():
        try:
            return is_normal(K, G)
        except Exception:
            return False

    def check_h5():
        try:
            return is_subgroup(K, N)
        except Exception:
            return False

    def check_neg_q():
        try:
            # If K is not normal in G or not a subgroup of N, the quotient structures 
            # are invalid, meaning the conclusion fails.
            if not is_normal(K, G):
                return True
            if not is_subgroup(K, N):
                return True
                
            HK = PermutationGroup(H.generators + K.generators)
            
            # Check if N/K and HK/K form an internal semidirect product in G/K
            
            # 1. N/K is normal in G/K <=> N is normal in G
            if not is_normal(N, G):
                return True
                
            # 2. HK/K is a subgroup of G/K <=> HK is a subgroup of G
            if not is_subgroup(HK, G):
                return True
                
            # 3. (N/K) \cap (HK/K) == 1_{G/K} <=> N \cap HK == K
            N_int_HK = N.intersect(HK)
            if N_int_HK.order() != K.order():
                return True
                
            # 4. (N/K) * (HK/K) == G/K <=> N * HK == G
            N_HK = PermutationGroup(N.generators + HK.generators)
            if N_HK.order() != G.order():
                return True
                
            return False
        except Exception:
            return False

    return [check_h1(), check_h2(), check_h3(), check_h4(), check_h5(), check_neg_q()]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "H_3: G is the internal semidirect product of N and H",
    "H_4: K is a normal subgroup of G",
    "H_5: K is a subgroup of N",
    "¬Q: G/K is not isomorphic to the internal semidirect product of N/K and HK/K"
]

N_HYP = 5
NEG_Q_INDEX = 5