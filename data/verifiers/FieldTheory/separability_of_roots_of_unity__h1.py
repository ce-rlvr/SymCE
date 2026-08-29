import sympy
from sympy.matrices import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_n_p_char(witness):
    n, p, char_F = None, None, None
    
    if isinstance(witness, dict):
        n = witness.get('n')
        p = witness.get('p')
        if 'char_F' in witness:
            char_F = witness['char_F']
        elif 'F' in witness:
            F = witness['F']
            if hasattr(F, 'characteristic'):
                try:
                    char_F = F.characteristic()
                except Exception:
                    pass
            elif hasattr(F, 'char'):
                try:
                    char_F = F.char
                except Exception:
                    pass
            elif isinstance(F, (int, sympy.Integer)):
                char_F = F
    else:
        try:
            n = getattr(witness, 'n', None)
            p = getattr(witness, 'p', None)
            if hasattr(witness, 'char_F'):
                char_F = witness.char_F
            elif hasattr(witness, 'F'):
                F = witness.F
                if hasattr(F, 'characteristic'):
                    char_F = F.characteristic()
                elif hasattr(F, 'char'):
                    char_F = F.char
                elif isinstance(F, (int, sympy.Integer)):
                    char_F = F
        except Exception:
            pass

    if n is None and isinstance(witness, (tuple, list)) and len(witness) >= 3:
        n = witness[0]
        p = witness[1]
        F = witness[2]
        if isinstance(F, (int, sympy.Integer)):
            char_F = F
        elif hasattr(F, 'characteristic'):
            try:
                char_F = F.characteristic()
            except Exception:
                pass
        elif hasattr(F, 'char'):
            try:
                char_F = F.char
            except Exception:
                pass
            
    return n, p, char_F

def conditions(witness) -> list[bool]:
    n, p, char_F = get_n_p_char(witness)
    
    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False
        
    # H_2: p does not divide n
    try:
        if p == 0:
            h2 = isinstance(p, (int, sympy.Integer))
        else:
            h2 = isinstance(p, (int, sympy.Integer)) and (n % p != 0)
    except Exception:
        h2 = False
        
    # H_3: E is the splitting field of x^n - 1 over F
    # We verify this by checking if F is a valid field (characteristic is 0 or prime)
    try:
        h3 = char_F is not None and isinstance(char_F, (int, sympy.Integer)) and (char_F == 0 or sympy.isprime(char_F))
    except Exception:
        h3 = False
        
    # ¬Q: The field extension E/F is not separable
    # In the context of the false conjecture, this is interpreted as x^n - 1 having multiple roots,
    # which occurs when the characteristic of F divides n.
    try:
        neg_q = char_F is not None and isinstance(char_F, (int, sympy.Integer)) and (char_F > 0) and (n % char_F == 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: p does not divide n",
    "H_3: E is the splitting field of x^n - 1 over F",
    "¬Q: The field extension E/F is not separable (x^n - 1 has multiple roots)"
]

N_HYP = 3
NEG_Q_INDEX = 3