import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        # The witness is expected to be a finite magma represented by its Cayley table (list of lists)
        if not isinstance(witness, (list, tuple)):
            return [False]
        if not all(isinstance(row, (list, tuple)) for row in witness):
            return [False]
            
        n = len(witness)
        if n == 0:
            return [False]
            
        for row in witness:
            if len(row) != n:
                return [False]
            for x in row:
                if not (isinstance(x, int) and 0 <= x < n):
                    return [False]
                    
        # Condition 1: The map L_g(x) = g * x must be a permutation of G for all g.
        # This means every row in the Cayley table must be a permutation of 0..n-1.
        maps_to_sym = True
        for row in witness:
            if set(row) != set(range(n)):
                maps_to_sym = False
                break
                
        # Condition 2: The map L must be a group homomorphism from G to Sym(G).
        # L_{g*h} = L_g \circ L_h  <=>  (g * h) * x = g * (h * x) for all g, h, x.
        is_homo = True
        if maps_to_sym:
            for g in range(n):
                for h in range(n):
                    gh = witness[g][h]
                    for x in range(n):
                        if witness[gh][x] != witness[g][witness[h][x]]:
                            is_homo = False
                            break
                    if not is_homo:
                        break
                if not is_homo:
                    break
                    
        # Condition 3: The map L must be injective.
        # L_g = L_h implies g = h. This means all rows in the Cayley table must be distinct.
        is_inj = True
        if maps_to_sym and is_homo:
            seen_rows = set()
            for row in witness:
                row_tuple = tuple(row)
                if row_tuple in seen_rows:
                    is_inj = False
                    break
                seen_rows.add(row_tuple)
                
        conclusion_holds = maps_to_sym and is_homo and is_inj
        neg_q = not conclusion_holds
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The map from G to Sym(G) defined by left multiplication is not an injective group homomorphism"
]

N_HYP = 0
NEG_Q_INDEX = 0