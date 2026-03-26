from textwrap import dedent
import general as gen
from fractions import Fraction
import sympy as sp

import logging 
log = logging.getLogger(__name__)  

def string_of_estimate(est, type):

    text = "\n" + r"""  \item """
    templates = {
        'dyadic': r"""$\|T_jf\|_q \lesssim 2^{\kappa j}\|f\|_p$ for all $j\in\mathbb{N}$ where $(\frac{1}{p},\frac{1}{q},\kappa) = """,
        'ss':     r"""$\|Tf\|_q \lesssim  \|f\|_p$ for $(\frac{1}{p},\frac{1}{q}) = """,
        'sw':     r"""$\|Tf\|_{q,\infty} \lesssim  \|f\|_p$ for $(\frac{1}{p},\frac{1}{q}) = """,
        'ws':     r"""$\|Tf\|_q \lesssim  \|f\|_{p,1}$ for $(\frac{1}{p},\frac{1}{q}) = """,
        'ww':     r"""$\|Tf\|_{q,\infty} \lesssim  \|f\|_{p,1}$ for $(\frac{1}{p},\frac{1}{q}) = """
    }
    return text + templates[type] + latexsymbolic(est) + "$"



def latexpoints(pts):
    text = ["\n $$ \n"]
    for pt in pts:
        if pt[2]:
            text.append(r"""(\frac{1}{p},\frac{1}{q}) = (""" +
                        latexsymbolic(pt[0]) + "," +
                        latexsymbolic(pt[1]) + ")")
    text.append("\n $$ \n")
    return "".join(text) 

def latexsegment(pt0, pt1):

    x0, y0 = pt0[0], pt0[1]
    x1, y1 = pt1[0], pt1[1]
    if x0 == y0 and x1 == y1:
        log.error("This is not a segment.")
        exit()

    # Helper
    def interval(a, b, left_closed, right_closed, var):
        l = r"\leq" if left_closed else "<"
        r_ = r"\leq" if right_closed else "<"
        return latexsymbolic(a) + f" {l} {var} {r_} " + latexsymbolic(b)

    left_closed = pt0[2]
    right_closed = pt1[2]

    if x0 < x1 and y0 != y1:
        b = (x1 - x0) / (y0 - y1)
        c = x0 + b * y0
        sign = "+" if b > 0 else "-"
        b_abs = b if b > 0 else -b
        eq = r"""\frac{1}{p} """ + sign + " " + latexsymbolic(b_abs) + r"""\cdot\frac{1}{q} = """ + latexsymbolic(c)
        interval_str = interval(x0, x1, left_closed, right_closed, r"\frac{1}{p}")
        return "\n $$ \n  " + eq + r"""\qquad""" + interval_str + "\n $$"

    elif x0 < x1 and y0 == y1:
        eq = r"""\frac{1}{q} = """ + latexsymbolic(y0)
        interval_str = interval(x0, x1, left_closed, right_closed, r"\frac{1}{p}")
        return "\n $$ \n  " + eq + r"""\qquad""" + interval_str + "\n $$"

    elif x0 == x1 and y0 < y1:
        eq = r"""\frac{1}{p} = """ + latexsymbolic(x0)
        interval_str = interval(y0, y1, left_closed, right_closed, r"\frac{1}{q}")
        return "\n $$ \n  " + eq + r"""\qquad""" + interval_str + "\n $$"

    else:
        return latexsegment(pt1, pt0)

def introtext(input_variables):
    
    dyadic_estimates = input_variables[1]
    ss_estimates = input_variables[2]
    ws_estimates = input_variables[3]
    sw_estimates = input_variables[4]
    ww_estimates = input_variables[5]
    d_list = input_variables[6]
    selfadjoint = input_variables[7] 
    X_finite_measure = input_variables[8]
    Y_finite_measure = input_variables[9] 

    text=[] 
    text.append(dedent(r"""
\documentclass[12pt]{article}
\usepackage{graphicx}
\usepackage{amssymb}
\usepackage{amsmath}

\begin{document}

\section*{Interpolation result}
  
  The task is to interpolate some given estimates for the linear operator(s) $T$ or $T_j$ where
  $$ 
    T  = \sum_{j\in\mathbb{N}} T_j
  $$
  where $T,T_j:X\to Y$ are measurable functions between measure spaces $X,Y$. 
  In the following, standard norms on Lebesgue spaces $L^p(X),L^q(Y)$ or Lorentz space $L^{p,s}(X),L^{q,s}(Y)$ 
  with $p,q,s\in [1,\infty]$ will be denoted by
  $\|\cdot\|_p$ and $\|\cdot\|_{p,s}$, respectively. 
  We use complex and real interpolation theory.                       
  The estimates for $T,T_j$ in general depend on some parameter $d\in\mathbb{N}$.
  It often plays the role of the space dimension where $X$ or $Y$ is a $d$-dimensional Riemannian manifold.   
  See the end of this pdf file for general explanations of the
  Riesz diagrams on the following page(s).                       
                       
\subsection*{Your input data}                       
"""))
    if X_finite_measure and Y_finite_measure:
        text.append(r"""\medskip"""+"\n\n"+r"""\noindent We use the information that $X$ and $Y$ have finite measure."""+"\n")
    elif X_finite_measure:
        text.append(r"""\medskip"""+"\n\n"+r"""\noindent We use the information that $X$ has finite measure."""+"\n")
    elif Y_finite_measure:
        text.append(r"""\medskip"""+"\n\n"+r"""\noindent We use the information that $Y$ has finite measure."""+"\n")
    if selfadjoint:
        text.append(r"""\medskip"""+"\n\n"+r"""\noindent We take into account that $T$ and all $T_j$ are assumed to be selfadjoint."""+"\n")        
    text.append(r"""\begin{itemize}""" + "\n  "+r"""\itemsep-2pt""")    
    for est in dyadic_estimates:
        text.append(string_of_estimate(est,"dyadic"))
    for est in ss_estimates:
        text.append(string_of_estimate(est,"ss"))
    for est in sw_estimates:
        text.append(string_of_estimate(est,"sw"))
    for est in ws_estimates:
        text.append(string_of_estimate(est,"ws"))    
    for est in ww_estimates:
        text.append(string_of_estimate(est,"ww"))    
    text.append("\n"+r"""\end{itemize}"""+"\n"+r"""\noindent We consider parameters"""+"\n $$ \n"+ r"""  d \in \{"""+ gen.toString(d_list)[1:-1]+r"""\}."""+"\n $$ \n")                  
    return "".join(text)                    

def latexsymbolic(expr):    
        
    if isinstance(expr,int):
        return str(expr)    
    elif isinstance(expr,float): 
        return latexsymbolic(gen.rationalize(expr))        
    elif isinstance(expr,sp.Float): 
        return latexsymbolic(float(expr))       
    elif isinstance(expr,Fraction): 
        den = expr.denominator
        num = expr.numerator 
        if num>=0:
            if den==1:
                return str(num).replace("*"," \cdot ")            
            else:
                return r"""\frac{"""+latexsymbolic(num)+r"""}{"""+latexsymbolic(den)+r"""}"""          
        else:
            if den==1:                
                return "-"+str(-num).replace("*"," \cdot ")    
            else:                
                return "-"+r"""\frac{"""+latexsymbolic(-num)+r"""}{"""+latexsymbolic(den)+r"""}"""          
    elif isinstance(expr, sp.Basic):        
        num, den = expr.as_numer_denom()
        if den==1:
            return str(num).replace("*"," \cdot ")    
        elif den==-1:    
            return "-"+str(-num).replace("*"," \cdot ")    
        else:          
            return r"""\frac{"""+latexsymbolic(num)+r"""}{"""+latexsymbolic(den)+r"""}"""    
    elif isinstance(expr,list) or isinstance(expr,tuple):     
        inner = ", ".join(latexsymbolic(x) for x in expr)
        return f"({inner})"    
    return expr


def latextext(pqcond, symbol):

    strict = (symbol == '<>')

    # def comp(a, b, var):
    #     if a == 1:
    #         return var
    #     elif a == -1:
    #         return "-" + var
    #     return None

    # Single variable cases
    if pqcond[1] == 0:
        var = r"\frac{1}{p}"
        rhs = latexsymbolic(pqcond[2] if pqcond[0] == 1 else -pqcond[2])
        op = "<" if strict else r"\leq"
        if pqcond[0] == -1:
            op = ">" if strict else r"\geq"
        return var + " " + op + " " + rhs

    if pqcond[0] == 0:
        var = r"\frac{1}{q}"
        rhs = latexsymbolic(pqcond[2] if pqcond[1] == 1 else -pqcond[2])
        op = "<" if strict else r"\leq"
        if pqcond[1] == -1:
            op = ">" if strict else r"\geq"
        return var + " " + op + " " + rhs

    # General case
    coeff = pqcond[1] / pqcond[0]
    rhs = pqcond[2] / pqcond[0]

    if coeff == 1:
        lhs = r"\frac{1}{p} + \frac{1}{q}"
    elif coeff == -1:
        lhs = r"\frac{1}{p} - \frac{1}{q}"
    elif coeff > 0:
        lhs = r"\frac{1}{p} + " + latexsymbolic(coeff) + r"\cdot \frac{1}{q}"
    else:
        lhs = r"\frac{1}{p} - " + latexsymbolic(-coeff) + r"\cdot \frac{1}{q}"

    if pqcond[0] > 0:
        op = "<" if strict else r"\leq"
    else:
        op = ">" if strict else r"\geq"

    return lhs + op + latexsymbolic(rhs)
    


def extrotext():

    return r"""
\newpage
\section*{Basic explanations:}
     \begin{itemize}
       \itemsep-2pt 
       \item Generally speaking, a Riesz diagram depicts the set of $(\frac{1}{p},\frac{1}{q})$ such that $T$ satisfies an estimate of the form
       \begin{align*}
         \|Tf\|_q \lesssim \|f\|_p,\qquad
         \|Tf\|_{q,s} \lesssim \|f\|_{p,s} \quad\forall s\in [1,\infty], \\
         \|Tf\|_{q,\infty} \lesssim \|f\|_p,\quad
         \|Tf\|_q \lesssim \|f\|_{p,1},\quad
         \|Tf\|_{q,\infty} \lesssim \|f\|_{p,1}.
       \end{align*}
       Here, $p,q\in [1,\infty]$ and $\lesssim$ stands for $\leq C$ where $C$ is a positive number that is independent of the function $f$.
       We use the word ``region of validity'' for simplicity.
       The title of the Riesz diagram indicates which kind of estimate is meant and for which parameter $d$.
       The regions of validity for weak-type estimates, Lebesgue estimates, etc. 
       are identical possibly except for some estimates on the boundary.
       \item The Riesz diagram is a 2D polygon, which is very easy to identify. 
       This is in contrast to the corresponding
       representation in "natural coordinates" $p,q\in [1,\infty]$, which is a curved and unbounded geometrical object.        
       \item The orange region shows the interior of the region of validity.
       \item Corners: the estimates need not hold at the red points, but they do hold at the black and
       green points.
       \item Edges: the estimates need not hold along the red dotted segments, but they do hold along the
       black solid lines. This only refers to the relative interior of the segment. In other words, being red
       dotted or black solid does not affect the validity of the estimate at the endpoints of the segment.
       \item The pale blue  region in the background is the Riesz diagram depicting those exponents
       where dyadic estimates are known from the input data. If, effectively, there are less than two of such estimates, this region will be void. 
       \item If no other (i.e., non-dyadic) estimate from outside the blue region is
       given, the orange region of validity will be a subset of the blue region. Otherwise, it will
       be larger.       
     \end{itemize}

\end{document}     
"""
 