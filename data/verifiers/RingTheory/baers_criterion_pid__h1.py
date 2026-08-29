import itertools

class RingModuleWitness:
    """
    A witness object representing a finite commutative ring R and a finite R-module E.
    R_size: number of elements in R (elements are 0, 1, ..., R_size-1)
    R_add: callable(a, b) returning a + b in R
    R_mul: callable(a, b) returning a * b in R
    R_zero: the zero element of R
    R_one: the multiplicative identity of R
    E_size: number of elements in E (elements are 0, 1, ..., E_size-1)
    E_add: callable(u, v) returning u + v in E
    E_zero: the zero element of E
    act: callable(r, u) returning r * u in E
    """
    def __init__(self, R_size, R_add, R_mul, R_zero, R_one, E_size, E_add, E_zero, act):
        self.R_size = R_size
        self.R_add = R_add
        self.R_mul = R_mul
        self.R_zero = R_zero
        self.R_one = R_one
        self.E_size = E_size
        self.E_add = E_add
        self.E_zero = E_zero
        self.act = act

def get_ideal(R_size, R_add, R_mul, R_zero, generators):
    ideal = set(generators)
    ideal.add(R_zero)
    changed = True
    while changed:
        changed = False
        new_elements = set()
        for x in ideal:
            for y in ideal:
                new_elements.add(R_add(x, y))
            for r in range(R_size):
                new_elements.add(R_mul(r, x))
                new_elements.add(R_mul(x, r))
        if not new_elements.issubset(ideal):
            ideal.update(new_elements)
            changed = True
    return sorted(list(ideal))

def get_generators(I, R_size, R_add, R_mul, R_zero):
    I_set = set(I)
    for k in range(1, min(len(I), 4) + 1):
        for subset in itertools.combinations(I, k):
            if set(get_ideal(R_size, R_add, R_mul, R_zero, list(subset))) == I_set:
                return list(subset)
    return list(I)

def get_homomorphisms(I, R_size, R_add, R_mul, R_zero, E_size, E_add, E_zero, act):
    if not I or I == [R_zero]:
        return [{R_zero: E_zero}]
        
    gens = get_generators(I, R_size, R_add, R_mul, R_zero)
    homs = []
    I_set = set(I)
    
    for gen_vals in itertools.product(range(E_size), repeat=len(gens)):
        f = {}
        for g, v in zip(gens, gen_vals):
            f[g] = v
            
        valid = True
        changed = True
        while changed and valid:
            changed = False
            for r in range(R_size):
                for x in list(f.keys()):
                    z = R_mul(r, x)
                    if z in I_set:
                        val = act(r, f[x])
                        if z in f:
                            if f[z] != val:
                                valid = False
                                break
                        else:
                            f[z] = val
                            changed = True
                if not valid: break
            if not valid: break
            
            for x in list(f.keys()):
                for y in list(f.keys()):
                    z = R_add(x, y)
                    if z in I_set:
                        val = E_add(f[x], f[y])
                        if z in f:
                            if f[z] != val:
                                valid = False
                                break
                        else:
                            f[z] = val
                            changed = True
                if not valid: break
                
        if valid and len(f) == len(I):
            homs.append(f)
            
    return homs

def can_extend(f, I, E_size, act):
    for e_prime in range(E_size):
        valid = True
        for x in I:
            if f[x] != act(x, e_prime):
                valid = False
                break
        if valid:
            return True
    return False

def check_R_module(R_size, R_add, R_mul, R_zero, R_one, E_size, E_add, E_zero, act):
    for a in range(R_size):
        if R_add(a, R_zero) != a: return False
        if R_add(R_zero, a) != a: return False
        if R_mul(a, R_zero) != R_zero: return False
        if R_mul(R_zero, a) != R_zero: return False
        if R_mul(a, R_one) != a: return False
        if R_mul(R_one, a) != a: return False
        for b in range(R_size):
            if R_add(a, b) != R_add(b, a): return False
            if R_mul(a, b) != R_mul(b, a): return False
            for c in range(R_size):
                if R_add(R_add(a, b), c) != R_add(a, R_add(b, c)): return False
                if R_mul(R_mul(a, b), c) != R_mul(a, R_mul(b, c)): return False
                if R_mul(a, R_add(b, c)) != R_add(R_mul(a, b), R_mul(a, c)): return False
                
    for u in range(E_size):
        if E_add(u, E_zero) != u: return False
        if E_add(E_zero, u) != u: return False
        for v in range(E_size):
            if E_add(u, v) != E_add(v, u): return False
            for w in range(E_size):
                if E_add(E_add(u, v), w) != E_add(u, E_add(v, w)): return False
                
    for u in range(E_size):
        if act(R_one, u) != u: return False
        for v in range(E_size):
            for r in range(R_size):
                if act(r, E_add(u, v)) != E_add(act(r, u), act(r, v)): return False
        for r in range(R_size):
            for s in range(R_size):
                if act(R_add(r, s), u) != E_add(act(r, u), act(s, u)): return False
                if act(R_mul(r, s), u) != act(r, act(s, u)): return False
                
    return True

def check_principal_ideals_extend(R_size, R_add, R_mul, R_zero, E_size, E_add, E_zero, act):
    for r in range(R_size):
        if r == R_zero:
            continue
        I = get_ideal(R_size, R_add, R_mul, R_zero, [r])
        homs = get_homomorphisms(I, R_size, R_add, R_mul, R_zero, E_size, E_add, E_zero, act)
        for f in homs:
            if not can_extend(f, I, E_size, act):
                return False
    return True

def check_not_injective(R_size, R_add, R_mul, R_zero, E_size, E_add, E_zero, act):
    principal_ideals = []
    for x in range(R_size):
        principal_ideals.append(set(get_ideal(R_size, R_add, R_mul, R_zero, [x])))

    ideals = set()
    ideals.add(tuple([R_zero]))
    changed = True
    while changed:
        changed = False
        new_ideals = set()
        for I in ideals:
            for P in principal_ideals:
                sum_ideal = set(I) | P
                sum_ideal = get_ideal(R_size, R_add, R_mul, R_zero, list(sum_ideal))
                new_ideals.add(tuple(sum_ideal))
        if not new_ideals.issubset(ideals):
            ideals.update(new_ideals)
            changed = True
            if len(ideals) > 1000:
                return False

    for I in ideals:
        homs = get_homomorphisms(list(I), R_size, R_add, R_mul, R_zero, E_size, E_add, E_zero, act)
        for f in homs:
            if not can_extend(f, list(I), E_size, act):
                return True
                
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R_size = int(witness['R_size'])
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            R_zero = int(witness['R_zero'])
            R_one = int(witness['R_one'])
            E_size = int(witness['E_size'])
            E_add = witness['E_add']
            E_zero = int(witness['E_zero'])
            act = witness['act']
        else:
            R_size = int(witness.R_size)
            R_add = witness.R_add
            R_mul = witness.R_mul
            R_zero = int(witness.R_zero)
            R_one = int(witness.R_one)
            E_size = int(witness.E_size)
            E_add = witness.E_add
            E_zero = int(witness.E_zero)
            act = witness.act
            
        if not (1 <= R_size <= 16 and 1 <= E_size <= 32):
            return [False, False, False]
        if not (0 <= R_zero < R_size and 0 <= R_one < R_size):
            return [False, False, False]
        if not (0 <= E_zero < E_size):
            return [False, False, False]
            
        def safe_R_add(a, b):
            res = int(R_add(a, b))
            if not (0 <= res < R_size): raise ValueError
            return res
            
        def safe_R_mul(a, b):
            res = int(R_mul(a, b))
            if not (0 <= res < R_size): raise ValueError
            return res
            
        def safe_E_add(a, b):
            res = int(E_add(a, b))
            if not (0 <= res < E_size): raise ValueError
            return res
            
        def safe_act(r, u):
            res = int(act(r, u))
            if not (0 <= res < E_size): raise ValueError
            return res
            
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_R_module(R_size, safe_R_add, safe_R_mul, R_zero, R_one, E_size, safe_E_add, E_zero, safe_act)
    except Exception:
        h1 = False
        
    try:
        h2 = check_principal_ideals_extend(R_size, safe_R_add, safe_R_mul, R_zero, E_size, safe_E_add, E_zero, safe_act)
    except Exception:
        h2 = False
        
    try:
        neg_q = check_not_injective(R_size, safe_R_add, safe_R_mul, R_zero, E_size, safe_E_add, E_zero, safe_act)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is an R-module",
    "H_2: For every non-zero r in R, any homomorphism f: (r) -> E extends to R -> E",
    "¬Q: E is not an injective R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2