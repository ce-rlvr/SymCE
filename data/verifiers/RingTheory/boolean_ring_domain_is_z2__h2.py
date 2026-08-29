import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

Z1 = 1  # Trivial ring

def conditions(witness) -> list[bool]:
    try:
        # Parse the witness into a finite ring representation: (n, add_table, mul_table)
        if isinstance(witness, int) and not isinstance(witness, bool):
            n = witness
            if n == 0:
                n = 1
            add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
            mul_table = [[(i * j) % n for j in range(n)] for i in range(n)]
        elif hasattr(witness, 'is_zero') and witness.is_zero:
            n = 1
            add_table = [[0]]
            mul_table = [[0]]
        elif isinstance(witness, list) and all(isinstance(x, (set, frozenset)) for x in witness):
            elements = witness
            n = len(elements)
            if n > 100:
                return [False, False, False]
            add_table = [[0] * n for _ in range(n)]
            mul_table = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    add_res = elements[i] ^ elements[j]
                    mul_res = elements[i] & elements[j]
                    if add_res not in elements: return [False, False, False]
                    if mul_res not in elements: return [False, False, False]
                    add_table[i][j] = elements.index(add_res)
                    mul_table[i][j] = elements.index(mul_res)
        elif isinstance(witness, tuple) and len(witness) == 3:
            n, add_table, mul_table = witness
            n = int(n)
        elif hasattr(witness, 'order') and callable(witness.order):
            n = int(witness.order())
            add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
            mul_table = [[(i * j) % n for j in range(n)] for i in range(n)]
        else:
            return [False, False, False]
            
        if n < 1 or n > 100:
            return [False, False, False]
            
        # Check ring axioms
        for i in range(n):
            for j in range(n):
                if not (0 <= add_table[i][j] < n): return [False, False, False]
                if not (0 <= mul_table[i][j] < n): return [False, False, False]
                
        # Commutativity of addition
        for i in range(n):
            for j in range(n):
                if add_table[i][j] != add_table[j][i]: return [False, False, False]
                
        # Associativity of addition
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]:
                        return [False, False, False]
                        
        # Additive identity
        zero = None
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None: return [False, False, False]
        
        # Additive inverse
        for i in range(n):
            if not any(add_table[i][j] == zero for j in range(n)):
                return [False, False, False]
                
        # Associativity of multiplication
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]:
                        return [False, False, False]
                        
        # Distributivity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                        return [False, False, False]
                    if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]:
                        return [False, False, False]
                        
        # H1: Boolean ring (x^2 = x for all x)
        h1 = True
        for i in range(n):
            if mul_table[i][i] != i:
                h1 = False
                break
                
        # H2: Integral domain (commutative, no zero divisors)
        # Note: In the context of this false conjecture, the dropped hypothesis is "R is non-trivial" 
        # (or 1 != 0). Thus, the trivial ring {0} is considered an integral domain here.
        is_comm = True
        for i in range(n):
            for j in range(n):
                if mul_table[i][j] != mul_table[j][i]:
                    is_comm = False
                    break
            if not is_comm: break
            
        has_zero_div = False
        for i in range(n):
            if i == zero: continue
            for j in range(n):
                if j == zero: continue
                if mul_table[i][j] == zero:
                    has_zero_div = True
                    break
            if has_zero_div: break
            
        h2 = is_comm and not has_zero_div
        
        # neg_Q: R is NOT isomorphic to Z/2Z
        # Z/2Z has exactly 2 elements. Any Boolean ring of size 2 is isomorphic to Z/2Z.
        neg_q = (n != 2)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: R is an integral domain",
    "¬Q: R is not isomorphic to Z/2Z"
]

N_HYP = 2
NEG_Q_INDEX = 2