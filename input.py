import general as gen
from pathlib import Path
import logging 
log = logging.getLogger("app")  


def check_view(view):
    if not isinstance(view,list): 
        return False
    else:
        return all([v in [1,2,3,4,5] for v in view])

def check_dlist(d_list):
    if not isinstance(d_list,list):
        return False
    else:
        return all([isinstance(d,float) or isinstance(d,int) for d in d_list])

def check_symmetric(symmetric):
    return (symmetric==True) or (symmetric==False)
 
    
## Dyadic Estimates should be as follows: [[A(d),B(d),\kappa_1(d)],[C(d),D(d),\kappa_2(d)],.] mit 0<=A(d)...<=1 for all d and \kappa_i(d) float
def check_dyadic_estimates(dyadic_estimates,dlist):        
    if not all([isinstance(est,list) for est in dyadic_estimates]):
        return False    
    if not all([len(est)==3 for est in dyadic_estimates]):
        return False         
    ## Check that the kappas are real numbers
    for D in dlist:       
        new_dyadic_estimates = gen.plugin(D,dyadic_estimates)                             
        try:
            if not all([est[2]<0 or est[2]>=0 for est in new_dyadic_estimates]):
                return False
        except:
            return False        
    ## Check that at least one kappa is negative
    for D in dlist:       
        new_dyadic_estimates = gen.plugin(D,dyadic_estimates)                             
        if  all([est[2]>=0 for est in new_dyadic_estimates]):
            log.warning("For at least one $d$ there is no dyadic estimate with negative kappa. So the given dyadic estimates do not provide anything helpful.")            
    return check_estimates([[est[0],est[1]] for est in dyadic_estimates],dlist)
         

## Estimates should be as follows: [[A(d),B(d)],[C(d),D(d)],[E(d),F(d)]] with 0<=A(d),...,F(d)<=1 for all d
def check_estimates(estimates,dlist):  
    if not all([isinstance(est,list) for est in estimates]):        
        return False
    if not all([len(est)==2 for est in estimates]):
        return False
    try:       
        for D in dlist:            
            estimates_d = gen.plugin(D,estimates)
            if not all([est[0]>= 0 and est[0]<=1 and est[1]>=0 and est[1]<=1 for est in estimates_d]):
                return False 
        return True
    except:
        return False 

def check_ss_estimates(estimates,dlist):   
    return check_estimates(estimates,dlist) 

def check_sw_estimates(estimates,dlist): 
    if not check_estimates(estimates,dlist): 
        return False 
    try:       
        for D in dlist:            
            estimates_d = gen.plugin(D,estimates)            
            if any([est[1]==0 for est in estimates_d]):
                log.error("Please label the estimate into L^{\infty,\infty} as estimate into L^\infty.")
                return False
        return True
    except:
        return False     

def check_ws_estimates(estimates,dlist):  
    if not check_estimates(estimates,dlist): 
        return False 
    try:       
        for D in dlist:            
            estimates_d = gen.plugin(D,estimates)            
            if any([est[0]==0 for est in estimates_d]):
                log.error("Please label the estimate from L^{1,1} as estimate from L^1.")
                return False
        return True
    except:
        return False     

def check_ww_estimates(estimates,dlist):   
    if not check_estimates(estimates,dlist): 
        return False 
    try:       
        for D in dlist:            
            estimates_d = gen.plugin(D,estimates)            
            if any([est[1]==0 for est in estimates_d]):
                log.error("Please label the estimate into L^{\infty,\infty} as estimate into L^\infty.")
                return False
            if any([est[0]==0 for est in estimates_d]):
                log.error("Please label the estimate from L^{1,1} as estimate from L^1.")
                return False
        return True
    except:
        return False     
 

def check(inputvariables):
 
    if len(inputvariables) != 10:
        return "Not the right number of input variables."
    if not all([inpvar!=None for inpvar in inputvariables]):
        return "Trivial input values."
    
    view = inputvariables[0]
    dyadic_estimates_initial = inputvariables[1]
    ss_estimates_initial = inputvariables[2] 
    ws_estimates_initial = inputvariables[3]
    sw_estimates_initial = inputvariables[4]
    ww_estimates_initial = inputvariables[5]
    d_list = inputvariables[6]
    symmetric = inputvariables[7] 
    X_finite_measure = inputvariables[8] 
    Y_finite_measure = inputvariables[9] 
    files = "interpolator"

    
    #print(inputvariables)
    log.info("### Input Data ###")        
    okay = True
    error = ""
    if not check_view(view):
        #print("A1a")
        error += r"Invalid input data: Views has to be a list consisting of 1,2,3,4,5." + "\n" 
        log.warning(error)        
        okay=False
    else:
        #print("A1b")
        log.info("Views: "+gen.toString(view)) 
    
    
    if not check_dlist(d_list):        
        #print("A2a")
        error += r"Invalid input data: d_list has to be a list of rational numbers." + "\n" 
        log.warning(error)        
        okay=False
    else:
        #print("A2b")
        log.info("d-list: "+gen.toString(d_list)) 
    
    
    if not check_dyadic_estimates(dyadic_estimates_initial,d_list):
        #print("A3a")
        error += r"Invalid input data: Dyadic estimates has to be a list [1/p_0,1/q_0,\kappa_0],[1/p_1,1/q_1,\kappa_1],... where p_0,p_1,q_0,q_1 \in [1,\infty] are symbolic expressions depending on d." + "\n"
        log.warning(error)        
        okay=False
    else:
        #print("A3b")
        log.info("Dyadic estimates: "+gen.toString(dyadic_estimates_initial))
    
    
    if not check_ss_estimates(ss_estimates_initial,d_list):
        #print("A4a")
        error += r"Invalid input data: Lebesgue estimates has to be a list  [1/p_0,1/q_0],[1/p_1,1/q_1],... where p_0,p_1,q_0,q_1 \in [1,\infty] are symbolic expressions depending on d." + "\n"
        log.warning(error)                
        okay=False
    else:
        #print("A4b")
        log.info("Lebesgue estimates: "+gen.toString(ss_estimates_initial))
    
    
    if not check_ws_estimates(ws_estimates_initial,d_list):
        #print("A5a")
        error += r"Invalid input data: Weak-Strong estimates has to be a list  [1/p_0,1/q_0],[1/p_1,1/q_1],... where p_0,p_1,q_0,q_1 \in [1,\infty] are symbolic expressions depending on d." + "\n"
        log.warning(error)        
        okay=False
    else:
        #print("A5b")
        log.info("Weak-Strong estimates: "+gen.toString(ws_estimates_initial))
    
    
    if not check_sw_estimates(sw_estimates_initial,d_list):
        #print("A6a")
        error += r"Invalid input data: Strong-Weak estimates has to be a list [1/p_0,1/q_0],[1/p_1,1/q_1],... where p_0,p_1,q_0,q_1 \in [1,\infty] are symbolic expressions depending on d." # "\n"
        log.warning(error)
        okay=False
    else:
        #print("A6b")
        log.info("Strong-Weak estimates: "+gen.toString(sw_estimates_initial))

    
    if not check_ww_estimates(ww_estimates_initial,d_list):
        #print("A7a")
        error += r"Invalid input data: Weak-type estimates has to be a list [1/p_0,1/q_0],[1/p_1,1/q_1],... where p_0,p_1,q_0,q_1 \in [1,\infty] are symbolic expressions depending on d." + "\n"
        log.warning(error)
        okay=False
    else:
        #print("A7b")
        log.info("Weak-type estimates: "+gen.toString(ww_estimates_initial))

    
    if len(dyadic_estimates_initial)+len(ss_estimates_initial)+len(ws_estimates_initial)+len(sw_estimates_initial)+len(ww_estimates_initial)<2:
        #print("A8")
        error += "Invalid input data: Please provide at least two estimates to interpolate." + "\n"
        log.warning(error)
        okay=False
 
    if symmetric and X_finite_measure != Y_finite_measure:
        #print("A9")
        error += "Invalid input data: For symmetric operators we must have X=Y, so both X,Y have finite measure or none. \n"
        log.warning(error)
        okay=False
    else:
        #print("A10")
        log.info("X_finite_measure: "+str(X_finite_measure))
        log.info("Y_finite_measure: "+str(Y_finite_measure))     
 
    if okay:        
        log.info("Input data was checked and appears to be correct.")   
        try:
            #print("A11")
            scriptdir = Path(__file__).resolve().parent
            folder = scriptdir / files
            # Ordner anlegen, falls er noch nicht existiert
            folder.mkdir(parents=True, exist_ok=True)
            log.info("Folder \""+files+"\" was successfully created.") 
        except:
            #print("A12")
            log.error("Attempt to create folder "+files+" failed.")
    else:
        print("A13")
        log.warning("Input data is not correct.")  
        log.warning(error)
        #log.info("Program is stopped due to incorrect input data.")
        #log.info("End of program! \n") 
        #log.info("################################################################")
        #exit()       
    return error


def estimates(inputvariables):
 
    if len(inputvariables) != 10:
        return False
    if not all([inpvar!=None for inpvar in inputvariables]):
        return False
    dyadic_estimates_initial = inputvariables[1]
    ss_estimates_initial = inputvariables[2] 
    ws_estimates_initial = inputvariables[3]
    sw_estimates_initial = inputvariables[4]
    ww_estimates_initial = inputvariables[5] 
    symmetric = inputvariables[7]
    X_finite_measure = inputvariables[8]   
    Y_finite_measure = inputvariables[9]
 
    if X_finite_measure:
        dyadic_estimates_initial += [[0,est[1],est[2]] for est in dyadic_estimates_initial if [0,est[1],est[2]] not in dyadic_estimates_initial]     
        ss_estimates_initial += [[0,est[1]]  for est in ss_estimates_initial if [0,est[1]] not in ss_estimates_initial]
        sw_estimates_initial += [[0,est[1]]  for est in sw_estimates_initial if [0,est[1]] not in sw_estimates_initial]
        ss_estimates_initial += [[0,est[1]]  for est in ws_estimates_initial if [0,est[1]] not in ss_estimates_initial]
        sw_estimates_initial += [[0,est[1]] for est in ww_estimates_initial if [0,est[1]] not in ww_estimates_initial] 
    if Y_finite_measure:
        dyadic_estimates_initial += [[est[0],1,est[2]] for est in dyadic_estimates_initial if [est[0],1,est[2]] not in dyadic_estimates_initial]     
        ss_estimates_initial += [[est[0],1]  for est in ss_estimates_initial if [est[0],1] not in ss_estimates_initial]
        ss_estimates_initial += [[est[0],1]  for est in sw_estimates_initial if [est[0],1] not in sw_estimates_initial]
        ws_estimates_initial += [[est[0],1]  for est in ws_estimates_initial if [est[0],1] not in ss_estimates_initial]
        ws_estimates_initial += [[est[0],1] for est in ww_estimates_initial if [est[0],1] not in ww_estimates_initial] 

    ## Prepare the user input: if the operators are symmetric then add the corresponding dual estimates.
    ## Indeed, \|T_jf\|_q\les 2^{-\kappa j}\|f\|_p  is then equivalent to \|T_jf\|_{p'}\les 2^{-\kappa j}\|f\|_{q'} 
    ## So estimates [1/p,1/q,kappa] induce estimates [1-1/q,1-1/p,kappa].
    if symmetric:
        dyadic_estimates_initial += [[1-est[1],1-est[0],est[2]] for est in dyadic_estimates_initial if [1-est[1],1-est[0],est[2]] not in dyadic_estimates_initial]     
        ss_estimates_initial += [[1-est[1],1-est[0]] for est in ss_estimates_initial if [1-est[1],1-est[0]] not in ss_estimates_initial]
        ws_estimates_initial += [[1-est[1],1-est[0]] for est in sw_estimates_initial if [1-est[1],1-est[0]] not in ws_estimates_initial]
        sw_estimates_initial += [[1-est[1],1-est[0]] for est in ws_estimates_initial if [1-est[1],1-est[0]] not in sw_estimates_initial]
        ww_estimates_initial += [[1-est[1],1-est[0]] for est in ww_estimates_initial if [1-est[1],1-est[0]] not in ww_estimates_initial] 
    
    estimates = []
    estimates += [[est[0],est[1],'ss'] for est in ss_estimates_initial]
    estimates += [[est[0],est[1],'ws'] for est in ws_estimates_initial]
    estimates += [[est[0],est[1],'sw'] for est in sw_estimates_initial]
    estimates += [[est[0],est[1],'ww'] for est in ww_estimates_initial] 

    log.info("### Conversion of the input data into two variables ###")
    log.info("dyadic estimates: "+gen.toString(dyadic_estimates_initial))
    log.info("estimates: "+gen.toString(estimates)) 

    return (dyadic_estimates_initial,estimates)