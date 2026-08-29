import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup for standard small groups
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup(Permutation(0))

def groups_equal(G1, G2):
    """Check if two permutation groups are equal by comparing order and generators."""
    try:
        if G1.order() != G2.order():
            return False
        for g in G1.generators:
            if g not in G2:
                return False
        return True
    except Exception:
        return False

def is_normal_series(G, series):
    """
    Check if `series` is a valid normal series for G.
    A normal series for G must start with G, and each subsequent group 
    must be a normal subgroup of the previous one.
    """
    try:
        if not isinstance(series, (list, tuple)):
            return False
        if len(series) == 0:
            return False
        if not groups_equal(series[0], G):
            return False
            
        for i in range(len(series) - 1):
            H1 = series[i]
            H2 = series[i+1]
            
            # Check if H2 is a subgroup of H1
            for h in H2.generators:
                if h not in H1:
                    return False
                    
            # Check if H2 is normal in H1
            # It suffices to check that generators of H1 conjugate generators of H2 into H2
            for g in H1.generators:
                for h in H2.generators:
                    if (g * h * ~g) not in H2:
                        return False
                    if (~g * h * g) not in H2:
                        return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Given a witness (G, A, B), check the hypotheses and the negated conclusion.
    """
    try:
        G, A, B = witness
    except Exception:
        return [False, False]
    
    # H_1: A and B are normal series for G
    try:
        h1 = is_normal_series(G, A) and is_normal_series(G, B)
    except Exception:
        h1 = False
        
    # ¬Q: A and B DO NOT have equivalent refinements
    try:
        # The product of the orders of the factor groups of any refinement of A is |G|/|A[-1]|.
        # If A and B have equivalent refinements, the multiset of factor groups must be the same,
        # which implies the product of their orders must be equal.
        # Therefore, |G|/|A[-1]| == |G|/|B[-1]|, which means |A[-1]| == |B[-1]|.
        # If the endpoints have different orders, they definitely DO NOT have equivalent refinements.
        # (For solvable groups, which any small witness will be, this is also a sufficient condition).
        neg_q = (A[-1].order() != B[-1].order())
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are normal series for G",
    "¬Q: A and B do not have equivalent refinements"
]

N_HYP = 1
NEG_Q_INDEX = 1