import itertools

# Top-level setup
# No specific named objects required for this domain

def conditions(witness):
    try:
        R = witness.R
        add = witness.add
        mul = witness.mul
        zero = witness.zero
        one = witness.one
        M = witness.M
        add_M = witness.add_M
        smul = witness.smul
        zero_M = witness.zero_M
        I = witness.I
        J = witness.J
    except AttributeError:
        try:
            R = witness['R']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
            one = witness['one']
            M = witness['M']
            add_M = witness['add_M']
            smul = witness['smul']
            zero_M = witness['zero_M']
            I = witness['I']
            J = witness['J']
        except Exception:
            return [False, False, False, False]

    # H1: R is a commutative ring with identity
    def check_H1():
        if not R or zero not in R or one not in R: return False
        for a in R:
            if add(a, zero) != a or add(zero, a) != a: return False
            if mul(a, one) != a or mul(one, a) != a: return False
            has_inv = False
            for b in R:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in R:
                if add(a, b) != add(b, a): return False
                if mul(a, b) != mul(b, a): return False
                for c in R:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
        return True

    # H2: M is an R-module
    def check_H2():
        if not M or zero_M not in M: return False
        for m in M:
            if add_M(m, zero_M) != m or add_M(zero_M, m) != m: return False
            if smul(one, m) != m: return False
            has_inv = False
            for n in M:
                if add_M(m, n) == zero_M and add_M(n, m) == zero_M:
                    has_inv = True
                    break
            if not has_inv: return False
            for n in M:
                if add_M(m, n) != add_M(n, m): return False
                for p in M:
                    if add_M(add_M(m, n), p) != add_M(m, add_M(n, p)): return False
                for r in R:
                    if smul(r, add_M(m, n)) != add_M(smul(r, m), smul(r, n)): return False
            for r in R:
                for s in R:
                    if smul(add(r, s), m) != add_M(smul(r, m), smul(s, m)): return False
                    if smul(mul(r, s), m) != smul(r, smul(s, m)): return False
        return True

    # H3: I + J = R
    def check_H3():
        if not all(i in R for i in I): return False
        if not all(j in R for j in J): return False
        sums = []
        for i in I:
            for j in J:
                s = add(i, j)
                if s not in sums:
                    sums.append(s)
        for r in R:
            if r not in sums: return False
        return True

    def get_submodule(generators):
        closure = list(generators)
        if zero_M not in closure:
            closure.append(zero_M)
        changed = True
        while changed:
            changed = False
            new_elems = []
            for a in closure:
                for r in R:
                    ra = smul(r, a)
                    if ra not in closure and ra not in new_elems:
                        new_elems.append(ra)
                for b in closure:
                    ab = add_M(a, b)
                    if ab not in closure and ab not in new_elems:
                        new_elems.append(ab)
            if new_elems:
                closure.extend(new_elems)
                changed = True
        return closure

    def get_IM(ideal):
        gens = []
        for i in ideal:
            for m in M:
                im = smul(i, m)
                if im not in gens:
                    gens.append(im)
        return get_submodule(gens)

    def get_quotient(submod):
        cosets = []
        for m in M:
            coset = []
            for s in submod:
                ms = add_M(m, s)
                if ms not in coset:
                    coset.append(ms)
            coset = sorted(coset, key=lambda x: str(x))
            if coset not in cosets:
                cosets.append(coset)
        
        def q_add(c1, c2):
            m1 = c1[0]
            m2 = c2[0]
            m = add_M(m1, m2)
            for c in cosets:
                if m in c: return cosets.index(c)
                
        def q_smul(r, c1):
            m1 = c1[0]
            m = smul(r, m1)
            for c in cosets:
                if m in c: return cosets.index(c)
                
        return list(range(len(cosets))), q_add, q_smul

    def check_neg_Q():
        I_cap_J = [x for x in I if x in J]
        I_cap_J_M = get_IM(I_cap_J)
        IM = get_IM(I)
        JM = get_IM(J)
        
        Q1_elems, Q1_add, Q1_smul = get_quotient(I_cap_J_M)
        Q2_elems, Q2_add, Q2_smul = get_quotient(IM)
        Q3_elems, Q3_add, Q3_smul = get_quotient(JM)
        
        P_elems = list(itertools.product(Q2_elems, Q3_elems))
        def P_add(p1, p2):
            return (Q2_add(p1[0], p2[0]), Q3_add(p1[1], p2[1]))
        def P_smul(r, p1):
            return (Q2_smul(r, p1[0]), Q3_smul(r, p1[1]))
            
        if len(Q1_elems) != len(P_elems):
            return True
            
        n = len(Q1_elems)
        if n == 0:
            return False
            
        # Find zero in Q1
        zero1 = None
        for a in Q1_elems:
            if all(Q1_add(a, b) == b for b in Q1_elems):
                zero1 = a
                break
                
        # Find zero in P
        zeroP = None
        for a in P_elems:
            if all(P_add(a, b) == b for b in P_elems):
                zeroP = a
                break
                
        if zero1 is None or zeroP is None:
            return True
            
        # Find generators for Q1
        generators = []
        generated = {zero1}
        for a in Q1_elems:
            if a not in generated:
                generators.append(a)
                new_generated = set(generated)
                changed = True
                while changed:
                    changed = False
                    to_add = set()
                    for g in new_generated | {a}:
                        for r in R:
                            elem = Q1_smul(r, g)
                            if elem not in new_generated and elem not in to_add:
                                to_add.add(elem)
                    for x in list(new_generated) + list(to_add):
                        for y in list(new_generated) + list(to_add):
                            elem = Q1_add(x, y)
                            if elem not in new_generated and elem not in to_add:
                                to_add.add(elem)
                    if to_add:
                        new_generated.update(to_add)
                        changed = True
                generated = new_generated

        # Try all mappings of generators
        for gen_mapped in itertools.product(P_elems, repeat=len(generators)):
            mapping = {zero1: zeroP}
            valid = True
            
            queue = []
            for g, mg in zip(generators, gen_mapped):
                if g in mapping:
                    if mapping[g] != mg:
                        valid = False
                        break
                else:
                    mapping[g] = mg
                    queue.append(g)
                    
            if not valid:
                continue
                
            head = 0
            keys = list(mapping.keys())
            while head < len(keys):
                a = keys[head]
                ma = mapping[a]
                head += 1
                
                for r in R:
                    ra = Q1_smul(r, a)
                    rma = P_smul(r, ma)
                    if ra in mapping:
                        if mapping[ra] != rma:
                            valid = False
                            break
                    else:
                        mapping[ra] = rma
                        keys.append(ra)
                if not valid: break
                
                current_keys = list(mapping.keys())
                for b in current_keys:
                    mb = mapping[b]
                    
                    ab = Q1_add(a, b)
                    mab = P_add(ma, mb)
                    if ab in mapping:
                        if mapping[ab] != mab:
                            valid = False
                            break
                    else:
                        mapping[ab] = mab
                        keys.append(ab)
                        
                    ba = Q1_add(b, a)
                    mba = P_add(mb, ma)
                    if ba in mapping:
                        if mapping[ba] != mba:
                            valid = False
                            break
                    else:
                        mapping[ba] = mba
                        keys.append(ba)
                        
                if not valid: break
                
            if valid and len(mapping) == n:
                if len(set(mapping.values())) == n:
                    return False # Isomorphic, so neg_Q is False
                    
        return True # Not isomorphic, so neg_Q is True

    try:
        h1 = check_H1()
    except Exception:
        h1 = False

    try:
        h2 = check_H2()
    except Exception:
        h2 = False

    try:
        h3 = check_H3()
    except Exception:
        h3 = False

    try:
        nq = check_neg_Q()
    except Exception:
        nq = False

    return [h1, h2, h3, nq]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M is an R-module",
    "H_3: I + J = R",
    "¬Q: M/((I \\cap J)M) is not isomorphic to M/IM \\times M/JM"
]

N_HYP = 3
NEG_Q_INDEX = 3