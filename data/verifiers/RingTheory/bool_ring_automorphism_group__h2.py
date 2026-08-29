import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Standard algebra objects
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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a finite Boolean ring R, and whether its 
    automorphism group is NOT isomorphic to the symmetric group S_n.
    
    The witness can be:
      - A tuple (elements, add_table, mul_table, n)
      - A tuple (elements, add_table, mul_table) where n defaults to len(elements)
      - An object with `elements`, `add`, `mul` methods, and optionally `n`.
    """
    try:
        if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
            elements = witness.elements
            size = len(elements)
            add_table = [[0]*size for _ in range(size)]
            mul_table = [[0]*size for _ in range(size)]
            
            elem_to_idx = {}
            for i, e in enumerate(elements):
                try:
                    elem_to_idx[e] = i
                except TypeError:
                    pass
                    
            for i, a in enumerate(elements):
                for j, b in enumerate(elements):
                    sum_val = witness.add(a, b)
                    prod_val = witness.mul(a, b)
                    if sum_val in elem_to_idx:
                        add_table[i][j] = elem_to_idx[sum_val]
                    else:
                        add_table[i][j] = elements.index(sum_val)
                    if prod_val in elem_to_idx:
                        mul_table[i][j] = elem_to_idx[prod_val]
                    else:
                        mul_table[i][j] = elements.index(prod_val)
            n = getattr(witness, 'n', size)
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                elements, add_table, mul_table, n = witness
            elif len(witness) == 3:
                elements, add_table, mul_table = witness
                n = len(elements)
            else:
                return [False, False]
        else:
            return [False, False]
            
        size = len(elements)
        if size == 0:
            return [False, False]
            
        if not isinstance(n, int):
            n = int(n)
            
        # Check tables dimensions and bounds
        if len(add_table) != size or len(mul_table) != size:
            return [False, False]
            
        is_ring = True
        
        for row in add_table:
            if len(row) != size or any(not (isinstance(val, int) and 0 <= val < size) for val in row):
                is_ring = False
        for row in mul_table:
            if len(row) != size or any(not (isinstance(val, int) and 0 <= val < size) for val in row):
                is_ring = False
                
        if not is_ring:
            return [False, False]
            
        # Commutativity of addition
        for i in range(size):
            for j in range(size):
                if add_table[i][j] != add_table[j][i]:
                    is_ring = False
                    
        # Associativity of addition
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]:
                        is_ring = False
                        
        # Identity of addition
        id_add = -1
        for i in range(size):
            if all(add_table[i][j] == j for j in range(size)):
                id_add = i
                break
        if id_add == -1:
            is_ring = False
            
        # Inverse of addition
        if is_ring:
            for i in range(size):
                if not any(add_table[i][j] == id_add for j in range(size)):
                    is_ring = False
                    
        # Associativity of multiplication
        if is_ring:
            for i in range(size):
                for j in range(size):
                    for k in range(size):
                        if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]:
                            is_ring = False
                            
        # Distributivity
        if is_ring:
            for i in range(size):
                for j in range(size):
                    for k in range(size):
                        if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                            is_ring = False
                        if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]:
                            is_ring = False
                            
        # Boolean property (x^2 = x)
        if is_ring:
            for i in range(size):
                if mul_table[i][i] != i:
                    is_ring = False
                    
        h1 = is_ring
        
        if not is_ring:
            neg_q = False
        else:
            # Count the number of atoms in the Boolean ring
            # An element x is an atom if x != 0 and for all y, x*y = x or x*y = 0
            atoms = 0
            for i in range(size):
                if i == id_add: 
                    continue
                is_atom = True
                for j in range(size):
                    prod = mul_table[i][j]
                    if prod != i and prod != id_add:
                        is_atom = False
                        break
                if is_atom:
                    atoms += 1
            
            # The automorphism group of a finite Boolean ring is isomorphic to S_k 
            # where k is the number of atoms. We check if S_k is isomorphic to S_n.
            # Two symmetric groups are isomorphic iff their orders are equal.
            if n < 0:
                isomorphic = False
            else:
                order_aut = math.factorial(atoms)
                order_sn = math.factorial(n)
                isomorphic = (order_aut == order_sn)
                
            neg_q = not isomorphic
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a finite Boolean ring",
    "¬Q: The automorphism group of R is not isomorphic to the symmetric group S_n"
]

N_HYP = 1
NEG_Q_INDEX = 1