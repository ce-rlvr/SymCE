import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: S is the set of all non-zero elements of R",
    "¬Q: The localized ring S^{-1}R is not a field"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R = witness
            if isinstance(R, int):
                S = list(range(1, R))
            else:
                return [False, False]
                
        if isinstance(R, int) and R >= 2:
            n = R
            
            try:
                S_original = set(S)
                S_set = set(x % n for x in S)
            except TypeError:
                return [False, False]
                
            h1 = (S_original == set(range(1, n)))
            
            closure = set(S_set)
            if not closure:
                closure.add(1)
            else:
                queue = list(S_set)
                while queue:
                    curr = queue.pop(0)
                    for s in S_set:
                        nxt = (curr * s) % n
                        if nxt not in closure:
                            closure.add(nxt)
                            queue.append(nxt)
            
            if 0 in closure:
                is_field = False
            else:
                if h1:
                    is_field = sympy.isprime(n)
                else:
                    if n > 200:
                        return [False, False]
                    
                    elements = []
                    for r in range(n):
                        for s in closure:
                            elements.append((r, s))
                    
                    classes = []
                    for e in elements:
                        found = False
                        for c in classes:
                            r1, s1 = e
                            r2, s2 = c[0]
                            equiv = False
                            for u in closure:
                                if (u * (r1 * s2 - r2 * s1)) % n == 0:
                                    equiv = True
                                    break
                            if equiv:
                                c.append(e)
                                found = True
                                break
                        if not found:
                            classes.append([e])
                    
                    if len(classes) < 2:
                        is_field = False
                    else:
                        zero_class = None
                        for c in classes:
                            r1, s1 = c[0]
                            equiv_zero = False
                            for u in closure:
                                if (u * r1) % n == 0:
                                    equiv_zero = True
                                    break
                            if equiv_zero:
                                zero_class = c
                                break
                        
                        is_field = True
                        for c in classes:
                            if c == zero_class:
                                continue
                            r1, s1 = c[0]
                            has_inv = False
                            for d in classes:
                                r2, s2 = d[0]
                                rp, sp = (r1 * r2) % n, (s1 * s2) % n
                                equiv_one = False
                                for u in closure:
                                    if (u * (rp * 1 - 1 * sp)) % n == 0:
                                        equiv_one = True
                                        break
                                if equiv_one:
                                    has_inv = True
                                    break
                            if not has_inv:
                                is_field = False
                                break
            
            neg_q = not is_field
            return [bool(h1), bool(neg_q)]
            
        return [False, False]
    except Exception:
        return [False, False]