import itertools

# Top-level setup
# (No specific named groups needed for this ring theory conjecture)
# The witness will provide the rings, maps, and multiplicative sets.

def get_attr(w, name):
    if isinstance(w, dict):
        return w[name]
    return getattr(w, name)

def conditions(witness):
    try:
        indices = get_attr(witness, 'indices')
        le = get_attr(witness, 'le')
        R = get_attr(witness, 'R')
        add = get_attr(witness, 'add')
        mul = get_attr(witness, 'mul')
        zero = get_attr(witness, 'zero')
        one = get_attr(witness, 'one')
        phi = get_attr(witness, 'phi')
        S_i = get_attr(witness, 'S_i')
        R_limit = get_attr(witness, 'R_limit')
        R_limit_add = get_attr(witness, 'R_limit_add')
        R_limit_mul = get_attr(witness, 'R_limit_mul')
        R_limit_zero = get_attr(witness, 'R_limit_zero')
        R_limit_one = get_attr(witness, 'R_limit_one')
        phi_infty = get_attr(witness, 'phi_infty')
        S = get_attr(witness, 'S')
    except Exception:
        return [False, False, False, False]

    def check_h1():
        if not indices: return False
        for i in indices:
            if not le(i, i): return False
        for i in indices:
            for j in indices:
                for k in indices:
                    if le(i, j) and le(j, k) and not le(i, k): return False
        for i in indices:
            for j in indices:
                has_upper = False
                for k in indices:
                    if le(i, k) and le(j, k):
                        has_upper = True
                        break
                if not has_upper: return False
                
        for i in indices:
            elems = R[i]
            z = zero[i]
            o = one[i]
            a = add[i]
            m = mul[i]
            if z not in elems or o not in elems: return False
            for x in elems:
                if a(x, z) != x or a(z, x) != x: return False
                if m(x, o) != x or m(o, x) != x: return False
                has_neg = False
                for y in elems:
                    if a(x, y) == z and a(y, x) == z:
                        has_neg = True
                        break
                if not has_neg: return False
                for y in elems:
                    if a(x, y) not in elems: return False
                    if m(x, y) not in elems: return False
                    if a(x, y) != a(y, x): return False
                    if m(x, y) != m(y, x): return False
                    for k_el in elems:
                        if a(a(x, y), k_el) != a(x, a(y, k_el)): return False
                        if m(m(x, y), k_el) != m(x, m(y, k_el)): return False
                        if m(x, a(y, k_el)) != a(m(x, y), m(x, k_el)): return False

        for i in indices:
            for j in indices:
                if le(i, j):
                    p = phi[(i, j)]
                    if p(one[i]) != one[j]: return False
                    for x in R[i]:
                        if p(x) not in R[j]: return False
                        for y in R[i]:
                            if p(add[i](x, y)) != add[j](p(x), p(y)): return False
                            if p(mul[i](x, y)) != mul[j](p(x), p(y)): return False
        for i in indices:
            for x in R[i]:
                if phi[(i, i)](x) != x: return False
        for i in indices:
            for j in indices:
                for k in indices:
                    if le(i, j) and le(j, k):
                        for x in R[i]:
                            if phi[(j, k)](phi[(i, j)](x)) != phi[(i, k)](x): return False
        return True

    def check_h2():
        for i in indices:
            Si = S_i[i]
            if one[i] not in Si: return False
            for x in Si:
                if x not in R[i]: return False
                for y in Si:
                    if mul[i](x, y) not in Si: return False
        for i in indices:
            for j in indices:
                if le(i, j):
                    for x in S_i[i]:
                        if phi[(i, j)](x) not in S_i[j]: return False
        return True

    def check_h3():
        elems = R_limit
        z = R_limit_zero
        o = R_limit_one
        a = R_limit_add
        m = R_limit_mul
        if z not in elems or o not in elems: return False
        for x in elems:
            if a(x, z) != x or a(z, x) != x: return False
            if m(x, o) != x or m(o, x) != x: return False
            has_neg = False
            for y in elems:
                if a(x, y) == z and a(y, x) == z:
                    has_neg = True
                    break
            if not has_neg: return False
            for y in elems:
                if a(x, y) not in elems: return False
                if m(x, y) not in elems: return False
                if a(x, y) != a(y, x): return False
                if m(x, y) != m(y, x): return False
                for k_el in elems:
                    if a(a(x, y), k_el) != a(x, a(y, k_el)): return False
                    if m(m(x, y), k_el) != m(x, m(y, k_el)): return False
                    if m(x, a(y, k_el)) != a(m(x, y), m(x, k_el)): return False
                    
        for i in indices:
            p = phi_infty[i]
            if p(one[i]) != o: return False
            for x in R[i]:
                if p(x) not in elems: return False
                for y in R[i]:
                    if p(add[i](x, y)) != a(p(x), p(y)): return False
                    if p(mul[i](x, y)) != m(p(x), p(y)): return False
                    
        for i in indices:
            for j in indices:
                if le(i, j):
                    for x in R[i]:
                        if phi_infty[j](phi[(i, j)](x)) != phi_infty[i](x): return False
                        
        for x in elems:
            is_image = False
            for i in indices:
                for y in R[i]:
                    if phi_infty[i](y) == x:
                        is_image = True
                        break
                if is_image: break
            if not is_image: return False
            
        for i in indices:
            for x in R[i]:
                for y in R[i]:
                    if phi_infty[i](x) == phi_infty[i](y):
                        found = False
                        for j in indices:
                            if le(i, j) and phi[(i, j)](x) == phi[(i, j)](y):
                                found = True
                                break
                        if not found: return False
        return True

    def check_neg_q():
        if R_limit_one not in S: return True
        for x in S:
            if x not in R_limit: return True
            for y in S:
                if R_limit_mul(x, y) not in S: return True
                
        def get_neg(elems, a, z, x):
            for y in elems:
                if a(x, y) == z: return y
            raise ValueError("No negative found")
            
        pairs_SR = [(r, s) for r in R_limit for s in S]
        def eq_SR(p1, p2):
            r1, s1 = p1
            r2, s2 = p2
            diff = R_limit_add(R_limit_mul(r1, s2), get_neg(R_limit, R_limit_add, R_limit_zero, R_limit_mul(r2, s1)))
            for t in S:
                if R_limit_mul(t, diff) == R_limit_zero:
                    return True
            return False
            
        classes_SR = []
        for p in pairs_SR:
            found = False
            for c in classes_SR:
                if eq_SR(p, c[0]):
                    c.append(p)
                    found = True
                    break
            if not found:
                classes_SR.append([p])
                
        SR_elems = list(range(len(classes_SR)))
        def SR_add(i, j):
            r1, s1 = classes_SR[i][0]
            r2, s2 = classes_SR[j][0]
            num = R_limit_add(R_limit_mul(r1, s2), R_limit_mul(r2, s1))
            den = R_limit_mul(s1, s2)
            for k, c in enumerate(classes_SR):
                if eq_SR((num, den), c[0]): return k
            return None
            
        def SR_mul(i, j):
            r1, s1 = classes_SR[i][0]
            r2, s2 = classes_SR[j][0]
            num = R_limit_mul(r1, r2)
            den = R_limit_mul(s1, s2)
            for k, c in enumerate(classes_SR):
                if eq_SR((num, den), c[0]): return k
            return None
            
        L_i_classes = {}
        L_i_add = {}
        L_i_mul = {}
        for i in indices:
            pairs = [(r, s) for r in R[i] for s in S_i[i]]
            def eq_L(p1, p2, idx=i):
                r1, s1 = p1
                r2, s2 = p2
                diff = add[idx](mul[idx](r1, s2), get_neg(R[idx], add[idx], zero[idx], mul[idx](r2, s1)))
                for t in S_i[idx]:
                    if mul[idx](t, diff) == zero[idx]:
                        return True
                return False
            classes = []
            for p in pairs:
                found = False
                for c in classes:
                    if eq_L(p, c[0]):
                        c.append(p)
                        found = True
                        break
                if not found:
                    classes.append([p])
            L_i_classes[i] = classes
            
            def make_add(idx, cls):
                def f(a_idx, b_idx):
                    r1, s1 = cls[a_idx][0]
                    r2, s2 = cls[b_idx][0]
                    num = add[idx](mul[idx](r1, s2), mul[idx](r2, s1))
                    den = mul[idx](s1, s2)
                    for k, c in enumerate(cls):
                        if eq_L((num, den), c[0], idx): return k
                    return None
                return f
                
            def make_mul(idx, cls):
                def f(a_idx, b_idx):
                    r1, s1 = cls[a_idx][0]
                    r2, s2 = cls[b_idx][0]
                    num = mul[idx](r1, r2)
                    den = mul[idx](s1, s2)
                    for k, c in enumerate(cls):
                        if eq_L((num, den), c[0], idx): return k
                    return None
                return f
                
            L_i_add[i] = make_add(i, classes)
            L_i_mul[i] = make_mul(i, classes)
            
        L_elements = [(i, k) for i in indices for k in range(len(L_i_classes[i]))]
        
        def psi(i, j, L_i_idx):
            r, s = L_i_classes[i][L_i_idx][0]
            pr = phi[(i, j)](r)
            ps = phi[(i, j)](s)
            def eq_L_j(p1, p2):
                r1, s1 = p1
                r2, s2 = p2
                diff = add[j](mul[j](r1, s2), get_neg(R[j], add[j], zero[j], mul[j](r2, s1)))
                for t in S_i[j]:
                    if mul[j](t, diff) == zero[j]:
                        return True
                return False
            for k, c in enumerate(L_i_classes[j]):
                if eq_L_j((pr, ps), c[0]):
                    return k
            return None
            
        def eq_lim(e1, e2):
            i, x = e1
            j, y = e2
            for k in indices:
                if le(i, k) and le(j, k):
                    if psi(i, k, x) == psi(j, k, y):
                        return True
            return False
            
        lim_classes = []
        for e in L_elements:
            found = False
            for c in lim_classes:
                if eq_lim(e, c[0]):
                    c.append(e)
                    found = True
                    break
            if not found:
                lim_classes.append([e])
                
        lim_elems = list(range(len(lim_classes)))
        
        def lim_add(idx1, idx2):
            i, x = lim_classes[idx1][0]
            j, y = lim_classes[idx2][0]
            for k in indices:
                if le(i, k) and le(j, k):
                    xk = psi(i, k, x)
                    yk = psi(j, k, y)
                    sum_k = L_i_add[k](xk, yk)
                    for c_idx, c in enumerate(lim_classes):
                        if eq_lim((k, sum_k), c[0]):
                            return c_idx
            return None
            
        def lim_mul(idx1, idx2):
            i, x = lim_classes[idx1][0]
            j, y = lim_classes[idx2][0]
            for k in indices:
                if le(i, k) and le(j, k):
                    xk = psi(i, k, x)
                    yk = psi(j, k, y)
                    prod_k = L_i_mul[k](xk, yk)
                    for c_idx, c in enumerate(lim_classes):
                        if eq_lim((k, prod_k), c[0]):
                            return c_idx
            return None
            
        if len(lim_elems) != len(SR_elems):
            return True
            
        for p in itertools.permutations(SR_elems):
            mapping = dict(zip(lim_elems, p))
            is_iso = True
            for x in lim_elems:
                for y in lim_elems:
                    if mapping[lim_add(x, y)] != SR_add(mapping[x], mapping[y]):
                        is_iso = False
                        break
                    if mapping[lim_mul(x, y)] != SR_mul(mapping[x], mapping[y]):
                        is_iso = False
                        break
                if not is_iso:
                    break
            if is_iso:
                return False
                
        return True

    def safe_check(func):
        try:
            return bool(func())
        except Exception:
            return False

    return [safe_check(check_h1), safe_check(check_h2), safe_check(check_h3), safe_check(check_neg_q)]

CONDITION_LABELS = [
    "H_1: (R_i, phi_ij) is a directed system of commutative rings",
    "H_2: S_i subseteq R_i are multiplicative subsets such that phi_ij(S_i) subseteq S_j",
    "H_3: R is the direct limit lim R_i",
    "¬Q: The direct limit of the localized rings lim (S_i^-1 R_i) is NOT isomorphic to S^-1 R"
]

N_HYP = 3
NEG_Q_INDEX = 3