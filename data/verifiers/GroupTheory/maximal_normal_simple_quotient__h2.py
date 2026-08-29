import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4) # V4 is isomorphic to a subgroup of A4, but we'll just provide standard groups
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def normal_subgroups(G):
    """Return a list of all normal subgroups of G."""
    # SymPy's normal_subgroups() returns a list of PermutationGroup objects
    try:
        return G.normal_subgroups()
    except Exception:
        return []

def is_normal(G, M):
    """Check if M is a normal subgroup of G."""
    try:
        if not M.is_subgroup(G):
            return False
        return G.is_normal(M)
    except Exception:
        return False

def is_maximal_normal(G, M):
    """
    Evaluate if M is a maximal normal subgroup.
    If the 'proper' hypothesis is dropped, M = G might be considered the maximal 
    element in the poset of all normal subgroups. We evaluate it literally:
    M is a normal subgroup, and there is no normal subgroup N strictly containing M.
    """
    try:
        if not is_normal(G, M):
            return False
        
        m_order = M.order()
        g_order = G.order()
        
        # Standard definition requires M to be proper (M != G).
        # However, to expose the dropped hypothesis (properness), we evaluate 
        # the literal condition: no normal subgroup strictly contains M.
        # If M == G, no normal subgroup strictly contains G, so it returns True.
        # If M is a proper maximal normal subgroup, the only normal subgroup 
        # strictly containing M is G.
        
        # To match the standard mathematical intent of "maximal normal subgroup" 
        # while allowing the counterexample, we check if there is any normal N 
        # strictly between M and G.
        for N in normal_subgroups(G):
            n_order = N.order()
            if n_order > m_order and n_order < g_order:
                if M.is_subgroup(N):
                    return False
                    
        # If M == G, the loop doesn't find anything, we return True (exposing the bug).
        # If M is proper, we must ensure it's actually maximal.
        if m_order == g_order:
            return True
            
        return True
    except Exception:
        return False

def is_simple_quotient(G, M):
    """
    Evaluate if the quotient group G/M is simple.
    A group is simple if it is non-trivial and has no proper non-trivial normal subgroups.
    """
    try:
        if not is_normal(G, M):
            return False
            
        m_order = M.order()
        g_order = G.order()
        q_order = g_order // m_order
        
        # The trivial group is not simple
        if q_order == 1:
            return False
            
        # By the correspondence theorem, G/M is simple iff there are no normal 
        # subgroups of G strictly between M and G.
        for N in normal_subgroups(G):
            n_order = N.order()
            if n_order > m_order and n_order < g_order:
                if M.is_subgroup(N):
                    return False
                    
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, M), check the remaining hypotheses and the negated conclusion.
    """
    try:
        G, M = witness
    except Exception:
        return [False, False]
        
    # H1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # neg_Q: M is a maximal normal subgroup of G if and only if the quotient group G/M is simple.
    # We want this equivalence to FAIL (so neg_Q is True).
    try:
        p = is_maximal_normal(G, M)
        q = is_simple_quotient(G, M)
        neg_q_ok = (p != q)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The equivalence (M is a maximal normal subgroup iff G/M is simple) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1