import sympy
from sympy import Symbol, groebner

# Top-level setup
# The witness is expected to provide its own ring objects and diagram structure.
# A ring object should have: elements (list), add(a, b), mul(a, b), zero, one.
# The witness should have: nodes, edges, rings, maps, limit_ring, limit_maps.

def is_commutative_ring(ring):
    elements = ring.elements
    zero = ring.zero
    one = ring.one
    for a in elements:
        if ring.add(a, zero) != a: return False
        if ring.add(zero, a) != a: return False
        if ring.mul(a, one) != a: return False
        if ring.mul(one, a) != a: return False
        
        has_inv = False
        for b in elements:
            if ring.add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
        for b in elements:
            if ring.add(a, b) != ring.add(b, a): return False
            if ring.mul(a, b) != ring.mul(b, a): return False
            for c in elements:
                if ring.add(ring.add(a, b), c) != ring.add(a, ring.add(b, c)): return False
                if ring.mul(ring.mul(a, b), c) != ring.mul(a, ring.mul(b, c)): return False
                if ring.mul(a, ring.add(b, c)) != ring.add(ring.mul(a, b), ring.mul(a, c)): return False
    return True

def is_integral_domain(ring):
    if ring.zero == ring.one:
        return False
    if not is_commutative_ring(ring):
        return False
    for a in ring.elements:
        if a != ring.zero:
            for b in ring.elements:
                if b != ring.zero:
                    if ring.mul(a, b) == ring.zero:
                        return False
    return True

def is_poset(nodes, edges):
    edge_set = set(edges)
    for i in nodes:
        if (i, i) not in edge_set:
            return False
    for (i, j) in edges:
        if i != j and (j, i) in edge_set:
            return False
    for (i, j) in edges:
        for (k, l) in edges:
            if j == k:
                if (i, l) not in edge_set:
                    return False
    return True

def check_diagram(witness):
    nodes = witness.nodes
    edges = witness.edges
    maps = witness.maps
    rings = witness.rings
    
    if not is_poset(nodes, edges):
        return False
        
    for i in nodes:
        f_ii = maps.get((i, i))
        if f_ii is None: return False
        for a in rings[i].elements:
            if f_ii(a) != a: return False
            
    for (i, j) in edges:
        for (k, l) in edges:
            if j == k:
                if (i, l) not in edges: return False
                f_ij = maps[(i, j)]
                f_jl = maps[(j, l)]
                f_il = maps[(i, l)]
                for a in rings[i].elements:
                    if f_jl(f_ij(a)) != f_il(a): return False
    return True

def check_colimit(witness):
    nodes = witness.nodes
    if not nodes:
        return False
        
    rings = witness.rings
    maps = witness.maps
    limit_ring = witness.limit_ring
    limit_maps = witness.limit_maps
    
    if not is_commutative_ring(limit_ring):
        return False
        
    for i in nodes:
        R = rings[i]
        f = limit_maps[i]
        if f(R.one) != limit_ring.one: return False
        for a in R.elements:
            for b in R.elements:
                if f(R.add(a, b)) != limit_ring.add(f(a), f(b)): return False
                if f(R.mul(a, b)) != limit_ring.mul(f(a), f(b)): return False
                
    for (i, j) in witness.edges:
        f_ij = maps[(i, j)]
        f_i = limit_maps[i]
        f_j = limit_maps[j]
        for a in rings[i].elements:
            if f_j(f_ij(a)) != f_i(a):
                return False
                
    images = set()
    for i in nodes:
        for a in rings[i].elements:
            images.add(limit_maps[i](a))
            
    generated = set(images)
    added = True
    while added:
        added = False
        new_elements = set()
        for a in generated:
            for b in generated:
                s = limit_ring.add(a, b)
                p = limit_ring.mul(a, b)
                if s not in generated:
                    new_elements.add(s)
                if p not in generated:
                    new_elements.add(p)
        if new_elements:
            generated.update(new_elements)
            added = True
            
    if len(generated) != len(limit_ring.elements):
        return False
        
    char = None
    for p in [2, 3, 5, 7, 11, 13, 17, 19]:
        all_match = True
        for i in nodes:
            R = rings[i]
            val = R.zero
            for _ in range(p):
                val = R.add(val, R.one)
            if val != R.zero:
                all_match = False
                break
        if all_match:
            char = p
            break
            
    if char is None:
        return False
        
    vars_sym = []
    var_map = {}
    for idx_i, i in enumerate(nodes):
        for idx_a, a in enumerate(rings[i].elements):
            sym = Symbol(f"x_{idx_i}_{idx_a}")
            vars_sym.append(sym)
            var_map[(i, a)] = sym
            
    relations = []
    for i in nodes:
        R = rings[i]
        for a in R.elements:
            xa = var_map[(i, a)]
            for b in R.elements:
                xb = var_map[(i, b)]
                x_ab_add = var_map[(i, R.add(a, b))]
                x_ab_mul = var_map[(i, R.mul(a, b))]
                relations.append(xa + xb - x_ab_add)
                relations.append(xa * xb - x_ab_mul)
        relations.append(var_map[(i, R.zero)])
        relations.append(var_map[(i, R.one)] - 1)
        
    for (i, j) in witness.edges:
        f_ij = maps[(i, j)]
        for a in rings[i].elements:
            xa = var_map[(i, a)]
            x_fa = var_map[(j, f_ij(a))]
            relations.append(xa - x_fa)
            
    G = groebner(relations, *vars_sym, domain=f'GF({char})', order='grevlex')
    LMs = [poly.LM() for poly in G.polys]
    
    num_vars = len(vars_sym)
    
    def count_standard_monomials(var_idx, current_exponents):
        if var_idx == num_vars:
            return 1
        count = 0
        for exp in [0, 1]:
            new_exponents = current_exponents + (exp,)
            padded = new_exponents + (0,) * (num_vars - len(new_exponents))
            divisible = False
            for lm in LMs:
                if all(p >= l for p, l in zip(padded, lm)):
                    divisible = True
                    break
            if not divisible:
                count += count_standard_monomials(var_idx + 1, new_exponents)
        return count

    dim = count_standard_monomials(0, ())
    true_size = char ** dim
    
    if len(limit_ring.elements) != true_size:
        return False
        
    return True

def conditions(witness):
    try:
        h1 = True
        for i in witness.nodes:
            if not is_integral_domain(witness.rings[i]):
                h1 = False
                break
    except Exception:
        h1 = False

    try:
        h2 = True
        if not check_diagram(witness):
            h2 = False
        else:
            for (i, j) in witness.edges:
                f_ij = witness.maps[(i, j)]
                R_i = witness.rings[i]
                R_j = witness.rings[j]
                if f_ij(R_i.one) != R_j.one:
                    h2 = False
                    break
                for a in R_i.elements:
                    for b in R_i.elements:
                        if f_ij(R_i.add(a, b)) != R_j.add(f_ij(a), f_ij(b)):
                            h2 = False
                            break
                        if f_ij(R_i.mul(a, b)) != R_j.mul(f_ij(a), f_ij(b)):
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
                
                seen = set()
                for a in R_i.elements:
                    fa = f_ij(a)
                    if fa in seen:
                        h2 = False
                        break
                    seen.add(fa)
                if not h2: break
    except Exception:
        h2 = False

    try:
        is_colimit = check_colimit(witness)
        if not is_colimit:
            neg_q = False
        else:
            neg_q = not is_integral_domain(witness.limit_ring)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: For every i in I, R_i is an integral domain",
    "H_2: For every i <= j in I, the transition homomorphism f_{ij} is injective",
    "¬Q: The direct limit is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2