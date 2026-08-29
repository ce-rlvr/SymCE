import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (G, H) where G is a PermutationGroup and H is a list/set of elements in G.
    """
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: G acts on the set of left cosets G/H via g \cdot (xH) = (gx)H
    # This requires that H is a subset of G. The action itself is always well-defined for any subset.
    try:
        elements = list(G.generate())
        h2 = all(h in elements for h in H)
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion fails
    try:
        elements = list(G.generate())
        H_set = set(H)
        
        # Find the identity element of G
        id_el = None
        for g in elements:
            if all(g * x == x for x in elements):
                id_el = g
                break
                
        if id_el is None:
            return [h1, h2, False]
            
        # Compute the set of left cosets C = {xH | x \in G}
        C = set()
        for x in elements:
            xH = frozenset(x * h for h in H_set)
            C.add(xH)
            
        # Compute the kernel of the action K
        K = set()
        for g in elements:
            acts_trivially = True
            for xH in C:
                gxH = frozenset(g * y for y in xH)
                if gxH != xH:
                    acts_trivially = False
                    break
            if acts_trivially:
                K.add(g)
                
        # Compute I = \bigcap_{g \in G} gHg^{-1}
        I = set(elements)
        for g in elements:
            gHg_inv = set(g * h * ~g for h in H_set)
            I = I.intersection(gHg_inv)
            
        conclusion_holds = True
        
        # Check if K == I
        if K != I:
            conclusion_holds = False
        else:
            # Check if K is a normal subgroup of G
            if id_el not in K:
                conclusion_holds = False
            else:
                for k1 in K:
                    for k2 in K:
                        if k1 * k2 not in K:
                            conclusion_holds = False
                for k in K:
                    if ~k not in K:
                        conclusion_holds = False
                for g in elements:
                    for k in K:
                        if g * k * ~g not in K:
                            conclusion_holds = False
                            
            # Check if K is contained in H
            if not K.issubset(H_set):
                conclusion_holds = False
                
            # Check if K is the largest normal subgroup of G contained in H
            if conclusion_holds:
                # Find all conjugacy classes of G
                conjugacy_classes = []
                unseen = set(elements)
                while unseen:
                    x = unseen.pop()
                    cclass = set()
                    for g in elements:
                        cclass.add(g * x * ~g)
                    conjugacy_classes.append(cclass)
                    unseen -= cclass
                    
                # A normal subgroup contained in H must be a union of conjugacy classes contained in H
                valid_cclasses = [c for c in conjugacy_classes if c.issubset(H_set)]
                
                for r in range(1, len(valid_cclasses) + 1):
                    for subset in itertools.combinations(valid_cclasses, r):
                        S = set().union(*subset)
                        if id_el not in S:
                            continue
                            
                        # Check if S is a subgroup
                        is_subgroup = True
                        for s1 in S:
                            for s2 in S:
                                if s1 * s2 not in S:
                                    is_subgroup = False
                                    break
                            if not is_subgroup:
                                break
                        if not is_subgroup:
                            continue
                            
                        for s in S:
                            if ~s not in S:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            continue
                            
                        # S is a normal subgroup contained in H. It must be a subset of K.
                        if not S.issubset(K):
                            conclusion_holds = False
                            break
                    if not conclusion_holds:
                        break
                        
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on the set of left cosets G/H via g \\cdot (xH) = (gx)H",
    "¬Q: The kernel of the action is not \\bigcap_{g \\in G} gHg^{-1} or it is not the largest normal subgroup of G contained in H"
]

N_HYP = 2
NEG_Q_INDEX = 2