import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

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

CONDITION_LABELS = [
    "H_1: x is an element of the alternating group A_n",
    "H_2: K is the conjugacy class of x in the symmetric group S_n",
    "¬Q: K splits into exactly two distinct conjugacy classes in A_n is NOT equivalent to the centralizer of x in S_n being contained in A_n"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                n, x = witness
                K_given = None
            elif len(witness) == 3:
                n, x, K_given = witness
            else:
                return [False, False, False]
        elif isinstance(witness, Permutation):
            x = witness
            n = x.size
            if n == 0:
                n = 1
            K_given = None
        else:
            return [False, False, False]
            
        if not isinstance(n, (int, sympy.Integer)):
            return [False, False, False]
        n = int(n)
        if n < 1:
            return [False, False, False]
            
        if not isinstance(x, Permutation):
            return [False, False, False]
            
        # Check if x is valid for n (does not move elements >= n)
        for i in range(n, x.size):
            if x(i) != i:
                return [False, False, False]
                
        # Standardize x to size n
        x_list = [x(i) for i in range(n)]
        x_std = Permutation(x_list)
        
        # H_1: x is in A_n
        h1 = x_std.is_even
        
        # Prevent timeout for large n (counterexample exists for n=1)
        if n > 6:
            return [False, False, False]
            
        # Generate S_n and A_n elements manually to avoid sympy version issues with small n
        Sn_elements = [Permutation(list(p)) for p in itertools.permutations(range(n))]
        An_elements = [p for p in Sn_elements if p.is_even]
        
        # Compute actual conjugacy class of x in S_n
        K_actual = set()
        for g in Sn_elements:
            K_actual.add(g * x_std * ~g)
            
        # H_2: K is the conjugacy class of x in S_n
        h2 = False
        if K_given is not None:
            if isinstance(K_given, (set, list, tuple)):
                K_given_std = set()
                for y in K_given:
                    if not isinstance(y, Permutation):
                        break
                    valid_y = True
                    for i in range(n, y.size):
                        if y(i) != i:
                            valid_y = False
                            break
                    if not valid_y:
                        break
                    y_list = [y(i) for i in range(n)]
                    K_given_std.add(Permutation(y_list))
                else:
                    h2 = (K_given_std == K_actual)
        else:
            # If K is not explicitly provided, we assume the implicit K_actual is used
            h2 = True
            
        # Check if K splits into exactly two distinct conjugacy classes in A_n
        An_classes = set()
        for y in K_actual:
            cls = frozenset(a * y * ~a for a in An_elements)
            An_classes.add(cls)
            
        splits_into_two = (len(An_classes) == 2)
        
        # Check if the centralizer of x in S_n is contained in A_n
        C_Sn = set()
        for g in Sn_elements:
            if g * x_std == x_std * g:
                C_Sn.add(g)
                
        An_set = set(An_elements)
        contained_in_An = C_Sn.issubset(An_set)
        
        # ¬Q: The equivalence fails
        neg_q = (splits_into_two != contained_in_An)
        
        return [bool(h1), bool(h2), bool(neg_q)]
        
    except Exception:
        return [False, False, False]