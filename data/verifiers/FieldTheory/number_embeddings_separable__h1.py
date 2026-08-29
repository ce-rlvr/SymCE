import sympy
from sympy import oo

QQ = "QQ"
QQ_x = "QQ(x)"
QQ_bar = "QQ_bar"
CC = "CC"
RR = "RR"
Fp = "Fp"
Fp_x = "Fp(x)"
Fp_bar = "Fp_bar"

CONDITION_LABELS = [
    "H_1: E/K is a separable extension",
    "H_2: C is an algebraically closed field containing K",
    "¬Q: The number of distinct K-algebra homomorphisms from E into C is not exactly the degree of E over K"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False]
        
        K, E, C = witness
        
        if not isinstance(K, str): K = str(K)
        if not isinstance(E, str): E = str(E)
        if not isinstance(C, str): C = str(C)
        
        h1 = False
        if K == "QQ" and E in ["QQ", "QQ(x)", "QQ_bar", "RR", "CC"]:
            h1 = True
        elif K == "Fp" and E in ["Fp", "Fp(x)", "Fp_bar"]:
            h1 = True
        elif K == "RR" and E in ["RR", "CC"]:
            h1 = True
        elif K == "QQ" and E.startswith("QQ(sqrt("):
            h1 = True
            
        h2 = False
        if C in ["QQ_bar", "CC", "Fp_bar"]:
            if K == "QQ" and C in ["QQ_bar", "CC"]:
                h2 = True
            elif K == "RR" and C == "CC":
                h2 = True
            elif K == "Fp" and C == "Fp_bar":
                h2 = True
            elif K == C:
                h2 = True
                
        deg = None
        if K == "QQ":
            if E == "QQ": deg = 1
            elif E == "QQ(x)": deg = "aleph_0"
            elif E == "QQ_bar": deg = "aleph_0"
            elif E == "RR": deg = "continuum"
            elif E == "CC": deg = "continuum"
            elif E.startswith("QQ(sqrt("): deg = 2
        elif K == "Fp":
            if E == "Fp": deg = 1
            elif E == "Fp(x)": deg = "aleph_0"
            elif E == "Fp_bar": deg = "aleph_0"
        elif K == "RR":
            if E == "RR": deg = 1
            elif E == "CC": deg = 2
            
        num_homs = None
        if K == "QQ":
            if E == "QQ":
                if C in ["QQ_bar", "CC"]: num_homs = 1
            elif E == "QQ(x)":
                if C == "QQ_bar": num_homs = "aleph_0"
                elif C == "CC": num_homs = "continuum"
            elif E == "QQ_bar":
                if C == "QQ_bar": num_homs = "continuum"
                elif C == "CC": num_homs = "continuum"
            elif E == "RR":
                if C == "CC": num_homs = "2^continuum"
            elif E == "CC":
                if C == "CC": num_homs = "2^continuum"
            elif E.startswith("QQ(sqrt("):
                if C in ["QQ_bar", "CC"]: num_homs = 2
        elif K == "Fp":
            if E == "Fp":
                if C == "Fp_bar": num_homs = 1
            elif E == "Fp(x)":
                if C == "Fp_bar": num_homs = "aleph_0"
            elif E == "Fp_bar":
                if C == "Fp_bar": num_homs = "continuum"
        elif K == "RR":
            if E == "RR":
                if C == "CC": num_homs = 1
            elif E == "CC":
                if C == "CC": num_homs = 2
                
        if deg is None or num_homs is None:
            neg_q = False
        else:
            neg_q = (deg != num_homs)
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]