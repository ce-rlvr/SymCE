import itertools
from sympy import isprime, Matrix, simplify, eye, zeros

# Top-level setup for standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Supports two witness formats:
    
    Format 1 (Finite Field Exhaustive):
      witness = (T, lam, p, n)
      - T: callable or dict mapping tuple of ints to tuple of ints
      - lam: int (eigenvalue)
      - p: prime int (field Z_p)
      - n: int >= 1 (dimension)
      
    Format 2 (Specific Vectors over any field):
      witness = (T, lam, v1, v2, c)
      - T: callable taking a sympy Matrix and returning a sympy Matrix
      - lam: scalar
      - v1: sympy Matrix (non-zero, in E_lambda)
      - v2: sympy Matrix (in E_lambda, to test addition closure)
      - c: scalar (to test scalar multiplication closure)
    """
    h1_ok = False
    h2_ok = False
    h3_ok = True  # H3 is a definition
    neg_q_ok = False

    if isinstance(witness, tuple) and len(witness) == 4:
        try:
            T, lam, p, n = witness
            
            # H1: V is a vector space over a field F
            if isprime(p) and isinstance(n, int) and n >= 1 and (p**n <= 4096):
                h1_ok = True
            else:
                return [False, False, False, False]
                
            V_elements = list(itertools.product(range(p), repeat=n))
            
            def eval_T(v):
                if isinstance(T, dict):
                    res = T[v]
                elif hasattr(T, 'shape') and len(T.shape) == 2:
                    v_mat = Matrix(n, 1, v)
                    res_mat = T * v_mat
                    res = tuple(res_mat)
                else:
                    res = T(v)
                return tuple(int(x) % p for x in res)
                
            # H2: \lambda \in F is an eigenvalue of T
            lam = int(lam) % p
            zero_vec = (0,) * n
            for v in V_elements:
                if v != zero_vec:
                    if eval_T(v) == tuple((lam * x) % p for x in v):
                        h2_ok = True
                        break
                        
            # Negated Conclusion: E_\lambda is NOT a T-invariant subspace of V
            E_lambda = set()
            for v in V_elements:
                if eval_T(v) == tuple((lam * x) % p for x in v):
                    E_lambda.add(v)
                    
            is_subspace = True
            if zero_vec not in E_lambda:
                is_subspace = False
            else:
                for u in E_lambda:
                    for v in E_lambda:
                        if tuple((u[i] + v[i]) % p for i in range(n)) not in E_lambda:
                            is_subspace = False
                            break
                    if not is_subspace:
                        break
                if is_subspace:
                    for u in E_lambda:
                        for c_scalar in range(p):
                            if tuple((c_scalar * u[i]) % p for i in range(n)) not in E_lambda:
                                is_subspace = False
                                break
                        if not is_subspace:
                            break
                            
            is_T_invariant = True
            for u in E_lambda:
                if eval_T(u) not in E_lambda:
                    is_T_invariant = False
                    break
                    
            neg_q_ok = not (is_subspace and is_T_invariant)
            
        except Exception:
            pass

    elif isinstance(witness, tuple) and len(witness) == 5:
        try:
            T, lam, v1, v2, c = witness
            
            if not isinstance(v1, Matrix):
                v1 = Matrix(v1)
            if not isinstance(v2, Matrix):
                v2 = Matrix(v2)
                
            # H1: V is a vector space over a field F
            if v1.shape == v2.shape:
                h1_ok = True
                
            def safe_T(v):
                if hasattr(T, 'shape') and len(T.shape) == 2:
                    res = T * v
                else:
                    res = T(v)
                if not isinstance(res, Matrix):
                    res = Matrix(res)
                return res

            def is_in_E(v):
                diff = safe_T(v) - lam * v
                for x in diff:
                    if simplify(x) != 0:
                        return False
                return True

            # H2: \lambda \in F is an eigenvalue of T
            is_nonzero = any(simplify(x) != 0 for x in v1)
            if is_nonzero and is_in_E(v1):
                h2_ok = True
                
            # Negated Conclusion: E_\lambda is NOT a T-invariant subspace of V
            zero = v1 * 0
            
            if not is_in_E(zero):
                neg_q_ok = True
            elif is_in_E(v2) and not is_in_E(v1 + v2):
                neg_q_ok = True
            elif not is_in_E(c * v1):
                neg_q_ok = True
            elif not is_in_E(safe_T(v1)):
                neg_q_ok = True
                
        except Exception:
            pass

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: \\lambda \\in F is an eigenvalue of T",
    "H_3: E_\\lambda = \\{v \\in V \\mid T(v) = \\lambda v\\} is the eigenspace associated with \\lambda",
    "¬Q: E_\\lambda is NOT a T-invariant subspace of V"
]

N_HYP = 3
NEG_Q_INDEX = 3