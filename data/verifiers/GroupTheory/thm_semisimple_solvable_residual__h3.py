import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings for witness expressions
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

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, S = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and getattr(G, 'is_group', True)
    except Exception:
        h1 = False
        
    # H2: S is a normal semisimple subgroup of G
    try:
        h2 = False
        if isinstance(S, PermutationGroup) and getattr(S, 'is_group', True):
            # Check if S is a subgroup of G
            is_subgroup = all(G.contains(g) for g in S.generators)
            if is_subgroup:
                # Check if S is normal in G
                is_normal = True
                for s in S.generators:
                    for g in G.generators:
                        conj = g * s * ~g
                        if not S.contains(conj):
                            is_normal = False
                            break
                    if not is_normal:
                        break
                
                if is_normal:
                    # Check if S is semisimple
                    # A finite group is semisimple iff it is a direct product of non-abelian simple groups.
                    # This is equivalent to being perfect and having no non-trivial abelian normal subgroups.
                    if S.order() == 1:
                        h2 = True
                    else:
                        is_perfect = (S.derived_subgroup().order() == S.order())
                        if is_perfect:
                            if S.generators:
                                id_elem = S.generators[0] * ~S.generators[0]
                            else:
                                id_elem = Permutation()
                                
                            has_abelian_normal = False
                            count = 0
                            for x in S.elements:
                                if x == id_elem:
                                    continue
                                count += 1
                                if count > 2000:  # Safety limit to prevent timeouts
                                    break
                                    
                                # Generate the normal closure of x in S
                                closure_gens = {x}
                                queue = [x]
                                while queue:
                                    curr = queue.pop(0)
                                    for g in S.generators:
                                        conj = g * curr * ~g
                                        if conj not in closure_gens:
                                            closure_gens.add(conj)
                                            queue.append(conj)
                                            
                                # Check if the normal closure is abelian
                                closure_list = list(closure_gens)
                                is_abelian = True
                                for i in range(len(closure_list)):
                                    for j in range(i + 1, len(closure_list)):
                                        if closure_list[i] * closure_list[j] != closure_list[j] * closure_list[i]:
                                            is_abelian = False
                                            break
                                    if not is_abelian:
                                        break
                                        
                                if is_abelian:
                                    has_abelian_normal = True
                                    break
                                    
                            if not has_abelian_normal:
                                h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: S is NOT the solvable residual of G
    try:
        neg_q = False
        if h1 and isinstance(S, PermutationGroup):
            # Compute the solvable residual of G (limit of the derived series)
            R = G
            while True:
                D = R.derived_subgroup()
                if D.order() == R.order():
                    break
                R = D
            
            # Check if S is equal to the solvable residual R
            is_equal = (S.order() == R.order()) and all(R.contains(g) for g in S.generators)
            neg_q = not is_equal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: S is a normal semisimple subgroup of G",
    "¬Q: S is not the solvable residual of G"
]

N_HYP = 2
NEG_Q_INDEX = 2