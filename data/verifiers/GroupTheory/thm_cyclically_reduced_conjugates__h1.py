import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        u, v, mapping, g_val = witness
        
        def get_letters(w):
            if isinstance(w, list):
                return w
            if isinstance(w, str):
                letters = []
                for char in w:
                    if char.islower():
                        letters.append((char.lower(), 1))
                    else:
                        letters.append((char.lower(), -1))
                return letters
            if hasattr(w, 'array_form'):
                letters = []
                for gen, exp in w.array_form:
                    for _ in range(abs(exp)):
                        letters.append((gen, 1 if exp > 0 else -1))
                return letters
            raise ValueError("Unsupported word format")

        def is_reduced(letters):
            for i in range(len(letters) - 1):
                l1 = letters[i]
                l2 = letters[i+1]
                if isinstance(l1, int):
                    if l1 == -l2: return False
                else:
                    if l1[0] == l2[0] and l1[1] == -l2[1]: return False
            return True

        def is_cyclically_reduced(letters):
            if not is_reduced(letters):
                return False
            if len(letters) > 0:
                l1 = letters[0]
                l2 = letters[-1]
                if isinstance(l1, int):
                    if l1 == -l2: return False
                else:
                    if l1[0] == l2[0] and l1[1] == -l2[1]: return False
            return True
            
        u_letters = get_letters(u)
        v_letters = get_letters(v)
        
        h1 = is_cyclically_reduced(u_letters) and is_cyclically_reduced(v_letters)
        
        identity = g_val * g_val**-1
        
        def evaluate(w):
            res = identity
            if isinstance(w, list):
                for letter in w:
                    if letter > 0:
                        val = mapping[letter]
                    else:
                        val = mapping[-letter]**-1
                    res = res * val
            elif isinstance(w, str):
                for char in w:
                    if char.islower():
                        val = mapping[char.lower()]
                    else:
                        val = mapping[char.lower()]**-1
                    res = res * val
            elif hasattr(w, 'array_form'):
                for gen, exp in w.array_form:
                    val = mapping[gen]
                    if exp > 0:
                        res = res * (val**exp)
                    else:
                        res = res * ((val**-1)**(-exp))
            return res
            
        u_val = evaluate(u)
        v_val = evaluate(v)
        
        h2 = (g_val * u_val * g_val**-1 == v_val)
        
        def is_cyclic_permutation(u_let, v_let):
            if len(u_let) != len(v_let):
                return False
            if len(u_let) == 0:
                return True
            for i in range(len(u_let)):
                if u_let[i:] + u_let[:i] == v_let:
                    return True
            return False
            
        neg_q = not is_cyclic_permutation(u_letters, v_letters)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: u and v are cyclically reduced words with respect to the basis X",
    "H_2: u and v are conjugate elements in F",
    "¬Q: The word u is not a cyclic permutation of the word v"
]

N_HYP = 2
NEG_Q_INDEX = 2