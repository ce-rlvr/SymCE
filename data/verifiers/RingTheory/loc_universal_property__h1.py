import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        R = witness['R']
        S = witness['S']
        T = witness['T']
        S_inv_R = witness['S_inv_R']
        
        add_R = witness['add_R']
        mul_R = witness['mul_R']
        add_T = witness['add_T']
        mul_T = witness['mul_T']
        add_S_inv_R = witness['add_S_inv_R']
        mul_S_inv_R = witness['mul_S_inv_R']
        
        zero_R = witness['zero_R']
        one_R = witness['one_R']
        zero_T = witness['zero_T']
        one_T = witness['one_T']
        zero_S_inv_R = witness['zero_S_inv_R']
        one_S_inv_R = witness['one_S_inv_R']
        
        f = witness['f']
        phi = witness['phi']
    except Exception:
        return [False] * 5

    def is_unit(x, ring, mul_op, one_elem):
        for u in ring:
            if mul_op(x, u) == one_elem and mul_op(u, x) == one_elem:
                return True
        return False

    def get_inverse(x, ring, mul_op, one_elem):
        for u in ring:
            if mul_op(x, u) == one_elem and mul_op(u, x) == one_elem:
                return u
        return None

    def is_ring_hom(m, A, B, add_A, mul_A, add_B, mul_B, one_A, one_B):
        try:
            if m(one_A) != one_B: return False
            for x in A:
                if m(x) not in B: return False
                for y in A:
                    if m(add_A(x, y)) != add_B(m(x), m(y)): return False
                    if m(mul_A(x, y)) != mul_B(m(x), m(y)): return False
            return True
        except Exception:
            return False

    # H1: S is a multiplicatively closed subset of R
    try:
        h1 = True
        if not all(s in R for s in S): h1 = False
        if one_R not in S: h1 = False
        for s1 in S:
            for s2 in S:
                if mul_R(s1, s2) not in S: h1 = False
    except Exception:
        h1 = False

    # H2: f: R \to T is a ring homomorphism
    try:
        h2 = is_ring_hom(f, R, T, add_R, mul_R, add_T, mul_T, one_R, one_T)
    except Exception:
        h2 = False

    # H3: f(s) is a unit in T for all s \in S
    try:
        h3 = True
        for s in S:
            if not is_unit(f(s), T, mul_T, one_T):
                h3 = False
                break
    except Exception:
        h3 = False

    # H4: \phi: R \to S^{-1}R is the canonical localization map
    try:
        h4 = True
        if not is_ring_hom(phi, R, S_inv_R, add_R, mul_R, add_S_inv_R, mul_S_inv_R, one_R, one_S_inv_R):
            h4 = False
        else:
            for s in S:
                if not is_unit(phi(s), S_inv_R, mul_S_inv_R, one_S_inv_R):
                    h4 = False
                    break
            
            if h4:
                gens = set()
                for r in R:
                    gens.add(phi(r))
                for s in S:
                    inv_s = get_inverse(phi(s), S_inv_R, mul_S_inv_R, one_S_inv_R)
                    if inv_s is not None:
                        gens.add(inv_s)
                
                closure = set(gens)
                added = True
                while added:
                    added = False
                    new_elements = set()
                    for x in closure:
                        for y in closure:
                            s_add = add_S_inv_R(x, y)
                            s_mul = mul_S_inv_R(x, y)
                            if s_add not in closure and s_add not in new_elements:
                                new_elements.add(s_add)
                            if s_mul not in closure and s_mul not in new_elements:
                                new_elements.add(s_mul)
                    if new_elements:
                        closure.update(new_elements)
                        added = True
                
                if not all(x in closure for x in S_inv_R):
                    h4 = False
    except Exception:
        h4 = False

    # ¬Q: There does not exist a unique ring homomorphism g: S^{-1}R \to T such that f = g \circ \phi
    try:
        g_map = {}
        well_defined = True
        
        for r in R:
            pr = phi(r)
            fr = f(r)
            if pr in g_map and g_map[pr] != fr:
                well_defined = False
            g_map[pr] = fr
            
        for s in S:
            inv_s = get_inverse(phi(s), S_inv_R, mul_S_inv_R, one_S_inv_R)
            inv_fs = get_inverse(f(s), T, mul_T, one_T)
            if inv_s is not None and inv_fs is not None:
                if inv_s in g_map and g_map[inv_s] != inv_fs:
                    well_defined = False
                g_map[inv_s] = inv_fs
                
        added = True
        while added and well_defined:
            added = False
            new_g_map = {}
            keys = list(g_map.keys())
            for x in keys:
                for y in keys:
                    s_add = add_S_inv_R(x, y)
                    t_add = add_T(g_map[x], g_map[y])
                    if s_add in g_map:
                        if g_map[s_add] != t_add:
                            well_defined = False
                            break
                    elif s_add in new_g_map:
                        if new_g_map[s_add] != t_add:
                            well_defined = False
                            break
                    else:
                        new_g_map[s_add] = t_add
                        added = True
                        
                    s_mul = mul_S_inv_R(x, y)
                    t_mul = mul_T(g_map[x], g_map[y])
                    if s_mul in g_map:
                        if g_map[s_mul] != t_mul:
                            well_defined = False
                            break
                    elif s_mul in new_g_map:
                        if new_g_map[s_mul] != t_mul:
                            well_defined = False
                            break
                    else:
                        new_g_map[s_mul] = t_mul
                        added = True
                if not well_defined:
                    break
            if not well_defined:
                break
            g_map.update(new_g_map)
            
        if not well_defined:
            valid_g_count = 0
        else:
            if all(x in g_map for x in S_inv_R):
                if is_ring_hom(lambda x: g_map[x], S_inv_R, T, add_S_inv_R, mul_S_inv_R, add_T, mul_T, one_S_inv_R, one_T):
                    valid_g_count = 1
                else:
                    valid_g_count = 0
            else:
                valid_g_count = 0
                
        neg_q = (valid_g_count != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: f: R \\to T is a ring homomorphism",
    "H_3: f(s) is a unit in T for all s \\in S",
    "H_4: \\phi: R \\to S^{-1}R is the canonical localization map",
    "¬Q: There does not exist a unique ring homomorphism g: S^{-1}R \\to T such that f = g \\circ \\phi"
]

N_HYP = 4
NEG_Q_INDEX = 4