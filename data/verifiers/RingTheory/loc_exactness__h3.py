import sympy
from sympy import Matrix, eye, zeros
import itertools

# Top-level setup for standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The induced sequence 0 \\to S^{-1}M' \\to S^{-1}M \\to S^{-1}M'' \\to 0 is not a short exact sequence"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Expected witness format:
    {
      'n': int, # modulo for the ring Z/nZ (must be >= 2)
      'S': list[int], # multiplicatively closed subset
      'F': sympy.Matrix or list[list[int]], # map M' -> M
      'G': sympy.Matrix or list[list[int]]  # map M -> M''
    }
    """
    try:
        h1 = False
        if isinstance(witness, dict):
            n = witness.get('n', 0)
            if isinstance(n, int) and n >= 2:
                h1 = True
    except Exception:
        h1 = False

    try:
        h2 = False
        if isinstance(witness, dict):
            n = witness.get('n', 0)
            S = witness.get('S', [])
            if isinstance(n, int) and n >= 2 and isinstance(S, (list, tuple, set)) and len(S) > 0:
                S_set = set(s % n for s in S)
                if 1 in S_set:
                    closed = True
                    for a in S_set:
                        for b in S_set:
                            if (a * b) % n not in S_set:
                                closed = False
                                break
                        if not closed:
                            break
                    h2 = closed
    except Exception:
        h2 = False

    try:
        neg_q = False
        if isinstance(witness, dict):
            n = witness.get('n', 0)
            S = witness.get('S', [])
            F = witness.get('F')
            G = witness.get('G')
            
            if isinstance(n, int) and n >= 2 and isinstance(S, (list, tuple, set)) and len(S) > 0:
                S_set = set(s % n for s in S)
                
                F_mat = Matrix(F)
                G_mat = Matrix(G)
                
                b, a = F_mat.shape
                c, b2 = G_mat.shape
                
                if b != b2:
                    neg_q = True
                elif n**a <= 10000 and n**b <= 10000 and n**c <= 10000:
                    F_list = [[int(val) % n for val in row] for row in F_mat.tolist()]
                    G_list = [[int(val) % n for val in row] for row in G_mat.tolist()]

                    def is_zero_in_localized(v):
                        for s in S_set:
                            if all((s * vi) % n == 0 for vi in v):
                                return True
                        return False

                    def mat_mul(A, x):
                        return tuple(sum(A[i][j] * x[j] for j in range(len(x))) % n for i in range(len(A)))

                    injective = True
                    for x in itertools.product(range(n), repeat=a):
                        fx = mat_mul(F_list, x)
                        if is_zero_in_localized(fx):
                            if not is_zero_in_localized(x):
                                injective = False
                                break
                    
                    im_subset_ker = True
                    if injective:
                        for x in itertools.product(range(n), repeat=a):
                            fx = mat_mul(F_list, x)
                            gfx = mat_mul(G_list, fx)
                            if not is_zero_in_localized(gfx):
                                im_subset_ker = False
                                break
                    
                    ker_subset_im = True
                    if injective and im_subset_ker:
                        im_f = set()
                        for x in itertools.product(range(n), repeat=a):
                            im_f.add(mat_mul(F_list, x))
                        
                        for y in itertools.product(range(n), repeat=b):
                            gy = mat_mul(G_list, y)
                            if is_zero_in_localized(gy):
                                found = False
                                for s in S_set:
                                    sy = tuple((s * yi) % n for yi in y)
                                    if sy in im_f:
                                        found = True
                                        break
                                if not found:
                                    ker_subset_im = False
                                    break
                    
                    surjective = True
                    if injective and im_subset_ker and ker_subset_im:
                        im_g = set()
                        for y in itertools.product(range(n), repeat=b):
                            im_g.add(mat_mul(G_list, y))
                            
                        for z in itertools.product(range(n), repeat=c):
                            found = False
                            for s in S_set:
                                sz = tuple((s * zi) % n for zi in z)
                                if sz in im_g:
                                    found = True
                                    break
                            if not found:
                                surjective = False
                                break
                    
                    if not (injective and im_subset_ker and ker_subset_im and surjective):
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]