import math
import itertools
import functools
from sympy import Matrix, sympify

class NumberFieldIdealWitness:
    """
    A helper class for constructing witnesses for this conjecture.
    - K_is_number_field: bool
    - O_K_is_ring_of_integers: bool
    - n: int (degree of the number field)
    - mult: 3D list of size n x n x n representing the multiplication table of O_K
            mult[i][j][k] is the k-th coordinate of e_i * e_j
    - I: 2D list of size n x n representing the Z-basis of ideal I
    - J: 2D list of size n x n representing the Z-basis of submodule J
    """
    def __init__(self, K_is_number_field, O_K_is_ring_of_integers, n, mult, I, J):
        self.K_is_number_field = K_is_number_field
        self.O_K_is_ring_of_integers = O_K_is_ring_of_integers
        self.n = n
        self.mult = mult
        self.I = I
        self.J = J

def get_attr(obj, attr):
    if isinstance(obj, dict):
        return obj[attr]
    return getattr(obj, attr)

def conditions(witness) -> list[bool]:
    # H_1: K is a number field
    try:
        h1 = bool(get_attr(witness, 'K_is_number_field'))
    except Exception:
        h1 = False

    # H_2: O_K is the ring of integers of K
    try:
        h2 = bool(get_attr(witness, 'O_K_is_ring_of_integers'))
    except Exception:
        h2 = False

    # H_3: I is a non-zero ideal of O_K
    try:
        n = get_attr(witness, 'n')
        mult = get_attr(witness, 'mult')
        M_I = get_attr(witness, 'I')
        
        M = Matrix(M_I)
        M_I_list = M.tolist()
        
        if M.det() == 0:
            h3 = False
        else:
            M_inv = M.inv()
            is_id = True
            for k in range(n):
                u = [1 if i == k else 0 for i in range(n)]
                for row in M_I_list:
                    p = [0] * n
                    for i in range(n):
                        for j in range(n):
                            for m in range(n):
                                p[m] += u[i] * row[j] * mult[i][j][m]
                    c = Matrix(1, n, p) * M_inv
                    for val in c:
                        if not sympify(val).is_integer:
                            is_id = False
                            break
                    if not is_id:
                        break
                if not is_id:
                    break
            h3 = is_id
    except Exception:
        h3 = False

    # ¬Q: N(IJ) != N(I)N(J)
    try:
        n = get_attr(witness, 'n')
        mult = get_attr(witness, 'mult')
        M_I = get_attr(witness, 'I')
        M_J = get_attr(witness, 'J')
        
        M_I_mat = Matrix(M_I)
        M_J_mat = Matrix(M_J)
        
        M_I_list = M_I_mat.tolist()
        M_J_list = M_J_mat.tolist()
        
        N_I = int(abs(M_I_mat.det()))
        N_J = int(abs(M_J_mat.det()))
        
        products = []
        for row_I in M_I_list:
            for row_J in M_J_list:
                p = [0] * n
                for i in range(n):
                    for j in range(n):
                        for m in range(n):
                            p[m] += row_I[i] * row_J[j] * mult[i][j][m]
                products.append(p)
        
        M_IJ = Matrix(products)
        minors = []
        for rows in itertools.combinations(range(len(products)), n):
            subM = M_IJ[list(rows), :]
            minors.append(int(abs(subM.det())))
        
        if not minors:
            neg_q = False
        else:
            N_IJ = minors[0]
            for m in minors[1:]:
                N_IJ = math.gcd(N_IJ, m)
                
            neg_q = (N_IJ != N_I * N_J)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a number field",
    "H_2: O_K is the ring of integers of K",
    "H_3: I is a non-zero ideal of O_K",
    "¬Q: N(IJ) != N(I)N(J)"
]

N_HYP = 3
NEG_Q_INDEX = 3