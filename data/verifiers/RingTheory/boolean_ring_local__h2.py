import itertools
import math

class Z2Ring:
    elements = [0, 1]
    zero = 0
    one = 1
    @staticmethod
    def add(x, y): return (x + y) % 2
    @staticmethod
    def mul(x, y): return (x * y) % 2

class Z2xZ2Ring:
    elements = [(0,0), (0,1), (1,0), (1,1)]
    zero = (0,0)
    one = (1,1)
    @staticmethod
    def add(x, y): return ((x[0]+y[0])%2, (x[1]+y[1])%2)
    @staticmethod
    def mul(x, y): return ((x[0]*y[0])%2, (x[1]*y[1])%2)

class Z2xZ2xZ2Ring:
    elements = [(i,j,k) for i in (0,1) for j in (0,1) for k in (0,1)]
    zero = (0,0,0)
    one = (1,1,1)
    @staticmethod
    def add(x, y): return ((x[0]+y[0])%2, (x[1]+y[1])%2, (x[2]+y[2])%2)
    @staticmethod
    def mul(x, y): return ((x[0]*y[0])%2, (x[1]*y[1])%2, (x[2]*y[2])%2)

Z2 = Z2Ring()
Z2_times_Z2 = Z2xZ2Ring()
Z2_times_Z2_times_Z2 = Z2xZ2xZ2Ring()

def conditions(witness):
    # H_1: R is a Boolean ring with a multiplicative identity
    try:
        unique_elements = []
        for e in witness.elements:
            if e not in unique_elements:
                unique_elements.append(e)
        elements = unique_elements
        zero = witness.zero
        one = witness.one
        add = witness.add
        mul = witness.mul
        
        h1_ok = True
        if zero not in elements or one not in elements:
            h1_ok = False
        else:
            for x in elements:
                if not h1_ok: break
                
                if add(x, zero) != x or add(zero, x) != x:
                    h1_ok = False; break
                if mul(x, one) != x or mul(one, x) != x:
                    h1_ok = False; break
                if mul(x, x) != x:
                    h1_ok = False; break
                
                has_inv = False
                for y in elements:
                    if add(x, y) == zero and add(y, x) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    h1_ok = False; break
                
                for y in elements:
                    if not h1_ok: break
                    if add(x, y) not in elements:
                        h1_ok = False; break
                    if mul(x, y) not in elements:
                        h1_ok = False; break
                    if add(x, y) != add(y, x):
                        h1_ok = False; break
                    
                    for z in elements:
                        if add(add(x, y), z) != add(x, add(y, z)):
                            h1_ok = False; break
                        if mul(mul(x, y), z) != mul(x, mul(y, z)):
                            h1_ok = False; break
                        if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)):
                            h1_ok = False; break
                        if mul(add(x, y), z) != add(mul(x, z), mul(y, z)):
                            h1_ok = False; break
    except Exception:
        h1_ok = False

    # neg_Q: R is not isomorphic to Z2
    try:
        unique_elements = []
        for e in witness.elements:
            if e not in unique_elements:
                unique_elements.append(e)
        elements = unique_elements
        
        if len(elements) != 2:
            neg_q_ok = True
        else:
            add = witness.add
            mul = witness.mul
            
            is_isomorphic = False
            for z, o in [(elements[0], elements[1]), (elements[1], elements[0])]:
                is_z2 = True
                if add(z, z) != z: is_z2 = False
                if add(z, o) != o: is_z2 = False
                if add(o, z) != o: is_z2 = False
                if add(o, o) != z: is_z2 = False
                
                if mul(z, z) != z: is_z2 = False
                if mul(z, o) != z: is_z2 = False
                if mul(o, z) != z: is_z2 = False
                if mul(o, o) != o: is_z2 = False
                
                if is_z2:
                    is_isomorphic = True
                    break
            
            neg_q_ok = not is_isomorphic
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring with a multiplicative identity",
    "¬Q: R is not isomorphic to Z2"
]

N_HYP = 1
NEG_Q_INDEX = 1