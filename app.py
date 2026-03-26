from flask import Flask, session, redirect, render_template, request, send_file
import general as gen
import main
import input as inp 
from pathlib import Path

import logging 

global script_dir  
scriptdir = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = "super_secret_key"
logging.basicConfig(
      filename= scriptdir / "interpolator.log",
      filemode="w",
      level=logging.INFO,
      # Es gibt: DEBUG, INFO, WARNING, ERROR, CRITICAL
      format="%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(funcName)s() - %(name)s - %(message)s"
   )
log = logging.getLogger(__name__)  


def translate_inputvariables(input_variables):
    # Extract each single input variable
    view=input_variables[0]
    dyadic_estimates_initial=input_variables[1]
    ss_estimates_initial=input_variables[2]
    ws_estimates_initial=input_variables[3]
    sw_estimates_initial=input_variables[4]
    ww_estimates_initial=input_variables[5]
    d_list=input_variables[6]
    symmetric=input_variables[7]
    files=input_variables[8]
    X_finite_measure=input_variables[9]
    Y_finite_measure = input_variables[10]
        
    ## symmetric, X_finite_measure, Y_finite_measure are autmatically boolean --> no conversion necessary
    
    try:    
        if view is None or view.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_view = [5]            
            log.warning("No input for 'view'. We proceed with view = [5].")   
        else:
            new_view = [int(x) for x in view.split(",")]             
    except:        
        new_view = view
        log.warning("Input for 'view' is not valid. Please correct this.")   
    #print(new_view)

    try:
        if d_list is None or d_list.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_d_list = [2]            
            log.warning("No input for 'd_list'.  We proceed with d_list = [2].")   
        else:
            new_d_list = [int(x) for x in d_list.split(",")]
    except:
        new_d_list = d_list
        log.warning("Input for d_list is not valid. Please correct this.")
    #print(new_d_list)
    
    
    
    if files is None or files.lstrip("[']").rstrip("']").replace(" ","")=="":
        new_files = "dummy"
        log.warning("No input for 'files'. We proceed with files='dummy'.")
    else:
        new_files = files.lstrip("[']").rstrip("']").replace(" ","")
    #print(new_files)
         
    #print(dyadic_estimates_initial)
    try:
        if dyadic_estimates_initial is None or dyadic_estimates_initial.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_dyadic_estimates_initial = []
        else:            
            new_dyadic_estimates_initial = gen.parse_triplets(dyadic_estimates_initial)    
    except:
        new_dyadic_estimates_initial = []
        log.warning("Input for dyadic_estimates is not valid. We proceed with Dyadic Estimates = [].")
    #print(new_dyadic_estimates_initial)        
    
    try:
        if ss_estimates_initial is None or ss_estimates_initial.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_ss_estimates_initial = []
        else:            
            new_ss_estimates_initial = gen.parse_pairs(ss_estimates_initial)   
    except:
        new_ss_estimates_initial = []
        log.warning("Input for Lebesgue estimates is not valid. We proceed with Lebesgue estimates = [].")
    #print(new_ss_estimates_initial)

    try:
        if ww_estimates_initial is None or ww_estimates_initial.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_ww_estimates_initial = []
        else:            
            new_ww_estimates_initial = gen.parse_pairs(ww_estimates_initial)   
    except:
        new_ww_estimates_initial = []
        log.warning("Input for Weak-type estimates is not valid. We proceed with Wak-type estimates = [].")
    #print(new_ww_estimates_initial)

    try:
        if ws_estimates_initial is None or ws_estimates_initial.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_ws_estimates_initial = []
        else:            
            new_ws_estimates_initial = gen.parse_pairs(ws_estimates_initial)   
    except:
        new_ws_estimates_initial = []
        log.warning("Input for Weak-Strong estimates is not valid. We proceed with Weak-Strong estimates = [].")
    #print(new_ws_estimates_initial)

    try:
        if sw_estimates_initial is None or sw_estimates_initial.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_sw_estimates_initial = []
        else:            
            new_sw_estimates_initial = gen.parse_pairs(sw_estimates_initial)   
    except:
        new_sw_estimates_initial = []
        log.warning("Input for Strong-Weak estimates is not valid. We proceed with Strong-Weak estimates = [].")
    #print(new_sw_estimates_initial)
    
    new_input_variables = [
        new_view,
        new_dyadic_estimates_initial,
        new_ss_estimates_initial,
        new_ws_estimates_initial,
        new_sw_estimates_initial,
        new_ww_estimates_initial,
        new_d_list,
        symmetric,
        new_files,
        X_finite_measure,
        Y_finite_measure    
    ]

    return new_input_variables

def default_inputvariables(input_variables):
    # Extract each single input variable
    view=input_variables[0]
    dyadic_estimates_initial=input_variables[1]
    ss_estimates_initial=input_variables[2]
    ws_estimates_initial=input_variables[3]
    sw_estimates_initial=input_variables[4]
    ww_estimates_initial=input_variables[5]
    d_list=input_variables[6]
    symmetric=input_variables[7] 
    X_finite_measure=input_variables[8]
    Y_finite_measure = input_variables[9] 

    if view == []: 
        new_view = [5]            
        log.warning("The input data for 'view' was empty. We proceed with view = [5].")   
    else:
        new_view = view 

    if d_list == []:
        new_d_list = [2]            
        log.warning("The input data for 'd_list' was empty. We proceed with d_list = [2].")   
    else:
        new_d_list = d_list
            
    new_input_variables = [
        new_view,
        dyadic_estimates_initial,
        ss_estimates_initial,
        ws_estimates_initial,
        sw_estimates_initial,
        ww_estimates_initial,
        new_d_list,
        symmetric, 
        X_finite_measure,
        Y_finite_measure    
    ]

    return new_input_variables


def clear_inputvariables(input_variables):
    # Extract each single input variable
    view=input_variables[0]
    dyadic_estimates_initial=input_variables[1]
    ss_estimates_initial=input_variables[2]
    ws_estimates_initial=input_variables[3]
    sw_estimates_initial=input_variables[4]
    ww_estimates_initial=input_variables[5]
    d_list=input_variables[6]
    symmetric=input_variables[7] 
    X_finite_measure=input_variables[8]
    Y_finite_measure = input_variables[9]
    err_text = "" 

    try:    
        if view is None or view.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_view = []            
            log.warning("No input for 'view'.")   
        else:
            new_view = [int(x) for x in view.split(",")]    
            log.info("Input: view = "+str(new_view))         
    except:        
        new_view = []
        err_text += "Input for 'view' is not valid."
        log.warning("Input for 'view' is not valid.")   
    #print(new_view)

    try:
        if d_list is None or d_list.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_d_list = []            
            log.warning("No input for 'd_list'.")   
        else:
            new_d_list = [int(x) for x in d_list.split(",")]
            log.info("Input: d_list = "+str(new_d_list))         
    except:
        new_d_list = []
        err_text += "Input for d_list is not valid."
        log.warning("Input for d_list is not valid.")
    #print(new_d_list)
             
    #print(dyadic_estimates_initial)
    try:
        if dyadic_estimates_initial is None or dyadic_estimates_initial.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_dyadic_estimates_initial = []              
        else:            
            new_dyadic_estimates_initial = gen.parse_triplets(dyadic_estimates_initial)    
            log.info("Input: dyadic_estimates = "+str(new_dyadic_estimates_initial))         
    except:
        new_dyadic_estimates_initial = []
        err_text += "Input for dyadic_estimates is not valid."
        log.warning("Input for dyadic_estimates is not valid.")
    #print(new_dyadic_estimates_initial)        
    
    try:
        if ss_estimates_initial is None or ss_estimates_initial.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_ss_estimates_initial = []
        else:            
            new_ss_estimates_initial = gen.parse_pairs(ss_estimates_initial)  
            log.info("Input: ss_estimates = "+str(new_ss_estimates_initial))   
    except:
        new_ss_estimates_initial = []
        err_text += "Input for Lebesgue estimates is not valid."
        log.warning("Input for Lebesgue estimates is not valid.")
    #print(new_ss_estimates_initial)

    try:
        if ww_estimates_initial is None or ww_estimates_initial.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_ww_estimates_initial = []
        else:            
            new_ww_estimates_initial = gen.parse_pairs(ww_estimates_initial)               
            log.info("Input: ww_estimates = "+str(new_ww_estimates_initial))  
    except:
        new_ww_estimates_initial = []
        err_text += "Input for Weak-type estimates is not valid."
        log.warning("Input for Weak-type estimates is not valid.")
    #print(new_ww_estimates_initial)

    try:
        if ws_estimates_initial is None or ws_estimates_initial.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_ws_estimates_initial = []
        else:            
            new_ws_estimates_initial = gen.parse_pairs(ws_estimates_initial)   
            log.info("Input: ws_estimates = "+str(new_ws_estimates_initial))  
    except:
        new_ws_estimates_initial = []
        err_text += "Input for Weak-Strong estimates is not valid."
        log.warning("Input for Weak-Strong estimates is not valid.")
    #print(new_ws_estimates_initial)

    try:
        if sw_estimates_initial is None or sw_estimates_initial.lstrip("[']").rstrip("']").replace(" ","")=="":
            new_sw_estimates_initial = []
        else:            
            new_sw_estimates_initial = gen.parse_pairs(sw_estimates_initial)   
            log.info("Input: sw_estimates = "+str(new_sw_estimates_initial))  
    except:
        new_sw_estimates_initial = []
        err_text += "Input for Strong-Weak estimates is not valid."
        log.warning("Input for Strong-Weak estimates is not valid.")
    #print(new_sw_estimates_initial)
    
    cleared_input_variables = [
        new_view,
        new_dyadic_estimates_initial,
        new_ss_estimates_initial,
        new_ws_estimates_initial,
        new_sw_estimates_initial,
        new_ww_estimates_initial,
        new_d_list,
        symmetric, 
        X_finite_measure,
        Y_finite_measure    
    ]

    return (cleared_input_variables,err_text)


@app.route("/readme")
def readme():
    return send_file("readme.txt",mimetype="text/plain")


@app.route("/", methods=["GET", "POST"])
def index():     

    error_text = ""
          
    if request.method == "POST" and request.form.get("action") == "run": 
        
        log.info("################################################################")
        log.info("Start of program!")          
        
        view = request.form.get("view")
        dyadic_estimates_initial = request.form.get("dyadic_estimates_initial")
        ss_estimates_initial = request.form.get("ss_estimates_initial")
        ws_estimates_initial = request.form.get("ws_estimates_initial")
        sw_estimates_initial = request.form.get("sw_estimates_initial")
        ww_estimates_initial = request.form.get("ww_estimates_initial")
        d_list = request.form.get("d_list")
        symmetric = "symmetric" in request.form
        X_finite_measure = "X_finite_measure" in request.form
        Y_finite_measure = "Y_finite_measure" in request.form        
        input_variables = [
            view,
            dyadic_estimates_initial,
            ss_estimates_initial,
            ws_estimates_initial,
            sw_estimates_initial,
            ww_estimates_initial,
            d_list,
            symmetric, 
            X_finite_measure,
            Y_finite_measure
        ]              
        files = "interpolator"
                      
        try:            
            #new_input_variables = translate_inputvariables(input_variables)

            #print(str(input_variables))
            #print("1st errortext = " + error_text)
            log.info("Work with the input = "+gen.toString(input_variables))
            (cleared_input_variables,err_text) = clear_inputvariables(input_variables)                        
            #print(cleared_input_variables)
            log.info("After input clearing the input reads = "+gen.toString(cleared_input_variables))
            #print("2nd errortext = " + error_text)
            error_text += err_text
            new_input_variables = default_inputvariables(cleared_input_variables)                                    
            #print(new_input_variables)
            log.info("After inserting default values if necessary the input reads = "+gen.toString(new_input_variables))
            #print("3rd errortext = " + error_text)
            error_text += inp.check(new_input_variables)             
            #print("4th errortext = " + error_text)             
            
            if error_text != "":
                #print("B")
                log.info("Input error: no computation started.")                
                log.info("Error text = "+error_text)   
                #print(cleared_input_variables[2])
                #print(gen.toString(cleared_input_variables[2])[1:-1].replace(" ",""))
                return render_template("index.html", 
                                       error = error_text,
                                       view = cleared_input_variables[0][1:-1].replace(" ",""),
                                       dyadic_estimates_initial = gen.toString(cleared_input_variables[1])[1:-1].replace(" ",""),
                                       ss_estimates_initial = gen.toString(cleared_input_variables[2])[1:-1].replace(" ",""),
                                       ws_estimates_initial = gen.toString(cleared_input_variables[3])[1:-1].replace(" ",""),
                                       sw_estimates_initial = gen.toString(cleared_input_variables[4])[1:-1].replace(" ",""),
                                       ww_estimates_initial = gen.toString(cleared_input_variables[5])[1:-1].replace(" ",""),
                                       d_list = cleared_input_variables[6][1:-1].replace(" ",""),
                                       symmetric = cleared_input_variables[7],                                       
                                       X_finite_measure = cleared_input_variables[8],
                                       Y_finite_measure = cleared_input_variables[9])  
            
            try:                
                log.info("### Main method is started.")    
                main.main(new_input_variables)
                log.info("### Main method has been left.")                                     
                log.info("The pdf file will be written to " + files + "/" + files+".pdf") 
                error_text = ""               
                return send_file(files + "/" + files+".pdf",mimetype="application/pdf",as_attachment=False)                            
            except Exception:                
                error_text +=  "Error while executing the main method." 
                log.exception("Error while executing the main method.")
                raise
        except:         
            #print("E")                   
            error_text += "Input error: no computation started."
            log.exception("Input error: no computation started.")
                                         
        
        return render_template("index.html",error = error_text,
                           view = view,
                           dyadic_estimates_initial = dyadic_estimates_initial,
                            ss_estimates_initial = ss_estimates_initial,
                            ws_estimates_initial = ws_estimates_initial,
                            sw_estimates_initial = sw_estimates_initial,
                            ww_estimates_initial = ww_estimates_initial,
                            d_list = d_list,
                            symmetric = symmetric, 
                            X_finite_measure = X_finite_measure,
                            Y_finite_measure = Y_finite_measure)
     
    return render_template("index.html",error = error_text)

app.run(host="0.0.0.0", port=10000)

## [0.3,0.3,-1],[0.4,0.8,-3],[0,0.4,2]
     
