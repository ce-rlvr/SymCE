import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_group_info(G):
    if isinstance(G, tuple) and len(G) == 3:
        return list(G[0]), G[1], G[2]
    
    if hasattr(G, 'generate') and callable(G.generate):
        elements = list(G.generate())
    elif hasattr(G, 'elements'):
        elements = list(G.elements)
    else:
        elements = list(G)
        
    op = lambda x, y: x * y
        
    if hasattr(G, 'identity'):
        identity = G.identity
    else:
        identity = None
        for e in elements:
            try:
                if all(op(e, x) == x for x in elements):
                    identity = e
                    break
            except Exception:
                pass
                
    return elements, op, identity

def get_subgroups(elements, op, identity):
    subgroups = set()
    subgroups.add(frozenset([identity]))
    
    current_subgroups = {frozenset([identity])}
    all_subgroups = set(current_subgroups)
    
    while True:
        new_subgroups = set()
        for sg in current_subgroups:
            for x in elements:
                if x not in sg:
                    closure = set(sg)
                    queue = [x]
                    closure.add(x)
                    while queue:
                        if len(closure) > 1000:
                            raise ValueError("Subgroup too large")
                        curr = queue.pop(0)
                        for y in list(closure):
                            xy = op(curr, y)
                            if xy not in closure:
                                closure.add(xy)
                                queue.append(xy)
                            yx = op(y, curr)
                            if yx not in closure:
                                closure.add(yx)
                                queue.append(yx)
                    new_sg = frozenset(closure)
                    if new_sg not in all_subgroups:
                        new_subgroups.add(new_sg)
        if not new_subgroups:
            break
        all_subgroups.update(new_subgroups)
        if len(all_subgroups) > 2000:
            raise ValueError("Too many subgroups")
        current_subgroups = new_subgroups
        
    return list(all_subgroups)

def are_posets_isomorphic(P1, P2):
    if len(P1) != len(P2):
        return False
    n = len(P1)
    if n == 0:
        return True
        
    def get_comp_matrix(P):
        mat = [[False]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if P[i].issubset(P[j]):
                    mat[i][j] = True
        return mat

    mat1 = get_comp_matrix(P1)
    mat2 = get_comp_matrix(P2)
    
    def get_invariants(mat):
        inv = []
        for i in range(n):
            indeg = sum(mat[j][i] for j in range(n))
            outdeg = sum(mat[i][j] for j in range(n))
            inv.append((indeg, outdeg))
        return inv

    inv1 = get_invariants(mat1)
    inv2 = get_invariants(mat2)
    
    from collections import defaultdict
    groups1 = defaultdict(list)
    for i, inv in enumerate(inv1):
        groups1[inv].append(i)
        
    groups2 = defaultdict(list)
    for i, inv in enumerate(inv2):
        groups2[inv].append(i)
        
    if set(groups1.keys()) != set(groups2.keys()):
        return False
        
    for k in groups1:
        if len(groups1[k]) != len(groups2[k]):
            return False
            
    keys = list(groups1.keys())
    
    def search(group_idx, mapping):
        if group_idx == len(keys):
            return True
            
        k = keys[group_idx]
        g1 = groups1[k]
        g2 = groups2[k]
        
        for p in itertools.permutations(g2):
            new_mapping = mapping.copy()
            for i, val in zip(g1, p):
                new_mapping[i] = val
            
            mapped_so_far = []
            for i in range(group_idx + 1):
                mapped_so_far.extend(groups1[keys[i]])
                
            valid = True
            for i in mapped_so_far:
                for j in mapped_so_far:
                    if mat1[i][j] != mat2[new_mapping[i]][new_mapping[j]]:
                        valid = False
                        break
                if not valid:
                    break
            
            if valid:
                if search(group_idx + 1, new_mapping):
                    return True
        return False

    return search(0, {})

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False]
        G, H, f = witness
        
        G_elements, G_op, G_id = get_group_info(G)
        H_elements, H_op, H_id = get_group_info(H)
        
        if isinstance(f, dict):
            def f_map(x): return f.get(x, None)
        elif isinstance(f, list):
            def f_map(x): return f[x] if isinstance(x, int) and 0 <= x < len(f) else None
        else:
            f_map = f
            
        is_hom = True
        for x in G_elements:
            for y in G_elements:
                fx = f_map(x)
                fy = f_map(y)
                fxy = f_map(G_op(x, y))
                if fx is None or fy is None or fxy is None:
                    is_hom = False
                    break
                if fxy != H_op(fx, fy):
                    is_hom = False
                    break
            if not is_hom:
                break
                
        im_f = set()
        for x in G_elements:
            fx = f_map(x)
            if fx is not None:
                im_f.add(fx)
                
        is_surj = (im_f == set(H_elements))
        
        h1_ok = is_hom and is_surj
    except Exception:
        h1_ok = False

    try:
        if len(witness) != 3:
            return [h1_ok, False]
        G, H, f = witness
        
        G_elements, G_op, G_id = get_group_info(G)
        H_elements, H_op, H_id = get_group_info(H)
        
        if isinstance(f, dict):
            def f_map(x): return f.get(x, None)
        elif isinstance(f, list):
            def f_map(x): return f[x] if isinstance(x, int) and 0 <= x < len(f) else None
        else:
            f_map = f
            
        ker_f = set()
        for x in G_elements:
            if f_map(x) == H_id:
                ker_f.add(x)
                
        subgroups_G = get_subgroups(G_elements, G_op, G_id)
        subgroups_G_ker = [sg for sg in subgroups_G if ker_f.issubset(sg)]
        
        subgroups_H = get_subgroups(H_elements, H_op, H_id)
        
        posets_iso = are_posets_isomorphic(subgroups_G_ker, subgroups_H)
        
        neg_q_ok = not posets_iso
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a surjective group homomorphism from G to H",
    "¬Q: There is no inclusion-preserving bijection between the set of subgroups of G containing the kernel of f and the set of subgroups of H"
]

N_HYP = 1
NEG_Q_INDEX = 1