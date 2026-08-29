import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    Witness is expected to be a tuple of PermutationGroup objects: (G, N, H)
    """
    
    def is_sub(sub, supergroup):
        for gen in sub.generators:
            if gen not in supergroup:
                return False
        return True

    def is_normal(sub, supergroup):
        if not is_sub(sub, supergroup):
            return False
        for g in supergroup.generators:
            for n in sub.generators:
                if g * n * ~g not in sub:
                    return False
        return True

    def check_H1():
        try:
            G, N, H = witness
            if not (hasattr(G, 'is_group') and G.is_group): return False
            if not (hasattr(N, 'is_group') and N.is_group): return False
            if not (hasattr(H, 'is_group') and H.is_group): return False
            
            if not is_sub(N, G): return False
            if not is_sub(H, G): return False
            if not is_normal(N, G): return False
            
            # Internal semidirect product requires |N| * |H| == |G| and trivial intersection
            if N.order() * H.order() != G.order(): return False
            
            common_count = 0
            for g in N.elements:
                if g in H:
                    common_count += 1
                    if common_count > 1:
                        return False
            return True
        except Exception:
            return False

    def check_H2():
        try:
            G, N, H = witness
            if N.order() == 1: return False
            if not is_normal(N, G): return False
            
            # N is minimal normal iff the normal closure of every non-identity element in N is N itself
            for n in N.elements:
                if n**2 == n:  # Check if n is the identity element
                    continue
                
                conjugates = []
                for g in G.elements:
                    conj = g * n * ~g
                    conjugates.append(conj)
                
                K = PermutationGroup(conjugates)
                if K.order() < N.order():
                    return False
            return True
        except Exception:
            return False

    def check_neg_Q():
        try:
            G, N, H = witness
            if not is_sub(H, G):
                return True
            if H.order() == G.order():
                return True
            
            # H is NOT maximal if there exists some g not in H such that <H, g> is a proper subgroup of G
            for g in G.elements:
                if g not in H:
                    gens = list(H.generators) + [g]
                    K = PermutationGroup(gens)
                    if K.order() < G.order():
                        return True
            return False
        except Exception:
            return False

    return [check_H1(), check_H2(), check_neg_Q()]

CONDITION_LABELS = [
    "H_1: G is the internal semidirect product of normal subgroup N and subgroup H",
    "H_2: N is a minimal normal subgroup of G",
    "¬Q: H is not a maximal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2