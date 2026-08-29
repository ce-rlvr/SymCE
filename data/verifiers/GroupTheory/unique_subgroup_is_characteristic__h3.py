import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            k = witness.get('k')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, k, H = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: k is a positive integer
    try:
        h2 = (isinstance(k, int) or isinstance(k, sympy.Integer)) and k > 0
    except Exception:
        h2 = False

    # ¬Q: H is not a characteristic subgroup of G
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            neg_q = True
        else:
            try:
                is_sub = H.is_subgroup(G)
            except Exception:
                is_sub = False
                
            if not is_sub:
                neg_q = True
            else:
                elements = list(G.generate())
                gens = G.generators
                
                # Pre-filter elements by order to match generators for fast automorphism search
                candidates = [[e for e in elements if e.order() == g.order()] for g in gens]
                
                is_char = True
                for images in itertools.product(*candidates):
                    mapping = {G.identity: G.identity}
                    queue = [G.identity]
                    valid = True
                    
                    # BFS to build the homomorphism and check relations
                    while queue:
                        curr = queue.pop(0)
                        for i, g in enumerate(gens):
                            nxt = curr * g
                            nxt_img = mapping[curr] * images[i]
                            if nxt in mapping:
                                if mapping[nxt] != nxt_img:
                                    valid = False
                                    break
                            else:
                                mapping[nxt] = nxt_img
                                queue.append(nxt)
                        if not valid:
                            break
                            
                    # If valid and surjective, it's an automorphism
                    if valid and len(set(mapping.values())) == G.order():
                        for h in H.generators:
                            if mapping[h] not in H:
                                is_char = False
                                break
                    if not is_char:
                        break
                neg_q = not is_char
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: k is a positive integer",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2