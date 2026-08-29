import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class RingWrapper:
    def __init__(self, witness):
        self.is_known_associative = False
        if isinstance(witness, tuple) and len(witness) == 4 and isinstance(witness[0], int):
            self.is_known_associative = True
            self.n, self.R, self.I, self.J = witness
            if not self.R:
                raise ValueError("Empty ring")
            if len(self.R) > 200:
                raise ValueError("Ring too large, max 200 elements")
                
            sample = self.R[0]
            if hasattr(sample, 'applyfunc') and hasattr(sample, 'shape'):
                rows, cols = sample.shape
                if rows != cols:
                    raise ValueError("Matrices must be square")
                def to_fast(m):
                    return tuple(tuple(int(val) % self.n for val in row) for row in m.tolist())
                self.R = [to_fast(m) for m in self.R]
                self.I = [to_fast(m) for m in self.I]
                self.J = [to_fast(m) for m in self.J]
                def fast_add(a, b):
                    return tuple(tuple((v1 + v2) % self.n for v1, v2 in zip(r1, r2)) for r1, r2 in zip(a, b))
                def fast_mul(a, b):
                    res = []
                    for i in range(rows):
                        row = []
                        for j in range(cols):
                            val = sum(a[i][k] * b[k][j] for k in range(cols)) % self.n
                            row.append(val)
                        res.append(tuple(row))
                    return tuple(res)
                self.add = fast_add
                self.mul = fast_mul
                self.to_hashable = lambda val: val
            elif isinstance(sample, int) or hasattr(sample, 'is_integer'):
                self.R = [int(val) % self.n for val in self.R]
                self.I = [int(val) % self.n for val in self.I]
                self.J = [int(val) % self.n for val in self.J]
                self.add = lambda a, b: (a + b) % self.n
                self.mul = lambda a, b: (a * b) % self.n
                self.to_hashable = lambda val: val
            else:
                self.add = lambda a, b: (a + b) % self.n
                self.mul = lambda a, b: (a * b) % self.n
                self.to_hashable = lambda val: tuple(val)
        elif hasattr(witness, 'R') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
            self.R = witness.R
            self.I = witness.I
            self.J = witness.J
            self.add = witness.add
            self.mul = witness.mul
            self.to_hashable = getattr(witness, 'to_hashable', lambda val: val)
            if len(self.R) > 200:
                raise ValueError("Ring too large, max 200 elements")
        else:
            raise ValueError("Unknown witness format")
            
        self.hash_to_el = {self.to_hashable(e): e for e in self.R}
        self.R_hashes = set(self.to_hashable(e) for e in self.R)
        self.I_hashes = set(self.to_hashable(e) for e in self.I)
        self.J_hashes = set(self.to_hashable(e) for e in self.J)

    def is_ring(self):
        if not self.R_hashes: return False
        
        for a_h in self.R_hashes:
            for b_h in self.R_hashes:
                a = self.hash_to_el[a_h]
                b = self.hash_to_el[b_h]
                if self.to_hashable(self.add(a, b)) not in self.R_hashes: return False
                if self.to_hashable(self.mul(a, b)) not in self.R_hashes: return False
                
        zeros_list = []
        for z_h in self.R_hashes:
            z = self.hash_to_el[z_h]
            is_z = True
            for a_h in self.R_hashes:
                a = self.hash_to_el[a_h]
                if self.to_hashable(self.add(a, z)) != a_h:
                    is_z = False
                    break
                if self.to_hashable(self.add(z, a)) != a_h:
                    is_z = False
                    break
            if is_z:
                zeros_list.append(z_h)
        if not zeros_list: return False
        zero_h = zeros_list[0]
        
        for a_h in self.R_hashes:
            a = self.hash_to_el[a_h]
            has_inv = False
            for b_h in self.R_hashes:
                b = self.hash_to_el[b_h]
                if self.to_hashable(self.add(a, b)) != self.to_hashable(self.add(b, a)):
                    return False
                if self.to_hashable(self.add(a, b)) == zero_h:
                    has_inv = True
            if not has_inv: return False
            
        if not self.is_known_associative:
            for a_h in self.R_hashes:
                a = self.hash_to_el[a_h]
                for b_h in self.R_hashes:
                    b = self.hash_to_el[b_h]
                    for c_h in self.R_hashes:
                        c = self.hash_to_el[c_h]
                        
                        ab = self.add(a, b)
                        ab_c = self.add(ab, c)
                        bc = self.add(b, c)
                        a_bc = self.add(a, bc)
                        if self.to_hashable(ab_c) != self.to_hashable(a_bc): return False
                        
                        ab_m = self.mul(a, b)
                        ab_c_m = self.mul(ab_m, c)
                        bc_m = self.mul(b, c)
                        a_bc_m = self.mul(a, bc_m)
                        if self.to_hashable(ab_c_m) != self.to_hashable(a_bc_m): return False
                        
                        a_bpc = self.mul(a, bc)
                        ab_p_ac = self.add(ab_m, self.mul(a, c))
                        if self.to_hashable(a_bpc) != self.to_hashable(ab_p_ac): return False
                        
                        apb_c = self.mul(ab, c)
                        ac_p_bc = self.add(self.mul(a, c), bc_m)
                        if self.to_hashable(apb_c) != self.to_hashable(ac_p_bc): return False
                        
        return True

    def is_ideal(self, S_hashes):
        if not S_hashes.issubset(self.R_hashes):
            return False
        if not S_hashes:
            return False
            
        for a_h in S_hashes:
            for b_h in S_hashes:
                c = self.add(self.hash_to_el[a_h], self.hash_to_el[b_h])
                if self.to_hashable(c) not in S_hashes:
                    return False
                    
        zero_h = None
        for z_h in S_hashes:
            z = self.hash_to_el[z_h]
            is_z = True
            for a_h in S_hashes:
                a = self.hash_to_el[a_h]
                if self.to_hashable(self.add(a, z)) != a_h:
                    is_z = False
                    break
            if is_z:
                zero_h = z_h
                break
        if zero_h is None: return False
        
        for a_h in S_hashes:
            a = self.hash_to_el[a_h]
            has_inv = False
            for b_h in S_hashes:
                b = self.hash_to_el[b_h]
                if self.to_hashable(self.add(a, b)) == zero_h:
                    has_inv = True
                    break
            if not has_inv: return False
            
        for s_h in S_hashes:
            s = self.hash_to_el[s_h]
            for r_h in self.R_hashes:
                r = self.hash_to_el[r_h]
                if self.to_hashable(self.mul(s, r)) not in S_hashes:
                    return False
                if self.to_hashable(self.mul(r, s)) not in S_hashes:
                    return False
                    
        return True

    def check_I_plus_J_eq_R(self):
        sums = set()
        for i_h in self.I_hashes:
            for j_h in self.J_hashes:
                c = self.add(self.hash_to_el[i_h], self.hash_to_el[j_h])
                sums.add(self.to_hashable(c))
        return sums == self.R_hashes

    def get_additive_closure(self, elements):
        closure_dict = {}
        for e in elements:
            closure_dict[self.to_hashable(e)] = e
            
        if not closure_dict:
            return set()
            
        added = True
        while added:
            added = False
            new_elements = {}
            for a in closure_dict.values():
                for b in closure_dict.values():
                    c = self.add(a, b)
                    c_hash = self.to_hashable(c)
                    if c_hash not in closure_dict and c_hash not in new_elements:
                        new_elements[c_hash] = c
            if new_elements:
                closure_dict.update(new_elements)
                added = True
                
        return set(closure_dict.keys())

    def check_conclusion(self):
        intersection = self.I_hashes.intersection(self.J_hashes)
        
        IJ_gens = []
        for i_h in self.I_hashes:
            for j_h in self.J_hashes:
                IJ_gens.append(self.mul(self.hash_to_el[i_h], self.hash_to_el[j_h]))
        IJ_hashes = self.get_additive_closure(IJ_gens)
        
        JI_gens = []
        for j_h in self.J_hashes:
            for i_h in self.I_hashes:
                JI_gens.append(self.mul(self.hash_to_el[j_h], self.hash_to_el[i_h]))
        JI_hashes = self.get_additive_closure(JI_gens)
        
        sum_hashes = set()
        if not IJ_hashes and not JI_hashes:
            sum_hashes = set()
        elif not IJ_hashes:
            sum_hashes = JI_hashes
        elif not JI_hashes:
            sum_hashes = IJ_hashes
        else:
            for a_h in IJ_hashes:
                for b_h in JI_hashes:
                    c = self.add(self.hash_to_el[a_h], self.hash_to_el[b_h])
                    sum_hashes.add(self.to_hashable(c))
                    
        return intersection == sum_hashes

def conditions(witness) -> list[bool]:
    try:
        wrapper = RingWrapper(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = wrapper.is_ring() and wrapper.is_ideal(wrapper.I_hashes) and wrapper.is_ideal(wrapper.J_hashes)
    except Exception:
        h1 = False
        
    try:
        h2 = wrapper.check_I_plus_J_eq_R()
    except Exception:
        h2 = False
        
    try:
        neg_q = not wrapper.check_conclusion()
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are two-sided ideals of R",
    "H_2: I + J = R",
    "¬Q: I \\cap J \\neq IJ + JI"
]

N_HYP = 2
NEG_Q_INDEX = 2