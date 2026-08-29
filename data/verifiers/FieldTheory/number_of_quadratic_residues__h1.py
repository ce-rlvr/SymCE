import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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

CONDITION_LABELS = [
    "H_1: The characteristic of F_q is an odd prime",
    "¬Q: The number of non-zero squares in F_q is not exactly (q-1)/2"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    # Approach 1: Tuple of tables (add_table, mul_table)
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (list, tuple)):
            add_table, mul_table = witness
            q = len(add_table)
            
            zero = None
            for i in range(q):
                if all(add_table[i][j] == j for j in range(q)):
                    zero = i
                    break
                    
            one = None
            for i in range(q):
                if all(mul_table[i][j] == j for j in range(q)):
                    one = i
                    break
                    
            char = 0
            if zero is not None and one is not None:
                current = zero
                for i in range(1, q+1):
                    current = add_table[current][one]
                    if current == zero:
                        char = i
                        break
                        
            h1 = sympy.isprime(char) and char % 2 != 0
            
            if zero is not None:
                squares = set()
                for i in range(q):
                    sq = mul_table[i][i]
                    if sq != zero:
                        squares.add(sq)
                conclusion = (len(squares) == (q - 1) / 2)
                neg_q = not conclusion
                return [bool(h1), bool(neg_q)]
    except Exception:
        pass

    # Approach 2: Object with characteristic and iterable elements
    try:
        if hasattr(witness, 'characteristic'):
            char_attr = witness.characteristic
            if callable(char_attr):
                char = char_attr()
            else:
                char = char_attr
        elif hasattr(witness, 'char'):
            char_attr = witness.char
            if callable(char_attr):
                char = char_attr()
            else:
                char = char_attr
        else:
            char = None
            
        if hasattr(witness, 'elements'):
            elements = list(witness.elements)
        else:
            elements = list(witness)
            
        q = len(elements)
        
        if hasattr(witness, 'zero'):
            zero = witness.zero
        else:
            zero = None
            try:
                for e in elements:
                    is_z = True
                    for x in elements:
                        if e + x != x:
                            is_z = False
                            break
                    if is_z:
                        zero = e
                        break
            except Exception:
                pass
            if zero is None:
                zero = elements[0] - elements[0]
                
        if char is None:
            one = None
            try:
                for e in elements:
                    is_id = True
                    for x in elements:
                        if e * x != x or x * e != x:
                            is_id = False
                            break
                    if is_id:
                        one = e
                        break
            except Exception:
                pass
            if one is not None and zero is not None:
                current = zero
                for i in range(1, q+1):
                    current = current + one
                    if current == zero:
                        char = i
                        break
                        
        if char is not None:
            h1 = sympy.isprime(char) and char % 2 != 0
        else:
            h1 = False
            
        squares = []
        for x in elements:
            sq = x * x
            is_zero = (sq == zero)
            if not is_zero:
                found = False
                for s in squares:
                    if s == sq:
                        found = True
                        break
                if not found:
                    squares.append(sq)
                    
        conclusion = (len(squares) == (q - 1) / 2)
        neg_q = not conclusion
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        pass

    return [bool(h1), bool(neg_q)]