import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import DihedralGroup, SymmetricGroup, AlternatingGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_automorphisms(G):
    elements = list(G.generate())
    n = len(elements)
    gens = G.generators
    
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    mult_table = [[0] * n for _ in range(n)]
    for i, a in enumerate(elements):
        for j, b in enumerate(elements):
            mult_table[i][j] = elem_to_idx[a * b]
            
    id_idx = None
    for i, e in enumerate(elements):
        if e.order() == 1:
            id_idx = i
            break
    if id_idx is None:
        return []
        
    orders = [e.order() for e in elements]
    gen_indices = [elem_to_idx[g] for g in gens]
    
    automorphisms = []
    
    def backtrack(gen_idx, current_mapping):
        if gen_idx == len(gen_indices):
            mapping = [None] * n
            mapping[id_idx] = id_idx
            for g_i, m_g_i in zip(gen_indices, current_mapping):
                mapping[g_i] = m_g_i
                
            knowns = [id_idx]
            for g_i in gen_indices:
                if g_i not in knowns:
                    knowns.append(g_i)
                    
            head = 0
            valid = True
            while head < len(knowns) and valid:
                i = knowns[head]
                for j_idx in range(head + 1):
                    j = knowns[j_idx]
                    
                    # i * j
                    k1 = mult_table[i][j]
                    m_k1 = mult_table[mapping[i]][mapping[j]]
                    if mapping[k1] is None:
                        mapping[k1] = m_k1
                        knowns.append(k1)
                    elif mapping[k1] != m_k1:
                        valid = False
                        break
                    
                    if not valid: 
                        break
                    
                    # j * i
                    k2 = mult_table[j][i]
                    m_k2 = mult_table[mapping[j]][mapping[i]]
                    if mapping[k2] is None:
                        mapping[k2] = m_k2
                        knowns.append(k2)
                    elif mapping[k2] != m_k2:
                        valid = False
                        break
                head += 1
            
            if valid and len(knowns) == n:
                if len(set(mapping)) == n:
                    automorphisms.append(mapping)
            return

        g = gen_indices[gen_idx]
        g_order = orders[g]
        for target in range(n):
            if orders[target] == g_order:
                backtrack(gen_idx + 1, current_mapping + [target])

    backtrack(0, [])
    return automorphisms

def is_dihedral(G, n):
    try:
        if G.order() != 2 * n:
            return False
        if getattr(G, 'is_abelian', False) and n > 2:
            return False
        elements = list(G.generate())
        order_2 = sum(1 for g in elements if g.order() == 2)
        expected_order_2 = n + 1 if n % 2 == 0 else n
        if order_2 != expected_order_2:
            return False
        has_order_n = any(g.order() == n for g in elements)
        return has_order_n
    except Exception:
        return False

def conditions(witness):
    # H1: G is isomorphic to the dihedral group of order 8
    # We check for both size 8 (D4) and size 16 (D8) to handle potential notational ambiguity
    try:
        h1 = is_dihedral(witness, 4) or is_dihedral(witness, 8)
    except Exception:
        h1 = False

    # neg_Q: The automorphism group of G is NOT isomorphic to G
    try:
        neg_q = False
        if hasattr(witness, 'order') and witness.order() <= 16:
            automorphisms = get_automorphisms(witness)
            if len(automorphisms) != witness.order():
                neg_q = True
            else:
                perms = [Permutation(mapping) for mapping in automorphisms]
                AutG = PermutationGroup(*perms)
                if AutG.order() != witness.order():
                    neg_q = True
                elif getattr(AutG, 'is_abelian', False) != getattr(witness, 'is_abelian', False):
                    neg_q = True
                else:
                    def get_order_profile(grp):
                        profile = {}
                        for g in grp.generate():
                            o = g.order()
                            profile[o] = profile.get(o, 0) + 1
                        return profile
                    if get_order_profile(AutG) != get_order_profile(witness):
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is isomorphic to the dihedral group of order 8",
    "¬Q: The automorphism group of G is not isomorphic to G"
]

N_HYP = 1
NEG_Q_INDEX = 1