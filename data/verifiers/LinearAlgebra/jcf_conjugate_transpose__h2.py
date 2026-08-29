import sympy
from sympy import Matrix

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_jordan_blocks(J):
    """
    Extracts the multiset of Jordan blocks from a Jordan canonical form matrix J.
    Returns a list of tuples: (eigenvalue, block_size).
    """
    blocks = []
    n = J.shape[0]
    i = 0
    while i < n:
        val = J[i, i]
        size = 1
        # Check for 1s on the superdiagonal (SymPy's default convention)
        if i + 1 < n and J[i, i + 1] == 1:
            while i + size < n and J[i + size - 1, i + size] == 1 and J[i + size, i + size] == val:
                size += 1
        # Check for 1s on the subdiagonal (alternative convention)
        elif i + 1 < n and J[i + 1, i] == 1:
            while i + size < n and J[i + size, i + size - 1] == 1 and J[i + size, i + size] == val:
                size += 1
        blocks.append((val, size))
        i += size
    return blocks

def compare_multisets(blocks1, blocks2):
    """
    Compares two multisets of Jordan blocks for equality.
    """
    if len(blocks1) != len(blocks2):
        return False
    b2_list = list(blocks2)
    for b1 in blocks1:
        val1, size1 = b1
        matched = False
        for i, b2 in enumerate(b2_list):
            val2, size2 = b2
            if size1 == size2:
                diff = (val1 - val2).simplify()
                if diff == 0 or diff.is_zero:
                    matched = True
                else:
                    diff_exp = diff.expand(complex=True).simplify()
                    if diff_exp == 0 or diff_exp.is_zero:
                        matched = True
                if matched:
                    b2_list.pop(i)
                    break
        if not matched:
            return False
    return True

def conditions(witness) -> list[bool]:
    # H_1: Let A be an n \times n complex matrix.
    try:
        if not isinstance(witness, Matrix):
            return [False, False]
        if witness.shape[0] != witness.shape[1]:
            return [False, False]
        h1 = True
    except Exception:
        return [False, False]
        
    # neg_Q: The Jordan canonical form of A* is NOT obtained by replacing each 
    # Jordan block J_k(\lambda) in J with the Jordan block J_k(\bar{\lambda}).
    try:
        # Compute JCF of A and extract blocks
        _, J_A = witness.jordan_form()
        blocks_A = get_jordan_blocks(J_A)
        
        # Compute JCF of the conjugate transpose A* and extract blocks
        A_star = witness.H
        _, J_A_star = A_star.jordan_form()
        blocks_A_star = get_jordan_blocks(J_A_star)
        
        # Construct the expected blocks by conjugating the eigenvalues
        expected_blocks = []
        for val, size in blocks_A:
            try:
                c_val = val.conjugate()
            except AttributeError:
                c_val = sympy.conjugate(val)
            expected_blocks.append((c_val, size))
        
        # The conclusion fails if the actual blocks of A* do not match the expected blocks
        neg_q = not compare_multisets(blocks_A_star, expected_blocks)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "¬Q: The Jordan canonical form of A* is NOT obtained by replacing each Jordan block J_k(lambda) with J_k(bar(lambda))"
]

N_HYP = 1
NEG_Q_INDEX = 1