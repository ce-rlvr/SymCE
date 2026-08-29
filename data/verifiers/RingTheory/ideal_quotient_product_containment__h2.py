import sympy
from sympy import ZZ, QQ
import itertools

ZZ = sympy.ZZ
QQ = sympy.QQ

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "¬Q: (I:J)J is not a subset of I"
]

N_HYP = 2
NEG_Q_INDEX = 2

def normalize(witness):
    if isinstance(witness, dict):
        if 'n' in witness:
            n = witness['n']
            elements = list(range(n))
            add = lambda x, y: (x + y) % n
            mul = lambda x, y: (x * y) % n
            zero = 0
            return elements, add, mul, zero, list(witness['J']), list(witness['I'])
        else:
            elements = list(witness['R'])
            add = witness['add']
            mul = witness['mul']
            zero = witness.get('zero')
            if zero is None:
                for e in elements:
                    if all(add(e, x) == x for x in elements):
                        zero = e
                        break
            return elements, add, mul, zero, list(witness['J']), list(witness['I'])

    if isinstance(witness, tuple):
        if len(witness) == 3:
            R, J, I = witness
            if isinstance(R, int):
                n = R
                elements = list(range(n))
                add = lambda x, y: (x + y) % n
                mul = lambda x, y: (x * y) % n
                zero = 0
                return elements, add, mul, zero, list(J), list(I)
            else:
                R_list = list(R)
                if all(isinstance(x, int) for x in R_list):
                    n = max(R_list) + 1 if R_list else 1
                    add = lambda x, y: (x + y) % n
                    mul = lambda x, y: (x * y) % n
                    zero = 0
                    return R_list, add, mul, zero, list(J), list(I)
        elif len(witness) == 5:
            elements, add, mul, J, I = witness
            elements = list(elements)
            zero = None
            for e in elements:
                if all(add(e, x) == x for x in elements):
                    zero = e
                    break
            return elements, add, mul, zero, list(J), list(I)

    raise ValueError("Unrecognized witness format")

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, zero, J, I = normalize(witness)
    except Exception:
        return [False, False, False]

    def check_H1():
        if not elements: return False
        if zero is None: return False
        
        for a in elements:
            for b in elements:
                if add(a, b) not in elements: return False
                if add(a, b) != add(b, a): return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
        
        for a in elements:
            if not any(add(a, b) == zero for b in elements): return False
            
        for a in elements:
            for b in elements:
                if mul(a, b) not in elements: return False
                if mul(a, b) != mul(b, a): return False
                for c in elements:
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    
        has_one = False
        for e in elements:
            if all(mul(e, x) == x and mul(x, e) == x for x in elements):
                has_one = True
                break
        if not has_one: return False
        
        return True

    def check_H2():
        if not J: return False
        if not all(x in elements for x in J): return False
        
        for a in J:
            for b in J:
                if add(a, b) not in J: return False
                
        for r in elements:
            for j in J:
                if mul(r, j) not in J: return False
                
        for a in J:
            has_inv = False
            for b in J:
                if add(a, b) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        return True

    def check_neg_Q():
        if not all(x in elements for x in I): return False
        
        I_colon_J = []
        for r in elements:
            if all(mul(r, j) in I for j in J):
                I_colon_J.append(r)

        S = set()
        for x in I_colon_J:
            for y in J:
                S.add(mul(x, y))

        closure = set(S)
        if not closure:
            closure.add(zero)
            
        while True:
            new_elements = set()
            for a in closure:
                for b in closure:
                    new_elements.add(add(a, b))
            if new_elements.issubset(closure):
                break
            closure.update(new_elements)

        return not closure.issubset(set(I))

    try:
        h1 = check_H1()
    except Exception:
        h1 = False

    try:
        h2 = check_H2()
    except Exception:
        h2 = False

    try:
        neg_q = check_neg_Q()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]