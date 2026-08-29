import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Check witness structure: should be a tuple of two matrices (A, B)
    try:
        if not (isinstance(witness, tuple) and len(witness) == 2):
            return [False, False, False]
        A, B = witness
    except Exception:
        return [False, False, False]

    # H_1: A and B are square matrices
    try:
        h1 = hasattr(A, 'is_square') and A.is_square and hasattr(B, 'is_square') and B.is_square
    except Exception:
        h1 = False

    # H_2: A and B are both in Jordan canonical form
    try:
        def is_jcf(M):
            n = M.shape[0]
            for r in range(n):
                for c in range(n):
                    if r == c:
                        continue
                    elif c == r + 1:
                        val = M[r, c]
                        if val != 0 and val != 1:
                            return False
                        if val == 1 and M[r, r] != M[c, c]:
                            return False
                    else:
                        if M[r, c] != 0:
                            return False
            return True
            
        h2 = is_jcf(A) and is_jcf(B)
    except Exception:
        h2 = False

    # ¬Q: A and B are NOT identical up to a permutation of their Jordan blocks
    try:
        def get_blocks(M):
            n = M.shape[0]
            if n == 0:
                return []
            blocks = []
            i = 0
            while i < n:
                val = M[i, i]
                size = 1
                while i + size < n and M[i + size - 1, i + size] == 1:
                    size += 1
                blocks.append((val, size))
                i += size
            return blocks
        
        def multiset_eq(list1, list2):
            if len(list1) != len(list2):
                return False
            l2 = list(list2)
            for x in list1:
                found = False
                for i, y in enumerate(l2):
                    if x == y:
                        l2.pop(i)
                        found = True
                        break
                if not found:
                    return False
            return True

        blocks_A = get_blocks(A)
        blocks_B = get_blocks(B)
        neg_q = not multiset_eq(blocks_A, blocks_B)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A and B are square matrices",
    "H_2: A and B are both in Jordan canonical form",
    "¬Q: A and B are not identical up to a permutation of their Jordan blocks"
]

N_HYP = 2
NEG_Q_INDEX = 2