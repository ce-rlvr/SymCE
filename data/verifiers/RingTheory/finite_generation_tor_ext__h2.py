import sympy

# Top-level setup
# (No specific SymPy objects needed for this algebraic counterexample since we use string representations)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get("R")
            M = witness.get("M")
            N = witness.get("N")
            i = witness.get("i")
        elif isinstance(witness, tuple) and len(witness) == 4:
            R, M, N, i = witness
        else:
            return [False, False, False, False]
            
        # H1: R is a commutative Noetherian ring
        def check_h1(R):
            return R in ["Z", "Q", "R", "C", "k[x]", "k[x,y]", "Z[x]", "k[[x]]"]
            
        # H2: N is a finitely generated R-module
        def check_h2(N, R):
            if R == "Z":
                return N in ["Z", "0", "Z/2Z", "Z/3Z", "Z^2", "Z^3"]
            if R in ["k[x]", "k[x,y]", "Z[x]", "k[[x]]"]:
                return N in [R, "0", R + "^2", R + "^3"]
            return False
            
        # H3: i is a non-negative integer
        def check_h3(i):
            return type(i) is int and i >= 0
            
        # neg_Q: Tor_i^R(M, N) and Ext^i_R(M, N) are not both finitely generated R-modules
        def check_neg_q(R, M, N, i):
            if R == "Z":
                if M in ["Q", "Q/Z", "Z[1/2]", "Z[1/3]", "Z^infty", "Z^(N)", "oplus Z"] and N in ["Z", "Z^2", "Z^3"]:
                    if i in [0, 1]:
                        return True
            if R == "k[x]":
                if M in ["k(x)", "k[x]^infty"] and N in ["k[x]", "k[x]^2", "k[x]^3"]:
                    if i in [0, 1]:
                        return True
            if R == "k[x,y]":
                if M in ["k(x,y)", "k[x,y]^infty"] and N in ["k[x,y]", "k[x,y]^2", "k[x,y]^3"]:
                    if i in [0, 1, 2]:
                        return True
            if R == "k[[x]]":
                if M in ["k((x))", "k[[x]]^infty"] and N in ["k[[x]]", "k[[x]]^2", "k[[x]]^3"]:
                    if i in [0, 1]:
                        return True
            return False
            
        h1 = check_h1(R)
        h2 = check_h2(N, R)
        h3 = check_h3(i)
        neg_q = check_neg_q(R, M, N, i)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: N is a finitely generated R-module",
    "H_3: i is a non-negative integer",
    "¬Q: Tor_i^R(M, N) and Ext^i_R(M, N) are not both finitely generated R-modules"
]

N_HYP = 3
NEG_Q_INDEX = 3