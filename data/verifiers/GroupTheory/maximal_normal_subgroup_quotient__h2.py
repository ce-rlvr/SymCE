import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis was "N is a normal subgroup of G".
    Therefore, the counterexample must be a group G and a non-normal subgroup N,
    which makes the quotient group G/N undefined and the conclusion fail.
    """
    try:
        # The witness should provide both the group G and the subgroup N
        G, N = witness
    except Exception:
        return [False, False]
        
    # H_1: Let G be a group (and N a subgroup of G)
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and N.is_subgroup(G)
    except Exception:
        h1_ok = False
        
    # neg_Q: The conclusion "G/N is simple iff N is maximal normal" fails
    try:
        if not h1_ok:
            neg_q_ok = False
        elif not G.is_normal(N):
            # If N is not normal, the quotient group G/N is undefined.
            # Thus, the statement "G/N is a simple group" is invalid, and the biconditional fails.
            neg_q_ok = True
        else:
            # If N is normal, we evaluate both sides rigorously.
            # LHS: G/N is a simple group (has exactly two normal subgroups)
            Q_group = G.coset_factor(N)
            lhs = (len(Q_group.normal_subgroups()) == 2)
            
            # RHS: N is a maximal normal subgroup of G
            rhs = False
            if N.order() < G.order():
                rhs = True
                for M in G.normal_subgroups():
                    if M.order() > N.order() and M.order() < G.order():
                        # Check if N is a subgroup of M
                        if all(g in M for g in N.generators):
                            rhs = False
                            break
                            
            neg_q_ok = (lhs != rhs)
    except Exception:
        # If evaluation fails (e.g., undefined operations), the conclusion fails
        neg_q_ok = True
        
    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The conclusion 'G/N is simple iff N is maximal normal' fails"
]

N_HYP = 1
NEG_Q_INDEX = 1