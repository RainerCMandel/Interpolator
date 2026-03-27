import interpolator as inter 
import general as gen
import plotter as plotter
import sympy as sp
import input as inp 
import latexwriter
import sys 
import matplotlib 
matplotlib.use("Agg") 
import logging 
log = logging.getLogger(__name__)  



def create_input_data():
   ### USER INPUT

   ## Which Riesz diagrams should be displayed?    
   # 1 stands for L^{p,1}\to L^{q,\infty}
   # 2 stands for L {p,s}\to L^{q,s}
   # 3 stands for L^{p,1}\to L^q
   # 4 stands for L^p\to L^{q,\infty}
   # 5 stands for L^p\to L^q
   # Example: view = [2,1]
   view = [1,5]

   ## Which dyadic estimates \|T_jf\|_q\les 2^{-\kappa j}\|f\|_p are given? 
   # Please provide them as arrays [1/p,1/q,\kappa] and p,q,\kappa may depend on a parameter d.
   # Example 1: dyadic_estimates_initial = [[1,0.3,-3],[0.2,0.6,2],[1/(d+1),1/2,3]]
   # Example 2: dyadic_estimates_initial = [[0.7,0.2,-4],[0.1,0.4,-2],[0.4,0.7,1],[0.3,0.2,6],[0.8,0.8,1],[0.8,0.2,-1]]
   # Example 3: dyadic_estimates_initial = [[1,0,(1-d)/2],[(d+3)/(2*(d+1)),1/2,1/2],[1,1/2,1/2]]
   d = sp.symbols('d')
   dyadic_estimates_initial = [[1,0,(1+d)/2],[0.7,0.7,-1]]


   ## Which additional estimates for T are known?
   ss_estimates_initial = []
   ws_estimates_initial = []
   sw_estimates_initial = [[0.3,0.1]]
   ww_estimates_initial = [[0.4,0.7]] 

   ## Which parameters d should be considered?
   d_list = [2,3]

   ## Are X and Y of finite measure?
   X_finite_measure = False
   Y_finite_measure = False

   ## Are all T_j selfadjoint? 
   selfadjoint = False
   
   input_variables = [
         view,
         dyadic_estimates_initial,
         ss_estimates_initial,
         ws_estimates_initial,
         sw_estimates_initial,
         ww_estimates_initial,
         d_list,
         selfadjoint, 
         X_finite_measure,
         Y_finite_measure
      ]    
   return input_variables


def log_uncaught_exceptions(exc_type, exc_value, exc_traceback):
   if issubclass(exc_type, KeyboardInterrupt):
      sys.__excepthook__(exc_type, exc_value, exc_traceback)
      return
   log.error("Ungefangene Exception: ",exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = log_uncaught_exceptions



def main(input_variables):
      
   view = input_variables[0]
   d_list = input_variables[6]
   selfadjoint = input_variables[7]    
   d = sp.symbols('d')
        
   mapping = {
         1: "ww, Weak-Type",
         2: "Lorentz",
         3: "ws, Weak-Strong",
         4: "sw, Strong-Weak",
         5: "ss, Lebesgue"
      }   

   log.info("################################################################")
   log.info("Start of main method!")         
   pdf_text = latexwriter.introtext(input_variables) 
   (dyadic_estimates,estimates) = inp.estimates(input_variables)
   log.info("This ends all symbolic computations. Proceed with special d-parameters.")     

   for D in d_list:       
      log.info("### D  = "+str(D)+" ###")      
      dyadic_estimates_D =  gen.reduce_dyadic_estimates(gen.rationalize(gen.plugin(D,dyadic_estimates)))
      log.info("dyadic_estimates_D = " + gen.toString(dyadic_estimates_D))
      estimates_D = gen.reduce_estimates(gen.rationalize(gen.plugin(D,estimates)))
      log.info("estimates_D = " + gen.toString(estimates_D))  
      endpoint_estimates_D = gen.reduce_estimates(inter.all_estimates(dyadic_estimates_D,estimates_D)) 
      log.info("Collect all resulting non-dyadic estimates.")      
      log.info("Here is the list of endpoint_estimates_D:")
      for est in endpoint_estimates_D: 
         log.info("Corner/endpoint estimate: " + gen.toString(est))
      for v in view:    
         log.info("### D  = "+str(D)+", view = "+str(v)+ "  ("+mapping.get(v) + ") ###")
         admissible_estimates_and_lines_DV = inter.admissible_estimates_and_lines(v,endpoint_estimates_D)
         log.info("The points and lines of the last step contain all information about the validity of the estimate along the boundary.")                       
         plotter.plot_to_jpg(v,D,admissible_estimates_and_lines_DV,dyadic_estimates_D,selfadjoint,files)              
         pdf_text += plotter.output_plot_and_text(v,D,admissible_estimates_and_lines_DV,files)       
         log.info("The Latex code for (view,d) =" + gen.toString((v,d)) + " is written.")      
   pdf_text += latexwriter.extrotext()
   log.info("The full Latex code is available. It will be used to produce the pdf file.")   
   plotter.print_and_plot_to_files(pdf_text,files)   
   
   print("\n Program finished succesfully! \n")
   log.info("Program finished succesfully!") 
   log.info("################################################################") 

   return




### MAIN PROGAM (manual) ###

## Here you can run your program without html page by inserting input_variables in create_input_data()
## input_variables = create_input_data()
## main(input_variables)
