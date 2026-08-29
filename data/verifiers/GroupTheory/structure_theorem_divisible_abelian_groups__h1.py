import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for witness expressions
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

def check_divisible(G):
    """
    Checks if the group G is divisible.
    For finitely generated groups (like SymPy's PermutationGroups), 
    the only divisible group is the trivial group.
    """
    if isinstance(G, str):
        divisible_strs = ["GL", "SO", "SU", "Q", "R", "C", "Prüfer", "Z(p^infty)"]
        return any(s in G for s in divisible_strs)

    if hasattr(G, 'is_divisible'):
        val = G.is_divisible
        if callable(val):
            return bool(val())
        return bool(val)
    
    if hasattr(G, 'order'):
        try:
            return G.order() == 1
        except Exception:
            pass
            
    if hasattr(G, 'elements'):
        try:
            return len(list(G.elements)) == 1
        except Exception:
            pass
            
    return False

def check_abelian(G):
    """
    Checks if the group G is abelian.
    """
    if isinstance(G, str):
        non_abelian_strs = ["GL", "SO", "SU", "S3", "S4", "A4", "D4", "Q8"]
        return not any(s in G for s in non_abelian_strs)

    if hasattr(G, 'is_abelian'):
        val = G.is_abelian
        if callable(val):
            return bool(val())
        return bool(val)
        
    return False

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    """
    try:
        h1 = check_divisible(witness)
    except Exception:
        h1 = False
        
    try:
        # The conclusion states that G is isomorphic to a direct sum of copies of Q and Prüfer p-groups.
        # By the Structure Theorem for Divisible Abelian Groups, a group is isomorphic to such a 
        # direct sum IF AND ONLY IF it is both divisible and abelian.
        # Therefore, the conclusion holds iff G is divisible and abelian.
        div = check_divisible(witness)
        ab = check_abelian(witness)
        conclusion_holds = div and ab
        
        # We want the negated conclusion (True when the conclusion FAILS)
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a divisible group",
    "¬Q: G is not isomorphic to a direct sum of copies of Q and Prüfer p-groups"
]

N_HYP = 1
NEG_Q_INDEX = 1