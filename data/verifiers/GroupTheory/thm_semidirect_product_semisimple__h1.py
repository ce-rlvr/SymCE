import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_normal(H, G):
    """Check if H is a normal subgroup of G."""
    for g in G.generators:
        for h in H.generators:
            if not H.contains(g * h * ~g):
                return False
    return True

def is_subgroup(H, G):
    """Check if H is a subgroup of G."""
    for h in H.generators:
        if not G.contains(h):
            return False
    return True

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    'Semidirect Products in Semisimple Groups are Direct'
    """
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a semisimple group
    def check_h1():
        try:
            if G.order() == 1:
                return False
            # A finite group is semisimple iff it is a direct product of non-abelian simple groups.
            # This implies it is perfect and has no non-trivial abelian normal subgroups.
            if G.derived_subgroup().order() != G.order():
                return False
            for n_sub in G.normal_subgroups():
                if n_sub.order() > 1 and n_sub.is_abelian:
                    return False
            return True
        except Exception:
            return False

    h1_ok = check_h1()
    
    # H_2: N is a normal subgroup of G
    def check_h2():
        try:
            return is_subgroup(N, G) and is_normal(N, G)
        except Exception:
            return False
            
    h2_ok = check_h2()
    
    # H_3: H is a subgroup of G such that G is the internal semidirect product of N and H
    def check_h3():
        try:
            if not is_subgroup(H, G):
                return False
            # For internal semidirect product, we need |N| * |H| == |G| and N ∩ H = {1}
            if N.order() * H.order() != G.order():
                return False
            # Check trivial intersection
            if N.order() < H.order():
                small, large = N, H
            else:
                small, large = H, N
            for g in small.generate():
                if not g.is_Identity and large.contains(g):
                    return False
            return True
        except Exception:
            return False
            
    h3_ok = check_h3()
    
    # neg_Q: H is NOT a normal subgroup of G, OR G is NOT the internal direct product of N and H
    def check_neg_q():
        try:
            # Since N is normal, N ∩ H = {1}, and NH = G (from hypotheses),
            # G is the internal direct product of N and H IF AND ONLY IF H is normal in G.
            # Thus, the conclusion fails exactly when H is NOT normal in G.
            return not is_normal(H, G)
        except Exception:
            return False
            
    neg_q_ok = check_neg_q()
    
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G such that G is the internal semidirect product of N and H",
    "¬Q: H is not a normal subgroup of G, or G is not the internal direct product of N and H"
]

N_HYP = 3
NEG_Q_INDEX = 3