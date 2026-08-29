import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard group theory bindings (provided for completeness)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# Standard ring/module bindings for string-based witnesses
ZZ = "ZZ"
QQ = "QQ"
Z = "Z"
Q = "Q"

def conditions(witness):
    try:
        R, M, N, i = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: R is a commutative Noetherian ring
    try:
        R_str = str(R).strip()
        h1 = R_str in ["ZZ", "Z", "Integers", "S.Integers", "QQ", "Q", "Rationals", "S.Rationals", "QQ[x]", "ZZ[x]", "Z/2Z"]
    except Exception:
        h1 = False

    # H2: M is a finitely generated R-module
    try:
        R_str = str(R).strip()
        M_str = str(M).strip()
        h2 = False
        if R_str in ["ZZ", "Z", "Integers", "S.Integers"]:
            h2 = M_str in ["ZZ", "Z", "Integers", "S.Integers", "Z/2Z", "Z/3Z", "Z/nZ", "0", "Z^2", "Z^3"]
        elif R_str in ["QQ", "Q", "Rationals", "S.Rationals"]:
            h2 = M_str in ["QQ", "Q", "Rationals", "S.Rationals", "0", "Q^2", "Q^3"]
    except Exception:
        h2 = False

    # H3: i is a non-negative integer
    try:
        h3 = (isinstance(i, int) or isinstance(i, sympy.Integer)) and i >= 0
    except Exception:
        h3 = False

    # neg_Q: Tor_i^R(M, N) and Ext^i_R(M, N) are finitely generated R-modules (Conclusion must FAIL)
    try:
        def tor(R, M, N, i):
            R_str = str(R).strip()
            M_str = str(M).strip()
            N_str = str(N).strip()
            
            if R_str in ["ZZ", "Z", "Integers", "S.Integers"]:
                if i == 0:
                    if M_str in ["ZZ", "Z", "Integers", "S.Integers"]: return N_str
                    if N_str in ["ZZ", "Z", "Integers", "S.Integers"]: return M_str
                    if M_str == "Z/2Z" and N_str in ["QQ", "Q", "Rationals", "S.Rationals"]: return "0"
                if i == 1:
                    if M_str in ["ZZ", "Z", "Integers", "S.Integers"]: return "0"
                    if N_str in ["ZZ", "Z", "Integers", "S.Integers"]: return "0"
            return "UNKNOWN"

        def ext(R, M, N, i):
            R_str = str(R).strip()
            M_str = str(M).strip()
            N_str = str(N).strip()
            
            if R_str in ["ZZ", "Z", "Integers", "S.Integers"]:
                if i == 0:
                    if M_str in ["ZZ", "Z", "Integers", "S.Integers"]: return N_str
                if i == 1:
                    if M_str in ["ZZ", "Z", "Integers", "S.Integers"]: return "0"
            return "UNKNOWN"

        def is_fg(R, X):
            R_str = str(R).strip()
            X_str = str(X).strip()
            if X_str == "UNKNOWN":
                return None
            if R_str in ["ZZ", "Z", "Integers", "S.Integers"]:
                if X_str in ["ZZ", "Z", "Integers", "S.Integers", "Z/2Z", "Z/3Z", "Z/nZ", "0", "Z^2", "Z^3"]:
                    return True
                if X_str in ["QQ", "Q", "Q/Z", "R", "C", "QQ/ZZ", "Rationals", "S.Rationals"]:
                    return False
            if R_str in ["QQ", "Q", "Rationals", "S.Rationals"]:
                if X_str in ["QQ", "Q", "Rationals", "S.Rationals", "0", "Q^2", "Q^3"]:
                    return True
                if X_str in ["R", "C", "Reals", "Complexes"]:
                    return False
            return None

        tor_val = tor(R, M, N, i)
        ext_val = ext(R, M, N, i)
        
        fg_tor = is_fg(R, tor_val)
        fg_ext = is_fg(R, ext_val)
        
        # The conclusion is that BOTH Tor and Ext are finitely generated.
        # The negated conclusion is True if AT LEAST ONE is known to be NOT finitely generated.
        if fg_tor is False or fg_ext is False:
            neg_q = True
        else:
            neg_q = False
            
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: M is a finitely generated R-module",
    "H_3: i is a non-negative integer",
    "¬Q: Tor_i^R(M, N) or Ext^i_R(M, N) is not a finitely generated R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3