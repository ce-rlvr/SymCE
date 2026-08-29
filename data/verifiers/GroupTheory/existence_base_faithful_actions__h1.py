import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from itertools import combinations

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
# V4 is the Klein four-group
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        # Parse the witness into a PermutationGroup G and a domain X
        if isinstance(witness, tuple) and len(witness) == 2:
            G, X = witness
            if isinstance(G, list) and all(isinstance(p, Permutation) for p in G):
                G = PermutationGroup(G) if G else PermutationGroup(Permutation())
            if not isinstance(G, PermutationGroup):
                return [False, False]
            if not isinstance(X, (list, set, tuple)):
                return [False, False]
            X = list(X)
            
            # Check if G acts on X (i.e., X is G-invariant)
            acts_on_X = True
            for g in G.generators:
                for x in X:
                    if g(x) not in X:
                        acts_on_X = False
                        break
                if not acts_on_X:
                    break
            
            if not acts_on_X:
                return [False, False]
                
            # Check if the action is faithful on X
            stab = G
            for x in X:
                stab = stab.stabilizer(x)
                if stab.order() == 1:
                    break
            
            if stab.order() != 1:
                return [False, False]
                
            h1_ok = True
            
        elif isinstance(witness, PermutationGroup):
            G = witness
            X = list(range(G.degree))
            h1_ok = True
            
        elif isinstance(witness, list) and all(isinstance(p, Permutation) for p in witness):
            G = PermutationGroup(witness) if witness else PermutationGroup(Permutation())
            X = list(range(G.degree))
            h1_ok = True
            
        else:
            return [False, False]
            
        # Conclusion: There exists a subset S ⊆ X such that the pointwise stabilizer of S in G is the trivial subgroup.
        def is_trivial_stabilizer(S):
            stab = G
            for s in S:
                stab = stab.stabilizer(s)
                if stab.order() == 1:
                    return True
            return stab.order() == 1

        exists_S = False
        
        # Check S = X first (if the action is faithful, this is guaranteed to be trivial)
        if is_trivial_stabilizer(X):
            exists_S = True
        else:
            # Fallback to checking all subsets
            for r in range(len(X) + 1):
                for S in combinations(X, r):
                    if is_trivial_stabilizer(S):
                        exists_S = True
                        break
                if exists_S:
                    break
                    
        # The negated conclusion is True if NO such subset exists
        neg_q_ok = not exists_S
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G acts faithfully on a finite set X",
    "¬Q: No subset S ⊆ X has a trivial pointwise stabilizer in G"
]

N_HYP = 1
NEG_Q_INDEX = 1