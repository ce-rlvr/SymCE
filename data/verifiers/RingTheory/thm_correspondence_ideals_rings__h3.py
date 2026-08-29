import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
class ZRing:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
    def add(self, a, b):
        return (a + b) % self.n
    def mul(self, a, b):
        return (a * b) % self.n
    def __repr__(self):
        return f"ZRing({self.n})"
    def __eq__(self, other):
        return isinstance(other, ZRing) and self.n == other.n
    def __hash__(self):
        return hash(self.n)

class RingWrapper:
    def __init__(self, elements, add, mul, zero):
        self.elements = list(elements)
        self.add = add
        self.mul = mul
        self.zero = zero

    def get_ideal_generated_by(self, generators):
        if self.zero is None:
            return frozenset(generators)
        ideal = set(generators)
        ideal.add(self.zero)
        
        inverses = {}
        for x in self.elements:
            for y in self.elements:
                if self.add(x, y) == self.zero:
                    inverses[x] = y
                    break
                    
        changed = True
        while changed:
            changed = False
            new_elements = set()
            for x in ideal:
                inv_x = inverses.get(x, x)
                if inv_x not in ideal:
                    new_elements.add(inv_x)
                for y in ideal:
                    s = self.add(x, y)
                    if s not in ideal: new_elements.add(s)
            for r in self.elements:
                for x in ideal:
                    p1 = self.mul(r, x)
                    if p1 not in ideal: new_elements.add(p1)
                    p2 = self.mul(x, r)
                    if p2 not in ideal: new_elements.add(p2)
            if new_elements:
                ideal.update(new_elements)
                changed = True
        return frozenset(ideal)

    def get_all_ideals(self):
        if self.zero is None:
            return []
        principal_ideals = set()
        for x in self.elements:
            principal_ideals.add(self.get_ideal_generated_by([x]))
        
        ideals = set(principal_ideals)
        changed = True
        while changed:
            changed = False
            new_ideals = set()
            for I1 in ideals:
                for I2 in ideals:
                    I_sum = set()
                    for x in I1:
                        for y in I2:
                            I_sum.add(self.add(x, y))
                    I_sum = frozenset(I_sum)
                    if I_sum not in ideals and I_sum not in new_ideals:
                        new_ideals.add(I_sum)
            if new_ideals:
                ideals.update(new_ideals)
                changed = True
        return list(ideals)

def parse_witness(witness):
    if isinstance(witness, dict):
        if 'n' in witness and 'm' in witness and 'k' in witness:
            return parse_witness((witness['n'], witness['m'], witness['k']))
        if 'R' in witness and 'S' in witness and 'f' in witness and 'K' in witness:
            return parse_witness((witness['R'], witness['S'], witness['f'], witness['K']))

    if isinstance(witness, tuple) and len(witness) == 3:
        n, m, k = witness
        if isinstance(n, int) and isinstance(m, int) and n > 0 and m > 0:
            R_el = list(range(n))
            R_add = lambda a, b: (a + b) % n
            R_mul = lambda a, b: (a * b) % n
            R_zero = 0
            R_wrap = RingWrapper(R_el, R_add, R_mul, R_zero)
            
            S_el = list(range(m))
            S_add = lambda a, b: (a + b) % m
            S_mul = lambda a, b: (a * b) % m
            S_zero = 0
            S_wrap = RingWrapper(S_el, S_add, S_mul, S_zero)
            
            f_func = lambda x: x % m
            
            if isinstance(k, int):
                K_set = R_wrap.get_ideal_generated_by([k % n])
            elif isinstance(k, (list, tuple, set)):
                K_set = R_wrap.get_ideal_generated_by([x % n for x in k])
            else:
                return None
                
            return R_wrap, S_wrap, f_func, K_set

    if isinstance(witness, tuple) and len(witness) == 4:
        R, S, f, K = witness
        if hasattr(R, 'elements') and hasattr(R, 'add') and hasattr(R, 'mul') and \
           hasattr(S, 'elements') and hasattr(S, 'add') and hasattr(S, 'mul'):
            
            R_zero = getattr(R, 'zero', None)
            if R_zero is None:
                for z in R.elements:
                    if all(R.add(z, a) == a for a in R.elements):
                        R_zero = z
                        break
            
            S_zero = getattr(S, 'zero', None)
            if S_zero is None:
                for z in S.elements:
                    if all(S.add(z, a) == a for a in S.elements):
                        S_zero = z
                        break

            R_wrap = RingWrapper(R.elements, R.add, R.mul, R_zero)
            S_wrap = RingWrapper(S.elements, S.add, S.mul, S_zero)
            
            if isinstance(f, dict):
                f_func = lambda x, d=f: d.get(x, S_zero)
            elif callable(f):
                f_func = f
            else:
                return None
                
            if isinstance(K, (list, set, frozenset, tuple)):
                K_set = frozenset(K)
            elif isinstance(K, int):
                K_set = R_wrap.get_ideal_generated_by([K])
            else:
                return None
                
            return R_wrap, S_wrap, f_func, K_set
            
    if isinstance(witness, tuple) and len(witness) == 8:
        R_el, R_add, R_mul, S_el, S_add, S_mul, f, K = witness
        if not (isinstance(R_el, (list, tuple, set)) and isinstance(S_el, (list, tuple, set))):
            return None
            
        R_zero = None
        for z in R_el:
            if all(R_add(z, a) == a for a in R_el):
                R_zero = z
                break
        S_zero = None
        for z in S_el:
            if all(S_add(z, a) == a for a in S_el):
                S_zero = z
                break
                
        R_wrap = RingWrapper(R_el, R_add, R_mul, R_zero)
        S_wrap = RingWrapper(S_el, S_add, S_mul, S_zero)
        
        if isinstance(f, dict):
            f_func = lambda x, d=f: d.get(x, S_zero)
        elif callable(f):
            f_func = f
        else:
            return None
            
        if isinstance(K, (list, set, frozenset, tuple)):
            K_set = frozenset(K)
        elif isinstance(K, int):
            K_set = R_wrap.get_ideal_generated_by([K])
        else:
            return None
            
        return R_wrap, S_wrap, f_func, K_set

    return None

def conditions(witness):
    parsed = parse_witness(witness)
    if parsed is None:
        return [False, False, False]
    
    R_wrap, S_wrap, f_func, K_set = parsed
    
    def check_ring(wrap):
        el = wrap.elements
        add = wrap.add
        mul = wrap.mul
        zero = wrap.zero
        if zero is None: return False
        if zero not in el: return False
        for a in el:
            for b in el:
                try:
                    if add(a, b) not in el: return False
                    if mul(a, b) not in el: return False
                except Exception:
                    return False
        for a in el:
            for b in el:
                for c in el:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
        for a in el:
            for b in el:
                if add(a, b) != add(b, a): return False
        for a in el:
            if add(zero, a) != a: return False
            if add(a, zero) != a: return False
        for a in el:
            if not any(add(a, b) == zero for b in el): return False
        for a in el:
            for b in el:
                for c in el:
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
        for a in el:
            for b in el:
                for c in el:
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        return True

    try:
        h1 = check_ring(R_wrap) and check_ring(S_wrap)
    except Exception:
        h1 = False

    try:
        is_hom = True
        for a in R_wrap.elements:
            if f_func(a) not in S_wrap.elements:
                is_hom = False
                break
        if is_hom:
            for a in R_wrap.elements:
                for b in R_wrap.elements:
                    if f_func(R_wrap.add(a, b)) != S_wrap.add(f_func(a), f_func(b)):
                        is_hom = False
                        break
                    if f_func(R_wrap.mul(a, b)) != S_wrap.mul(f_func(a), f_func(b)):
                        is_hom = False
                        break
                if not is_hom: break
        
        if is_hom:
            image = set(f_func(x) for x in R_wrap.elements)
            is_surj = (image == set(S_wrap.elements))
        else:
            is_surj = False
            
        h2 = is_hom and is_surj
    except Exception:
        h2 = False

    try:
        R_ideals = R_wrap.get_all_ideals()
        S_ideals = S_wrap.get_all_ideals()
        
        domain = [I for I in R_ideals if K_set.issubset(I)]
        
        mapped_ideals = []
        is_bijection = True
        
        for I in domain:
            f_I = frozenset(f_func(x) for x in I)
            if f_I not in S_ideals:
                is_bijection = False
                break
            mapped_ideals.append(f_I)
            
        if is_bijection:
            if len(domain) != len(S_ideals):
                is_bijection = False
            else:
                if set(mapped_ideals) != set(S_ideals):
                    is_bijection = False
                    
        neg_q = not is_bijection
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a surjective ring homomorphism",
    "¬Q: The map I |-> f(I) is not a bijection from the set of ideals of R containing K to the set of ideals of S"
]

N_HYP = 2
NEG_Q_INDEX = 2