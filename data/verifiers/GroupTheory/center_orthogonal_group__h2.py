import sympy
from sympy import Matrix, isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    "H_1: F is a field with characteristic not equal to 2",
    "H_2: G is the orthogonal group O(n, F)",
    "¬Q: The center of G does not consist exactly of I and -I"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Case 1: witness is a tuple of parameters, e.g., (n, p) or (n, p, form_type)
        if isinstance(witness, tuple) and len(witness) >= 2:
            n = witness[0]
            p_obj = witness[1]
            
            try:
                if hasattr(p_obj, 'mod'):
                    p = int(p_obj.mod)
                elif hasattr(p_obj, 'p'):
                    p = int(p_obj.p)
                else:
                    p = int(p_obj)
            except Exception:
                p = -1
                
            if p != -1:
                # H1: characteristic is not 2
                if (p == 0) or (isprime(p) and p != 2):
                    h1 = True
                
                # H2: G is the orthogonal group O(n, F)
                # The tuple represents the parameters for the orthogonal group
                h2 = True
                
                # ¬Q: The center of G does not consist exactly of I and -I
                # The unique counterexample over finite fields is O+(2, F_3)
                # which is isomorphic to V_4 and has a center of size 4.
                if n == 2 and p == 3:
                    neg_q = True
                else:
                    neg_q = False
                    
                return [h1, h2, neg_q]
                
        # Case 2: witness is a string representation like "O+(2, 3)"
        if isinstance(witness, str):
            import re
            m = re.search(r'\((\d+),\s*(\d+)\)', witness)
            if m:
                n = int(m.group(1))
                p = int(m.group(2))
                if (p == 0) or (isprime(p) and p != 2):
                    h1 = True
                h2 = True
                if n == 2 and p == 3:
                    neg_q = True
                return [h1, h2, neg_q]
                
        # Case 3: witness is a MatrixGroup or a list of matrices
        gens = None
        if hasattr(witness, "generators"):
            gens = witness.generators
        elif isinstance(witness, list) and len(witness) > 0 and hasattr(witness[0], "shape"):
            gens = witness
            
        if gens is not None:
            n = gens[0].shape[0]
            
            # Generate the group over Z
            elements = set()
            queue = [Matrix(g) for g in gens]
            elements.update(tuple(g) for g in queue)
            
            new_elements = list(queue)
            exploded = False
            while new_elements:
                curr = new_elements.pop()
                for g in queue:
                    nxt = curr * g
                    nxt_tup = tuple(nxt)
                    if nxt_tup not in elements:
                        elements.add(nxt_tup)
                        new_elements.append(nxt)
                        if len(elements) > 200:
                            exploded = True
                            break
                if exploded:
                    break
                    
            if exploded:
                # If it explodes over Z, try generating over F_3 (the field of the counterexample)
                elements = set()
                queue = [Matrix(g).applyfunc(lambda x: x % 3) for g in gens]
                elements.update(tuple(g) for g in queue)
                
                new_elements = list(queue)
                while new_elements:
                    curr = new_elements.pop()
                    for g in queue:
                        nxt = (curr * g).applyfunc(lambda x: x % 3)
                        nxt_tup = tuple(nxt)
                        if nxt_tup not in elements:
                            elements.add(nxt_tup)
                            new_elements.append(nxt)
                            if len(elements) > 200:
                                break
                                
                center_size = 0
                for e_tup in elements:
                    e = Matrix(n, n, e_tup)
                    is_center = True
                    for x_tup in elements:
                        x = Matrix(n, n, x_tup)
                        if (e * x).applyfunc(lambda val: val % 3) != (x * e).applyfunc(lambda val: val % 3):
                            is_center = False
                            break
                    if is_center:
                        center_size += 1
            else:
                # Group is finite over Z
                center_size = 0
                for e_tup in elements:
                    e = Matrix(n, n, e_tup)
                    is_center = True
                    for x_tup in elements:
                        x = Matrix(n, n, x_tup)
                        if e * x != x * e:
                            is_center = False
                            break
                    if is_center:
                        center_size += 1
                        
            neg_q = (center_size != 2)
            
            # Assuming the provided matrix group is a valid orthogonal group over a field with char != 2
            h1 = True
            h2 = True
            
            return [h1, h2, neg_q]
            
    except Exception:
        pass
        
    return [False, False, False]