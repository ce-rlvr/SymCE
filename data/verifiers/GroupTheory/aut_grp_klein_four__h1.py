import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # DihedralGroup(2) is isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_aut_isomorphic_to_S3(G):
    """
    Computes the automorphism group of G and checks if it is isomorphic to S_3.
    For performance, we limit the check to groups of order <= 30.
    (Mathematically, the only groups with Aut(G) isomorphic to S_3 are V_4 and S_3).
    """
    elements = []
    for i, e in enumerate(G.generate()):
        if i > 30:
            return False
        elements.append(e)
        
    n = len(elements)
    if n == 0:
        return False
        
    id_elem = G.identity
    if id_elem in elements:
        elements.remove(id_elem)
    elements.insert(0, id_elem)
    
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    mult_table = [[0] * n for _ in range(n)]
    for i, a in enumerate(elements):
        for j, b in enumerate(elements):
            mult_table[i][j] = elem_to_idx[a * b]
            
    # Find a small set of generators
    gens_idx = []
    generated = {0}
    for i in range(1, n):
        if i not in generated:
            gens_idx.append(i)
            new_gen = list(generated)
            new_gen.append(i)
            closure = set(new_gen)
            added = True
            while added:
                added = False
                to_add = []
                for x in closure:
                    for y in closure:
                        z = mult_table[x][y]
                        if z not in closure:
                            to_add.append(z)
                if to_add:
                    closure.update(to_add)
                    added = True
            generated = closure
            if len(generated) == n:
                break
                
    # Find all automorphisms by mapping generators
    automorphisms = []
    for target_tuple in itertools.product(range(n), repeat=len(gens_idx)):
        mapping = {0: 0}
        for g_idx, t_idx in zip(gens_idx, target_tuple):
            mapping[g_idx] = t_idx
            
        known = [0] + gens_idx
        is_hom = True
        head = 0
        while head < len(known):
            x = known[head]
            for i in range(head + 1):
                y = known[i]
                
                # Check x * y
                z1 = mult_table[x][y]
                mz1 = mult_table[mapping[x]][mapping[y]]
                if z1 in mapping:
                    if mapping[z1] != mz1:
                        is_hom = False
                        break
                else:
                    mapping[z1] = mz1
                    known.append(z1)
                    
                # Check y * x
                z2 = mult_table[y][x]
                mz2 = mult_table[mapping[y]][mapping[x]]
                if z2 in mapping:
                    if mapping[z2] != mz2:
                        is_hom = False
                        break
                else:
                    mapping[z2] = mz2
                    known.append(z2)
            if not is_hom:
                break
            head += 1
            
        if is_hom and len(mapping) == n:
            if len(set(mapping.values())) == n:
                map_list = [mapping[i] for i in range(n)]
                automorphisms.append(map_list)
                
    # S_3 has exactly 6 automorphisms
    if len(automorphisms) != 6:
        return False
        
    # Check if the automorphism group is non-abelian (since the only non-abelian group of order 6 is S_3)
    for f in automorphisms:
        for g in automorphisms:
            fg = [f[g[i]] for i in range(n)]
            gf = [g[f[i]] for i in range(n)]
            if fg != gf:
                return True
                
    return False

def conditions(witness) -> list[bool]:
    try:
        # A valid witness must be a group-like object
        if not hasattr(witness, 'generate') or not hasattr(witness, 'identity'):
            return [False]
            
        # Q: Aut(V) is isomorphic to S_3
        q = is_aut_isomorphic_to_S3(witness)
        
        # We want the conclusion to FAIL at the witness
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = ["¬Q: Aut(V) is not isomorphic to S_3"]
N_HYP = 0
NEG_Q_INDEX = 0
