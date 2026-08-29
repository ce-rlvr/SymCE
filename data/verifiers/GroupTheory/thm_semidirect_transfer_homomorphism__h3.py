import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)  # V4 is isomorphic to A4's Sylow 2-subgroup, but we bind A4 here as requested
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Witness is expected to be a tuple (G, N, H) where G, N, H are PermutationGroup objects.
    """
    try:
        G, N, H = witness
        if not isinstance(G, PermutationGroup):
            G = PermutationGroup(G)
        if not isinstance(N, PermutationGroup):
            N = PermutationGroup(N)
        if not isinstance(H, PermutationGroup):
            H = PermutationGroup(H)
    except Exception:
        return [False, False, False]

    # H_1: G = N \rtimes H is an internal semidirect product of finite groups
    try:
        h1 = True
        # Check if N and H are subgroups of G
        for g in N.generators:
            if g not in G:
                h1 = False
        for g in H.generators:
            if g not in G:
                h1 = False
        
        if h1:
            # Check if N is normal in G
            if not N.is_normal(G):
                h1 = False
            
            # Check if N intersect H is trivial and G = NH
            N_elems = set(N.generate())
            H_elems = set(H.generate())
            if len(N_elems.intersection(H_elems)) != 1:
                h1 = False
            if len(N_elems) * len(H_elems) != G.order():
                h1 = False
    except Exception:
        h1 = False

    # H_2: The complement subgroup H is abelian
    try:
        h2 = H.is_abelian
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails
    # Conclusion: V(h) = h^{|N|} for all h in H, and N is contained in ker(V)
    try:
        N_elems = list(N.generate())
        H_elems = list(H.generate())
        
        # Compute the transfer homomorphism V: G -> H
        # Since G = N \rtimes H, N is a left transversal of H in G.
        def V(g):
            res = G.identity
            for n in N_elems:
                x = g * n
                # Find h in H such that x * h^-1 in N
                found_h = None
                for h in H_elems:
                    if x * (~h) in N_elems:
                        found_h = h
                        break
                if found_h is None:
                    raise ValueError("h not found")
                res = res * found_h
            return res

        q_holds = True
        N_order = len(N_elems)
        
        # Check if V(h) == h^{|N|} for all h in H
        for h in H_elems:
            if V(h) != h**N_order:
                q_holds = False
                break
                
        # Check if N is contained in ker(V)
        if q_holds:
            for n in N_elems:
                if V(n) != G.identity:
                    q_holds = False
                    break
                    
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G = N \rtimes H is an internal semidirect product of finite groups",
    "H_2: The complement subgroup H is abelian",
    "¬Q: The restriction of V to H is not given by V(h) = h^{|N|} or N is not contained in ker(V)"
]

N_HYP = 2
NEG_Q_INDEX = 2