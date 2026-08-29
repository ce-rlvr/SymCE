import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
trivial = CyclicGroup(1)

def get_automorphisms(G):
    elements = list(G.generate())
    if not elements:
        return []
    
    id_idx = -1
    for i, e in enumerate(elements):
        if e * e == e:
            id_idx = i
            break
            
    if id_idx == -1:
        return []
        
    # Swap identity to index 0
    elements[0], elements[id_idx] = elements[id_idx], elements[0]
    n = len(elements)
    
    if n > 20:
        raise ValueError("Group too large for naive automorphism search")
        
    mult = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mult[i][j] = elements.index(elements[i] * elements[j])
            
    ans = []
    def backtrack(step, p, used):
        if step == n:
            ans.append(tuple(p))
            return
        
        for j in range(n):
            if used[j]: continue
            
            valid = True
            # Check all multiplication relations that can now be evaluated
            for x in range(step + 1):
                for y in range(step + 1):
                    m = mult[x][y]
                    if max(x, y, m) == step:
                        px = j if x == step else p[x]
                        py = j if y == step else p[y]
                        pm = j if m == step else p[m]
                        if pm != mult[px][py]:
                            valid = False
                            break
                if not valid:
                    break
            
            if valid:
                p.append(j)
                used[j] = True
                backtrack(step + 1, p, used)
                used[j] = False
                p.pop()

    used = [False]*n
    used[0] = True
    backtrack(1, [0], used)
    return ans

def conditions(witness):
    try:
        # The witness can be just G, or a tuple (G, A)
        if isinstance(witness, tuple):
            G = witness[0]
        else:
            G = witness
            
        if not hasattr(G, 'generate'):
            h1_ok = False
        else:
            elements = list(G.generate())
            h1_ok = len(elements) > 0
    except Exception:
        h1_ok = False
        
    try:
        if not h1_ok:
            neg_q = False
        else:
            automorphisms = get_automorphisms(G)
            if not automorphisms:
                neg_q = False
            else:
                n = len(automorphisms[0])
                
                center = []
                for z in automorphisms:
                    is_center = True
                    for p in automorphisms:
                        zp = tuple(z[p[i]] for i in range(n))
                        pz = tuple(p[z[i]] for i in range(n))
                        if zp != pz:
                            is_center = False
                            break
                    if is_center:
                        center.append(z)
                        
                # The conclusion is that Z(A) is trivial (size 1)
                # Negation: Z(A) is NOT trivial (size > 1)
                neg_q = len(center) > 1
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: A is the automorphism group of G",
    "¬Q: The center Z(A) is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1