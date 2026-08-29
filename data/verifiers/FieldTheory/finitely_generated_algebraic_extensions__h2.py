import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
import itertools

# Top-level setup
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            try:
                iter(witness[1])
                witness = witness[1]
            except TypeError:
                pass

        is_infinite_collection = False
        
        if isinstance(witness, sympy.Set):
            if witness.is_finite == False:
                is_infinite_collection = True
            elif witness.is_finite == True:
                is_infinite_collection = False
            else:
                is_infinite_collection = True
            iterator = iter(witness)
        elif hasattr(witness, '__len__'):
            is_infinite_collection = False
            iterator = iter(witness)
        else:
            iterator = iter(witness)
            is_infinite_collection = True 
            
        elements = []
        for _ in range(10):
            try:
                elements.append(sympy.sympify(next(iterator)))
            except StopIteration:
                is_infinite_collection = False
                break
                
        if len(elements) > 0:
            h1 = True
            
            h2 = True
            for e in elements:
                if not e.is_algebraic:
                    try:
                        sympy.minpoly(e)
                    except Exception:
                        h2 = False
                        break
                        
            if is_infinite_collection:
                more_elements = list(elements)
                try:
                    for _ in range(40):
                        more_elements.append(sympy.sympify(next(iterator)))
                except StopIteration:
                    is_infinite_collection = False
                    
            if is_infinite_collection:
                try:
                    minpolys = set()
                    for e in more_elements:
                        try:
                            mp = sympy.minpoly(e)
                            minpolys.add(mp)
                        except Exception:
                            pass
                    if len(minpolys) >= 4:
                        neg_q = True
                except Exception:
                    pass
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a field extension",
    "H_2: Each element \\alpha_i is algebraic over K",
    "¬Q: The field extension L/K is not finite"
]

N_HYP = 2
NEG_Q_INDEX = 2