GENERAL CONTENT:

Assume T = \sum_{j\in\mathbb{N}} T_j where T,T_j are linear operators that map measurable functions defined 
on a measure space X to measurable functions defined on a measure space Y. Based on the input data the program generates 
a pdf file describing and depicting the region of exponents p,q\in [1,\infty] where 
estimates of the form \|Tf\|_{L^q(Y)}\leq C\|f\|_{L^p(X)} or variants thereof hold. 
This is based on real and complex interpolation theory. Riesz diagrams are used to visualize the result. 

The input data is processed using rational numbers in decimal of fractional form. The given estimates may depend on some 
non-specified parameter d using +,-,* and /. Computations and plots is executed only for specific values of integer values of d. 
The default values of some input fields (see below) permit to produce an output just by inserting the estimates.


YOUR INPUT:
(In the following, the quotation marks "" indicate the begin/end of the input string. Please do not type them.)

* Views.Content:  A finite sequence of elements of \{1,2,3,4,5\}. It stands for the estimates the user wants to have analyzed.
  1: \|Tf\|_{L^{q,\infty}(Y)} \leq C \|f\|_{L^{p,1}(X)}
  2: \|Tf\|_{L^{q,s}(Y)} \leq C \|f\|_{L^{p,s}(X)} for all s\in [1,\infty]
  3: \|Tf\|_{L^q(Y)} \leq C \|f\|_{L^{p,1}(X)}
  4: \|Tf\|_{L^{q,\infty}(Y)} \leq C \|f\|_{L^p(X)}
  5: \|Tf\|_{L^q(Y)} \leq C \|f\|_{L^p(X)} 
  Views.Examples: "5" or "2,3,4" or "1,3,5"
  Views.Default: "5"
  The Riesz diagrams for 1,2,3,4,5 are actually identical except for the boundary.

* Dyadic Estimates.Content: A list of [1/p,1/q,\kappa] where an \|T_jf\|_q \leq C 2^{\kappa j} \|f\|_p is known. 
  So the first and second entries are numbers between 0 and 1 and kappa is an arbitrary rational number. 
  The numbers may depend on some formal integer parameter d and the above needs to hold for all admissible d.
  Dyadic Estimates.Examples: "[0.4,0.2,-2],[0.8,0.6,1],[d/(d+1),0.5,-d]"
  Dyadic Estimates.Default: ""

* Lebesgue Estimates.Content: A list of [1/p,1/q] where \|Tf\|_q \leq C \|f\|_p is known. 
  Again the numbers may depend on some formal integer parameter d.
  Lebesgue Estimates.Examples: "[0.4,0.2],[d/(2*(d+1)),1/(2*d)]" 
  Lebesgue Estimates.Default: ""

* Weak-Strong Estimates.Content: A list of [1/p,1/q] where \|Tf\|_q \leq C \|f\|_{p,1} is known. 
  Again the numbers may depend on some formal integer parameter d.
  Weak-Strong Estimates.Examples: "[0.3,0.2]" 
  Weak-Strong Estimates.Default: ""

* Strong-Weak Estimates.Content: A list of [1/p,1/q] where \|Tf\|_{q,\infty} \leq C \|f\|_p is known. 
  Again the numbers may depend on some formal integer parameter d.
  Strong-Weak Estimates.Examples: ""
  Strong-Weak Estimates.Default: ""

* Weak-Type Estimates.Content: A list of [1/p,1/q] where \|Tf\|_{q,\infty} \leq C \|f\|_{p,1} is known. 
  Again the numbers may depend on some formal integer parameter d.
  Weak-Type Estimates.Examples: "[0.8,(d+1)/(2*d)]" 
  Weak-Type Estimates.Default: ""

Interpolation requires at least two valid estimates, so the input data must lead to such. 
Otherwise the program will run into an error.

* List of d-parameter.Content: A list of admissible integer-valued d-parameters that the user wants to consider. 
  List of d-parameter.Examples: "1,3,4"
  List of d-parameter.Default: "2"

* symmetric: If T and all T_j are marked to be symmetric, then the induced dual estimates are added.
  Accordingly, the Riesz diagram is then symmetric with respect to (p,q) <-> (q',p').

* X of finite measure: If marked then X is assumed to have finite measure, so trivial estimates based on the embeddings 
  of Lebesgue spaces are added. The Riesz diagram is then filled all the way to the left where 1/p=0. 

* Y of finite measure: If marked then Y is assumed to have finite measure, so trivial estimates based on the embeddings 
  of Lebesgue spaces are added. The Riesz diagram is then filled all the way to the top where 1/q = 1.


FEEDBACK:
In case of errors please send your data to Rainer.Mandel@gmx.de and I will try to fix it as soon as possible. 
Other feedback is welcome as well.
