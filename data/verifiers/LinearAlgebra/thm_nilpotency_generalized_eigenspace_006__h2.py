import sympy
from sympy import Matrix, eye
import itertools

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "The restriction of the operator T - lambda I to the subspace W_lambda is a nilpotent operator."
    
    The dropped hypothesis from the true theorem is "T is a linear operator".
    A valid counterexample is a non-linear operator T on a finite-dimensional vector space
    where the generalized eigenspace W_lambda is NOT a subspace, making the conclusion false.
    
    Expected witness format:
    (n, T_dict, lam, W_lam_witness)
    where:
      - n: dimension of the vector space GF(2)^n
      - T_dict: dictionary mapping tuple[int] to tuple[int] representing the operator T
      - lam: scalar eigenvalue in GF(2)
      - W_lam_witness: list of tuple[int] representing the generalized eigenspace
    """
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        n, T_dict, lam, W_lam_witness = witness
        
        V = list(itertools.product([0, 1], repeat=n))
        H1 = True
        if not isinstance(n, int) or n < 1:
            H1 = False
        for v in V:
            if v not in T_dict:
                H1 = False
                break
            Tv = T_dict[v]
            if not isinstance(Tv, tuple) or len(Tv) != n:
                H1 = False
                break
                
        H2 = False
        zero = tuple([0] * n)
        for v in V:
            if v != zero:
                Tv = T_dict.get(v, None)
                if Tv is not None:
                    lam_v = tuple([(lam * x) % 2 for x in v])
                    if Tv == lam_v:
                        H2 = True
                        break
                        
        W_lam_computed = []
        for v in V:
            curr = v
            is_in_W = False
            for _ in range(len(V) + 1):
                Tx = T_dict.get(curr, zero)
                lam_x = tuple([(lam * x) % 2 for x in curr])
                curr = tuple([(Tx[i] - lam_x[i]) % 2 for i in range(n)])
                if curr == zero:
                    is_in_W = True
                    break
            if is_in_W:
                W_lam_computed.append(v)
                
        W_lam_witness_set = set(W_lam_witness)
        W_lam_computed_set = set(W_lam_computed)
        H3 = (W_lam_witness_set == W_lam_computed_set)
        
        is_subspace = True
        if zero not in W_lam_computed_set:
            is_subspace = False
        else:
            for u in W_lam_computed_set:
                for v in W_lam_computed_set:
                    u_plus_v = tuple([(u[i] + v[i]) % 2 for i in range(n)])
                    if u_plus_v not in W_lam_computed_set:
                        is_subspace = False
                        break
                if not is_subspace:
                    break
                    
        is_nilpotent = False
        if is_subspace:
            K = len(W_lam_computed_set)
            is_nilpotent = True
            for v in W_lam_computed_set:
                curr = v
                for _ in range(K):
                    Tx = T_dict.get(curr, zero)
                    lam_x = tuple([(lam * x) % 2 for x in curr])
                    curr = tuple([(Tx[i] - lam_x[i]) % 2 for i in range(n)])
                if curr != zero:
                    is_nilpotent = False
                    break
                    
        neg_Q = not (is_subspace and is_nilpotent)
        
        return [H1, H2, H3, neg_Q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: lambda is an eigenvalue of T",
    "H_3: W_lambda is the generalized eigenspace of T corresponding to lambda",
    "¬Q: The restriction of the operator T - lambda I to the subspace W_lambda is not a nilpotent operator"
]

N_HYP = 3
NEG_Q_INDEX = 3