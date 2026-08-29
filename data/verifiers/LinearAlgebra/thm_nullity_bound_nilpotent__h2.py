import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - V is a vector space of finite dimension n over a field F.
      - T is nilpotent with index of nilpotency k.
    Conclusion:
      - dim(ker(T)) >= n / k
    """
    # H_1: V is a vector space of finite dimension n over a field F
    # We verify that the witness provides a valid square matrix T.
    try:
        if isinstance(witness, tuple):
            T = None
            # Look for the first item (from the end) that can be interpreted as a square matrix
            for item in reversed(witness):
                try:
                    temp = Matrix(item)
                    if len(temp.shape) == 2 and temp.shape[0] == temp.shape[1]:
                        T = temp
                        break
                except Exception:
                    continue
            if T is None:
                T = witness[0] if witness else witness
        else:
            T = witness
            
        if not isinstance(T, Matrix):
            T = Matrix(T)
            
        if len(T.shape) != 2 or T.shape[0] != T.shape[1]:
            H1 = False
            n = 0
        else:
            H1 = True
            n = T.shape[0]
    except Exception:
        H1 = False
        n = 0

    # H_2: T is nilpotent with index of nilpotency k
    try:
        if not H1:
            H2 = False
            k = 1
        elif n == 0:
            H2 = True
            k = 1
        else:
            H2 = False
            Tk = eye(n)
            for i in range(1, n + 1):
                Tk = Tk * T
                # Check if Tk is the zero matrix
                if Tk.is_zero_matrix is True or all(v.is_zero is True or v == 0 for v in Tk):
                    k = i
                    H2 = True
                    break
            if not H2:
                k = 1
    except Exception:
        H2 = False
        k = 1

    # ¬Q: dim(ker(T)) < n / k
    try:
        if H1 and H2:
            nullity = n - T.rank()
            neg_Q = bool(nullity < n / k)
        else:
            neg_Q = False
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: V is a vector space of finite dimension n over a field F",
    "H_2: T is nilpotent with index of nilpotency k",
    "¬Q: dim(ker(T)) < n/k"
]

N_HYP = 2
NEG_Q_INDEX = 2