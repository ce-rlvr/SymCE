import itertools
from sympy import isprime, eye, zeros, Integer

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: \\lambda \\in F is an eigenvalue of T",
    "H_3: K_\\lambda is the generalized eigenspace associated with \\lambda",
    "¬Q: K_\\lambda is not a T-invariant subspace of V"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        # Witness format: (p, n, T_func, lambda_val)
        # p: prime number (field Z_p)
        # n: dimension of V (V = Z_p^n)
        # T_func: dict, callable, list of lists, or sympy Matrix representing the map T: V -> V
        # lambda_val: scalar in Z_p
        p, n, T_func, lambda_val = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: V is a vector space over a field F
    try:
        h1 = isprime(p) and isinstance(n, (int, Integer)) and n >= 1 and (p**n <= 1024)
    except Exception:
        h1 = False

    # H_3: K_\lambda is the generalized eigenspace associated with \lambda
    # We verify that T_func and lambda_val are well-formed so we can compute K_\lambda
    try:
        if isinstance(T_func, dict):
            T_eval = lambda x: T_func[x]
            h3 = isinstance(lambda_val, (int, Integer))
        elif callable(T_func):
            T_eval = T_func
            h3 = isinstance(lambda_val, (int, Integer))
        elif isinstance(T_func, (list, tuple)) and len(T_func) == n and len(T_func[0]) == n:
            def T_eval(x):
                return tuple(sum(T_func[i][j] * x[j] for j in range(n)) % p for i in range(n))
            h3 = isinstance(lambda_val, (int, Integer))
        elif hasattr(T_func, 'shape') and T_func.shape == (n, n):
            def T_eval(x):
                from sympy import Matrix
                x_mat = Matrix(n, 1, x)
                res = T_func * x_mat
                return tuple(res[i, 0] % p for i in range(n))
            h3 = isinstance(lambda_val, (int, Integer))
        else:
            T_eval = None
            h3 = False
    except Exception:
        h3 = False

    # Precompute V and T_map to speed up evaluations
    V = []
    zero_vec = None
    T_map = {}
    if h1 and h3:
        try:
            V = list(itertools.product(range(p), repeat=int(n)))
            zero_vec = tuple([0] * int(n))
            for v in V:
                T_map[v] = tuple([int(val % p) for val in T_eval(v)])
        except Exception:
            h1 = False
            h3 = False

    # H_2: \lambda \in F is an eigenvalue of T
    try:
        h2 = False
        if h1 and h3:
            for v in V:
                if v != zero_vec:
                    lam_v = tuple([int((lambda_val * x) % p) for x in v])
                    if T_map[v] == lam_v:
                        h2 = True
                        break
    except Exception:
        h2 = False

    # ¬Q: K_\lambda is not a T-invariant subspace of V
    try:
        neg_q = False
        if h1 and h3:
            # S_map represents the operator (T - \lambda I)
            S_map = {}
            for v in V:
                Tx = T_map[v]
                S_map[v] = tuple([int((Tx[i] - lambda_val * v[i]) % p) for i in range(n)])
            
            # Compute K_\lambda
            K_lambda = set()
            for v in V:
                curr = v
                is_in_K = False
                # Sequence must reach 0 in at most |V| steps if it ever does
                for _ in range(len(V) + 1):
                    curr = S_map[curr]
                    if curr == zero_vec:
                        is_in_K = True
                        break
                if is_in_K:
                    K_lambda.add(v)
            
            # Check if K_\lambda is a subspace
            is_subspace = True
            if zero_vec not in K_lambda:
                is_subspace = False
            else:
                # Closed under addition
                for u in K_lambda:
                    for v in K_lambda:
                        add_uv = tuple([int((u[i] + v[i]) % p) for i in range(n)])
                        if add_uv not in K_lambda:
                            is_subspace = False
                            break
                    if not is_subspace:
                        break
                # Closed under scalar multiplication
                if is_subspace:
                    for u in K_lambda:
                        for c in range(p):
                            cu = tuple([int((c * u[i]) % p) for i in range(n)])
                            if cu not in K_lambda:
                                is_subspace = False
                                break
                        if not is_subspace:
                            break
                            
            # Check if K_\lambda is T-invariant
            is_T_invariant = True
            for u in K_lambda:
                if T_map[u] not in K_lambda:
                    is_T_invariant = False
                    break
                    
            neg_q = not (is_subspace and is_T_invariant)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]