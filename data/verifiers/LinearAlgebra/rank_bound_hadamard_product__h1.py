import sympy as sp

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: B is an m \\times n matrix over the field F",
    "¬Q: The rank of the Hadamard product A \\circ B is greater than rank(A) \\times rank(B)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # Extract A and B from the witness
    try:
        if isinstance(witness, dict):
            A = witness['A']
            B = witness['B']
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                A, B = witness
            elif len(witness) == 3:
                _, A, B = witness
            elif len(witness) == 4:
                _, _, A, B = witness
            else:
                A, B = witness[-2], witness[-1]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: B is an m \times n matrix over the field F
    try:
        # Check if B can be interpreted as a matrix
        sp.Matrix(B)
        h1 = True
    except Exception:
        h1 = False

    # ¬Q: The rank of the Hadamard product A \circ B is greater than rank(A) * rank(B)
    try:
        # Compute rank of A
        if hasattr(A, 'rank') and callable(A.rank):
            rank_A = A.rank()
        else:
            rank_A = sp.Matrix(A).rank()

        # Compute rank of B
        if hasattr(B, 'rank') and callable(B.rank):
            rank_B = B.rank()
        else:
            rank_B = sp.Matrix(B).rank()

        # Compute the Hadamard product A \circ B
        if hasattr(A, 'multiply_elementwise') and callable(A.multiply_elementwise):
            A_circ_B = A.multiply_elementwise(B)
        elif hasattr(A, 'hadamard_product') and callable(A.hadamard_product):
            A_circ_B = A.hadamard_product(B)
        else:
            A_circ_B = sp.Matrix(A).multiply_elementwise(sp.Matrix(B))

        # Compute rank of A \circ B
        if hasattr(A_circ_B, 'rank') and callable(A_circ_B.rank):
            rank_AB = A_circ_B.rank()
        else:
            rank_AB = sp.Matrix(A_circ_B).rank()

        # Check if the conclusion fails (i.e., rank(A \circ B) > rank(A) * rank(B))
        neg_q = bool(rank_AB > rank_A * rank_B)
    except Exception:
        neg_q = False

    return [h1, neg_q]