import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.matrices import eye, zeros
import math
from itertools import combinations, product

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def can_be_generated_by(G, k):
    if k < 0:
        return False
    try:
        order = G.order()
    except Exception:
        return False
        
    if order == 1:
        return True
    if k == 0:
        return False
        
    try:
        if len(G.generators) <= k:
            return True
    except Exception:
        pass
        
    try:
        elements = list(G.generate())
    except Exception:
        return False
        
    is_perm = False
    try:
        if elements and type(elements[0]).__name__ == 'Permutation':
            is_perm = True
    except Exception:
        pass

    if is_perm:
        for subset in combinations(elements, k):
            try:
                if PermutationGroup(*subset).order() == order:
                    return True
            except Exception:
                pass
        return False

    for subset in combinations(elements, k):
        try:
            id_elem = elements[0]**0
            generated = {id_elem}
            queue = [id_elem]
            
            while queue:
                curr = queue.pop(0)
                for gen in subset:
                    nxt = curr * gen
                    if nxt not in generated:
                        generated.add(nxt)
                        queue.append(nxt)
                        if len(generated) == order:
                            break
                if len(generated) == order:
                    break
            if len(generated) == order:
                return True
        except Exception:
            pass
            
    return False

def has_surjective_homomorphism(F, G):
    if type(F).__name__ == 'FreeGroup':
        return can_be_generated_by(G, len(F.generators))
        
    if type(F).__name__ == 'FpGroup':
        gens = F.generators
        rels = F.relators
        try:
            elements = list(G.generate())
            order = G.order()
            id_elem = elements[0]**0
        except Exception:
            return False
            
        if len(gens) == 0:
            return order == 1
            
        is_perm = False
        try:
            if elements and type(elements[0]).__name__ == 'Permutation':
                is_perm = True
        except Exception:
            pass

        for tup in product(elements, repeat=len(gens)):
            generates = False
            if is_perm:
                try:
                    if PermutationGroup(*tup).order() == order:
                        generates = True
                except Exception:
                    pass
            else:
                try:
                    generated = {id_elem}
                    queue = [id_elem]
                    while queue:
                        curr = queue.pop(0)
                        for gen_val in tup:
                            nxt = curr * gen_val
                            if nxt not in generated:
                                generated.add(nxt)
                                queue.append(nxt)
                                if len(generated) == order:
                                    break
                        if len(generated) == order:
                            break
                    if len(generated) == order:
                        generates = True
                except Exception:
                    pass
            
            if not generates:
                continue
                
            all_rels_satisfied = True
            for rel in rels:
                val = id_elem
                try:
                    for letter in rel.letter_form:
                        if letter in gens:
                            idx = gens.index(letter)
                            val = val * tup[idx]
                        else:
                            inv_letter = letter**-1
                            if inv_letter in gens:
                                idx = gens.index(inv_letter)
                                val = val * (tup[idx]**-1)
                except Exception:
                    all_rels_satisfied = False
                    break
                        
                if val != id_elem:
                    all_rels_satisfied = False
                    break
            if all_rels_satisfied:
                return True
        return False
        
    if isinstance(F, PermutationGroup):
        try:
            gens = F.generators
            elements = list(G.generate())
            order = G.order()
            id_elem = elements[0]**0
            
            is_perm = False
            if elements and type(elements[0]).__name__ == 'Permutation':
                is_perm = True
                
            for tup in product(elements, repeat=len(gens)):
                generates = False
                if is_perm:
                    if PermutationGroup(*tup).order() == order:
                        generates = True
                else:
                    generated = {id_elem}
                    queue = [id_elem]
                    while queue:
                        curr = queue.pop(0)
                        for gen_val in tup:
                            nxt = curr * gen_val
                            if nxt not in generated:
                                generated.add(nxt)
                                queue.append(nxt)
                                if len(generated) == order:
                                    break
                        if len(generated) == order:
                            break
                    if len(generated) == order:
                        generates = True
                        
                if not generates:
                    continue
                    
                hom = {F.identity: id_elem}
                queue = [F.identity]
                valid_hom = True
                while queue:
                    curr = queue.pop(0)
                    for i, g in enumerate(gens):
                        nxt = curr * g
                        nxt_val = hom[curr] * tup[i]
                        if nxt in hom:
                            if hom[nxt] != nxt_val:
                                valid_hom = False
                                break
                        else:
                            hom[nxt] = nxt_val
                            queue.append(nxt)
                    if not valid_hom:
                        break
                if valid_hom:
                    return True
            return False
        except Exception:
            return False

    return False

def conditions(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            F, G, n = witness
        elif len(witness) == 2:
            F, G = witness
            try:
                if type(F).__name__ == 'FreeGroup':
                    n = len(F.generators)
                elif type(F).__name__ == 'FpGroup':
                    n = len(F.generators)
                elif isinstance(F, PermutationGroup):
                    n = len(F.generators)
                else:
                    n = 0
            except Exception:
                n = 0
        else:
            return [False] * 4
    else:
        return [False] * 4

    # H1: F is a free group of rank n
    try:
        if type(F).__name__ == 'FreeGroup':
            h1 = len(F.generators) == n
        elif type(F).__name__ == 'FpGroup':
            h1 = len(F.relators) == 0 and len(F.generators) == n
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: G is a finite group
    try:
        order = G.order()
        h2 = order != sympy.oo and float(order) < math.inf
    except Exception:
        h2 = False

    # H3: G can be generated by a set of n or fewer elements
    try:
        n_int = int(n)
        if n_int != n:
            h3 = False
        else:
            h3 = can_be_generated_by(G, n_int)
    except Exception:
        h3 = False

    # neg_Q: There does not exist a surjective group homomorphism from F onto G
    try:
        neg_q = not has_surjective_homomorphism(F, G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group of rank n",
    "H_2: G is a finite group",
    "H_3: G can be generated by a set of n or fewer elements",
    "¬Q: There does not exist a surjective group homomorphism from F onto G"
]

N_HYP = 3
NEG_Q_INDEX = 3