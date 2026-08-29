import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import itertools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup) and witness.order() >= 1
    except Exception:
        h1 = False

    # H2: G is a semisimple group
    # A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    # Equivalently, no non-trivial conjugacy class generates an abelian subgroup.
    try:
        if not h1:
            h2 = False
        else:
            h2 = True
            if witness.order() > 1:
                elements = list(witness.generate())
                identity = elements[0]**0
                gens = witness.generators
                
                unvisited = set(elements)
                unvisited.remove(identity)
                
                while unvisited:
                    x = unvisited.pop()
                    conj_class = set([x])
                    queue = [x]
                    while queue:
                        curr = queue.pop(0)
                        for g in gens:
                            nxt = g * curr * g**-1
                            if nxt not in conj_class:
                                conj_class.add(nxt)
                                queue.append(nxt)
                            nxt_inv = g**-1 * curr * g
                            if nxt_inv not in conj_class:
                                conj_class.add(nxt_inv)
                                queue.append(nxt_inv)
                                
                    unvisited.difference_update(conj_class)
                    
                    conj_list = list(conj_class)
                    is_abelian = True
                    for i in range(len(conj_list)):
                        for j in range(i + 1, len(conj_list)):
                            if conj_list[i] * conj_list[j] != conj_list[j] * conj_list[i]:
                                is_abelian = False
                                break
                        if not is_abelian:
                            break
                            
                    if is_abelian:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # neg_Q: Inn(G) is NOT a subgroup of Aut(G)'
    try:
        if not h1:
            neg_q = False
        else:
            elements = list(witness.generate())
            identity = elements[0]**0
            gens = witness.generators
            
            # Precompute full multiplication table for fast evaluation
            full_mult = {}
            for g1 in elements:
                full_mult[g1] = {}
                for g2 in elements:
                    full_mult[g1][g2] = g1 * g2
                    
            mult_table = {}
            for g in elements:
                mult_table[g] = []
                for gen in gens:
                    mult_table[g].append(full_mult[g][gen])
                    
            # Build a BFS tree to quickly generate mappings for automorphism candidates
            bfs_tree = []
            visited = {identity}
            queue = [identity]
            while queue:
                curr = queue.pop(0)
                for i, gen in enumerate(gens):
                    nxt = full_mult[curr][gen]
                    if nxt not in visited:
                        visited.add(nxt)
                        bfs_tree.append((curr, i, nxt))
                        queue.append(nxt)
                        
            cand_choices = []
            for gen in gens:
                order = gen.order()
                choices = [g for g in elements if g.order() == order]
                cand_choices.append(choices)
                
            elements_idx = {g: i for i, g in enumerate(elements)}
            aut_perms = []
            
            for cand in itertools.product(*cand_choices):
                mapping = {identity: identity}
                for parent, gen_idx, child in bfs_tree:
                    mapping[child] = full_mult[mapping[parent]][cand[gen_idx]]
                    
                seen = set()
                is_bij = True
                for v in mapping.values():
                    if v in seen:
                        is_bij = False
                        break
                    seen.add(v)
                if not is_bij:
                    continue
                    
                is_homo = True
                for g in elements:
                    for i, gen in enumerate(gens):
                        if mapping[mult_table[g][i]] != full_mult[mapping[g]][cand[i]]:
                            is_homo = False
                            break
                    if not is_homo:
                        break
                        
                if is_homo:
                    perm = [elements_idx[mapping[g]] for g in elements]
                    aut_perms.append(Permutation(perm))
                    
            AutG = PermutationGroup(aut_perms)
            
            inn_perms = []
            for g in elements:
                g_inv = g**-1
                perm = []
                for x in elements:
                    conj = full_mult[full_mult[g][x]][g_inv]
                    perm.append(elements_idx[conj])
                inn_perms.append(Permutation(perm))
                
            InnG = PermutationGroup(inn_perms)
            H_der = AutG.derived_subgroup()
            
            is_subgroup = True
            for gen in InnG.generators:
                if not H_der.contains(gen):
                    is_subgroup = False
                    break
                    
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "¬Q: Inn(G) is not a subgroup of the derived subgroup of Aut(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2