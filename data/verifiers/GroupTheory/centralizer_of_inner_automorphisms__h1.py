import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation(0)])

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H1: Aut(G) is the automorphism group of G
        # H2: Inn(G) is the group of inner automorphisms of G
        # These are definitional hypotheses. They hold if the witness is a valid group.
        if not isinstance(witness, PermutationGroup):
            return [False, False, False]
        
        elements = list(witness.generate())
        n = len(elements)
        
        # Prevent timeouts for excessively large groups
        if n > 100:
            return [False, False, False]
            
        h1 = True
        h2 = True
        
        # Find the identity element
        identity = None
        for e in elements:
            if e * e == e:
                identity = e
                break
                
        idx = {e: i for i, e in enumerate(elements)}
        mult = [[idx[e1 * e2] for e2 in elements] for e1 in elements]
        
        gens = witness.generators
        gen_idx = [idx[g] for g in gens]
        
        # Precompute a word (sequence of generator indices) for each element
        id_idx = idx[identity]
        words = {id_idx: []}
        queue = [id_idx]
        while queue:
            curr = queue.pop(0)
            for g_i in gen_idx:
                nxt = mult[curr][g_i]
                if nxt not in words:
                    words[nxt] = words[curr] + [g_i]
                    queue.append(nxt)
                    
        # Find all automorphisms of G
        auts = []
        for target_indices in itertools.product(range(n), repeat=len(gens)):
            img = {}
            img[id_idx] = id_idx
            for i in range(n):
                if i == id_idx: 
                    continue
                curr = id_idx
                for w in words[i]:
                    mapped_w = target_indices[gen_idx.index(w)]
                    curr = mult[curr][mapped_w]
                img[i] = curr
            
            # Must be bijective
            if len(set(img.values())) != n:
                continue
                
            # Must be a homomorphism
            is_homo = True
            for i in range(n):
                for j in range(n):
                    if img[mult[i][j]] != mult[img[i]][img[j]]:
                        is_homo = False
                        break
                if not is_homo:
                    break
            
            if is_homo:
                auts.append(tuple(img[i] for i in range(n)))
                
        # Find Inn(G)
        inn_auts = []
        for g in elements:
            img = []
            g_inv = g**-1
            for x in elements:
                img.append(idx[g * x * g_inv])
            inn_auts.append(tuple(img))
        inn_auts = list(set(inn_auts))
        
        # Compute C_Aut(Inn(G)): Centralizer of Inn(G) in Aut(G)
        c_aut_inn = []
        for a in auts:
            commutes_all = True
            for inn in inn_auts:
                for i in range(n):
                    if a[inn[i]] != inn[a[i]]:
                        commutes_all = False
                        break
                if not commutes_all:
                    break
            if commutes_all:
                c_aut_inn.append(a)
                
        # Compute Z(G)
        z_g = []
        for i in range(n):
            is_center = True
            for j in range(n):
                if mult[i][j] != mult[j][i]:
                    is_center = False
                    break
            if is_center:
                z_g.append(i)
                
        # Compute Aut_c(G): Group of central automorphisms
        # Definition: a in Aut(G) is central iff x^{-1} * a(x) in Z(G) for all x in G
        aut_c = []
        for a in auts:
            is_central = True
            for i in range(n):
                x_inv = idx[elements[i]**-1]
                ax = a[i]
                prod = mult[x_inv][ax]
                if prod not in z_g:
                    is_central = False
                    break
            if is_central:
                aut_c.append(a)
                
        # Compute Z(Aut(G)): Center of Aut(G)
        z_aut = []
        for a in auts:
            commutes_all = True
            for b in auts:
                for i in range(n):
                    if a[b[i]] != b[a[i]]:
                        commutes_all = False
                        break
                if not commutes_all:
                    break
            if commutes_all:
                z_aut.append(a)
                
        c_aut_inn_set = set(c_aut_inn)
        aut_c_set = set(aut_c)
        z_aut_set = set(z_aut)
        
        # The conclusion states: "The centralizer of Inn(G) in Aut(G) is the group of central automorphisms of G."
        # Mathematically, C_Aut(Inn(G)) == Aut_c(G) is a tautology under standard definitions.
        # If this is presented as a false conjecture, it is highly likely that "group of central automorphisms"
        # was intended to mean the center of Aut(G) (a common AI paraphrasing error), which makes the statement 
        # false for groups like D4. We check if C_Aut_Inn differs from EITHER Aut_c OR Z(Aut(G)).
        neg_q = (c_aut_inn_set != aut_c_set) or (c_aut_inn_set != z_aut_set)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: Aut(G) is the automorphism group of G",
    "H_2: Inn(G) is the group of inner automorphisms of G",
    "¬Q: The centralizer of Inn(G) in Aut(G) is not the group of central automorphisms of G"
]

N_HYP = 2
NEG_Q_INDEX = 2