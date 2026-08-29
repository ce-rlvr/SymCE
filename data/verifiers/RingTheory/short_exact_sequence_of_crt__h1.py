import sympy
import sympy.combinatorics
import sympy.matrices

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R_list = list(witness.get('R', []))
            I_list = list(witness.get('I', []))
            J_list = list(witness.get('J', []))
            add = witness.get('add', lambda x, y: x + y)
            sub = witness.get('sub', lambda x, y: x - y)
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                R, I, J = witness
                add = lambda x, y: x + y
                sub = lambda x, y: x - y
            elif len(witness) == 5:
                R, I, J, add, sub = witness
            else:
                return [False, False]
                
            def get_elements(obj):
                if hasattr(obj, 'elements'):
                    return list(obj.elements()) if callable(obj.elements) else list(obj.elements)
                return list(obj)
                
            try:
                R_list = get_elements(R)
                I_list = get_elements(I)
                J_list = get_elements(J)
            except TypeError:
                # If the ring is infinite or not iterable, we assume the standard algebraic 
                # properties hold (the sequence is always exact for standard rings).
                return [True, False]
        else:
            return [False, False]
            
        # Check H1: I and J are ideals (we check closure under addition and subtraction)
        h1 = True
        if R_list:
            if not I_list or not J_list:
                h1 = False
            else:
                for x in I_list:
                    for y in I_list:
                        if add(x, y) not in I_list: h1 = False
                        if sub(x, y) not in I_list: h1 = False
                for x in J_list:
                    for y in J_list:
                        if add(x, y) not in J_list: h1 = False
                        if sub(x, y) not in J_list: h1 = False
                        
        # Check neg_Q: The sequence is NOT exact
        # We verify if Im f == ker g. 
        # ker g = { (a, b) | a - b \in I + J }
        # Im f = { (r mod I, r mod J) | r \in R }
        I_plus_J = []
        for i in I_list:
            for j in J_list:
                I_plus_J.append(add(i, j))
                
        exact = True
        for a in R_list:
            for b in R_list:
                if sub(a, b) in I_plus_J:
                    found = False
                    for r in R_list:
                        if sub(r, a) in I_list and sub(r, b) in J_list:
                            found = True
                            break
                    if not found:
                        exact = False
                        break
            if not exact:
                break
                
        neg_Q = not exact
        return [h1, neg_Q]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: Let I and J be ideals of R",
    "¬Q: The sequence is not a short exact sequence of R-modules"
]

N_HYP = 1
NEG_Q_INDEX = 1