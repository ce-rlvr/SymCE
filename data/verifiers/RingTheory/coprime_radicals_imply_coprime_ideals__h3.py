import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy.ntheory import factorint
import math

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, I, J = witness
        else:
            return [False, False, False, False]
            
        h1 = False
        if str(R) in ['Z', 'ZZ', 'Integers', 'S.Integers'] or R == sympy.S.Integers or R == sympy.ZZ:
            h1 = True
            
        h2 = False
        if h1 and (isinstance(I, int) or (hasattr(I, 'is_Integer') and I.is_Integer)):
            h2 = True
            I = int(I)
            
        h3 = False
        neg_q = False
        
        if h2:
            if isinstance(J, int) or (hasattr(J, 'is_Integer') and J.is_Integer):
                J = int(J)
                
                def rad(n):
                    if n == 0: return 0
                    if n == 1 or n == -1: return 1
                    res = 1
                    for p in factorint(abs(n)): res *= p
                    return res
                
                rI = rad(I)
                rJ = rad(J)
                
                if rI == 0 and rJ == 0:
                    h3 = False
                elif rI == 0:
                    h3 = (rJ == 1)
                elif rJ == 0:
                    h3 = (rI == 1)
                else:
                    h3 = (math.gcd(rI, rJ) == 1)
                    
                if I == 0 and J == 0:
                    neg_q = True
                elif I == 0:
                    neg_q = (abs(J) != 1)
                elif J == 0:
                    neg_q = (abs(I) != 1)
                else:
                    neg_q = (math.gcd(abs(I), abs(J)) != 1)
            else:
                try:
                    J_list = [int(x) for x in J]
                except Exception:
                    return [h1, h2, False, False]
                    
                if I == 0:
                    rI = 0
                else:
                    rI = 1
                    for p in factorint(abs(I)): rI *= p
                    
                if not J_list:
                    h3 = False
                    neg_q = True
                else:
                    sqrt_J = set()
                    for j in J_list:
                        if j == 0:
                            sqrt_J.add(0)
                        elif j == 1:
                            sqrt_J.update([1, -1])
                        elif j == -1:
                            sqrt_J.add(-1)
                        else:
                            for n in range(1, int(math.log2(abs(j))) + 2):
                                if n % 2 == 0 and j < 0:
                                    continue
                                x = int(round(abs(j) ** (1.0 / n)))
                                if x ** n == abs(j):
                                    if j > 0:
                                        sqrt_J.add(x)
                                        if n % 2 == 0:
                                            sqrt_J.add(-x)
                                    else:
                                        sqrt_J.add(-x)
                                        
                    if rI == 1:
                        h3 = True
                    elif rI == 0:
                        h3 = False
                    else:
                        residues = set(x % rI for x in sqrt_J)
                        h3 = (len(residues) == rI)
                        
                    if I == 1 or I == -1:
                        neg_q = False
                    elif I == 0:
                        neg_q = True
                    else:
                        residues_J = set(x % abs(I) for x in J_list)
                        neg_q = (len(residues_J) != abs(I))
                        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: \\sqrt{I} + \\sqrt{J} = R",
    "¬Q: I + J != R"
]

N_HYP = 3
NEG_Q_INDEX = 3