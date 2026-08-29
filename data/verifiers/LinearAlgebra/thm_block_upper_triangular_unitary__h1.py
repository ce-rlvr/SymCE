import sympy
from sympy import Matrix, eye, simplify

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def _extract_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        U, blocks = witness
    else:
        U = witness
        blocks = None

    if isinstance(U, list):
        try:
            U = Matrix(U)
        except Exception:
            return None, None

    if not hasattr(U, 'shape') or U.shape[0] != U.shape[1]:
        return None, None

    n = U.shape[0]
    if blocks is None:
        if getattr(U, 'is_upper', False):
            blocks = [1] * n
        else:
            blocks = [n]

    return U, blocks

def conditions(witness) -> list[bool]:
    try:
        U, blocks = _extract_witness(witness)
        if U is None:
            h1 = False
        elif sum(blocks) != U.shape[0] or any(b <= 0 for b in blocks):
            h1 = False
        else:
            is_block_upper = True
            row_idx = 0
            for i, r in enumerate(blocks):
                col_idx = 0
                for j, c in enumerate(blocks):
                    if i > j:
                        block = U[row_idx:row_idx+r, col_idx:col_idx+c]
                        if not all(val == 0 or simplify(val) == 0 for val in block):
                            is_block_upper = False
                            break
                    col_idx += c
                row_idx += r
                if not is_block_upper:
                    break
            h1 = is_block_upper
    except Exception:
        h1 = False

    try:
        U, blocks = _extract_witness(witness)
        if U is None:
            neg_q = False
        elif sum(blocks) != U.shape[0] or any(b <= 0 for b in blocks):
            neg_q = False
        else:
            is_block_diag = True
            row_idx = 0
            for i, r in enumerate(blocks):
                col_idx = 0
                for j, c in enumerate(blocks):
                    if i != j:
                        block = U[row_idx:row_idx+r, col_idx:col_idx+c]
                        if not all(val == 0 or simplify(val) == 0 for val in block):
                            is_block_diag = False
                            break
                    col_idx += c
                row_idx += r
                if not is_block_diag:
                    break
                    
            diag_unitary = True
            row_idx = 0
            for i, r in enumerate(blocks):
                block = U[row_idx:row_idx+r, row_idx:row_idx+r]
                diff = block * block.H - eye(r)
                if not all(val == 0 or simplify(val) == 0 for val in diff):
                    diag_unitary = False
                    break
                row_idx += r
                
            q = is_block_diag and diag_unitary
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is partitioned as a block upper triangular matrix",
    "¬Q: U is not block diagonal, or at least one diagonal block is not unitary"
]

N_HYP = 1
NEG_Q_INDEX = 1