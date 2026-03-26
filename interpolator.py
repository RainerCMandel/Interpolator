from fractions import Fraction
import general as gen
import logging 
log = logging.getLogger(__name__)  

 
## This method transforms a given list of dyadic estimates \|T_jf\|_q\les 2^{\kappa j}\|f\|_p,
## encoded by [1/p,1/q,\kappa], into the list of endpoint estimates \|Tf\|_{?q?}\les \|f\|_{?p?}
## via Bourgain's method:
## In the typical case: [1/p_0,1/q_0,\kappa_0], [1/p_1,1/q_1,\kappa_1] with \kappa_0*\kappa_1<0
## yields an estimate L^{p_\theta,1}\to L^{q_\theta,\infty} where 
## (1-\theta)*\kappa_0+\theta*\kappa_1=0, 
## (1-\theta)*1/p_0 +\theta*1/p_1=1/p_\theta,
## (1-\theta)*1/q_0 +\theta*1/q_1=1/q_\theta 
## Such estimates are labeled 'ww'. 
## Case p_0=p_1: L^p instead of L^{p_0,1} and 's', else 'w'
## Case q_0=q_1: L^q instead of L^{q_0,\infty} and 's', else 'w'
## Estimates with \kappa=0 give rise to false estimates labeled 'f'.

def all_estimates(dyadic_estimates,estimates):    
    all_estimates = estimates  
    log.info("The given non-dyadic estimates:  estimates = "+gen.toString(estimates))      

    Z_indices = [i for i in range(len(dyadic_estimates)) if dyadic_estimates[i][2]==0]
    P_indices = [i for i in range(len(dyadic_estimates)) if dyadic_estimates[i][2]>0]    
    N_indices = [i for i in range(len(dyadic_estimates)) if dyadic_estimates[i][2]<0]                    
    all_estimates += [[dyadic_estimates[i][0],dyadic_estimates[i][1],'ss'] for i in N_indices]    
    # The dyadic estimates with kappa=0 can only be exploited if there is another one with kappa<0
    if N_indices != []:
        all_estimates += [[dyadic_estimates[i][0],dyadic_estimates[i][1],'f'] for i in Z_indices]      
    log.info("all estimates = " + gen.toString(all_estimates))
    # Apply Bourgain's interpolation method
    for i in P_indices:
        for j in N_indices:
            ## (1-theta)*dyadicestimates[i][2]+theta*dyadicestimates[j][2]=0
            theta = dyadic_estimates[i][2]/(dyadic_estimates[i][2]-dyadic_estimates[j][2])
            swf = 's' if dyadic_estimates[i][0] == dyadic_estimates[j][0] else 'w' 
            swf += 's' if dyadic_estimates[i][1] == dyadic_estimates[j][1] else 'w'             
            all_estimates.append([dyadic_estimates[i][0]*(1-theta)+dyadic_estimates[j][0]*theta,dyadic_estimates[i][1]*(1-theta)+dyadic_estimates[j][1]*theta,swf])          

    ## If the list of estimates contain estimates (1/p,1/q,swf1),(1/p,1/q,swf2) 
    ## then take the better one or combine them to a better one 
    all_estimates_merged = all_estimates    
    for est1 in all_estimates:                
        for est2 in all_estimates:                        
            if (est1[0] == est2[0] and est1[1]==est2[1] and est1[2]!=est2[2]):                
                swf1 = est1[2]
                swf2 = est2[2]
                ## If est1 is weaker that est2, then remove it. 
                if ((swf1=='f' and swf2!='f') or (swf1=='ww' and swf2!='f' and swf2!='ww') or (swf1=='ws' and swf2=='ss') or (swf1=='sw' and swf2=='ss')):                    
                    #all_estimates_merged = [est for est in all_estimates_merged if est!=est1] 
                    all_estimates_merged.remove(est1)
                ## If one estimate is weak-strong and the other strong-weak, create a new estimate labled 'swws'.    
                if ((swf1=='ws' and swf2=='sw') or (swf1=='sw' and swf2=='ws')):                                        
                    #all_estimates_merged = [est for est in all_estimates_merged if (est!=est1 or est!=est2)]+[[est2[0],est2[1],'swws']]         
                    all_estimates_merged.remove(est1,est2)
                    all_estimates_merged.append([est2[0],est2[1],'swws'])
    log.info("The estimates obtained by Bourgain's method are added to and merged with the given ones:  all_estimates_merged = "+gen.toString(all_estimates_merged))

    #for est in estimates:
    #    ## TODO Ist das fachlich korrekt? Nicht jede Strecke zwischen weak-type-estimates muss ss-estimates enthalten
    #    all_estimates_merged.append(est)

    
    def between(p,q):
        try: 
            x1, y1 = map(Fraction,p)
            x2, y2 = map(Fraction,q[0])
            x3, y3 = map(Fraction,q[1])
        except:
            print("Format-Fehler")
            exit()
        det = x1*(x2-y3)-y1*(x2-x3)+x2*y3-x3*y2
        return det == 0 and (x1-x2)*(x3-x1)>0 and (y1-y2)*(y3-y1)>0
    
    def better_interpolant(est,ests):
        try: 
            est0 = ests[0]
            est1 = ests[1]
        except:
            print("Format-Fehler")
            exit()        
        is_between = between([est[0],est[1]],[[est0[0],est0[1]],[est1[0],est1[1]]])
        is_better = est0[2]=='f' or est1[2]=='f' or est[2]=='ss' or (est[2]=='sw' and est[0]==est0[0] and est[0]==est1[0] and est0[2].startswith("w") and est1[2].startswith("w")) or (est[2]=='ws' and est[1]==est0[1] and est[1]==est1[1] and est0[2].endswith("w") and est1[2].endswith("w"))                    
        return is_between and is_better
    
    hull_estimates = gen.hull_estimates(all_estimates_merged)
    #log.info("all_estimates_merged"+gen.toString(all_estimates_merged))
    #log.info("hull_estimates"+gen.toString(hull_estimates))
    if len(hull_estimates) == 1:
        print("There are not enough estimates to get an interpolation result. End of program!")
        log.warning("There are not enough estimates to get an interpolation result. End of program!")
        exit()
    elif len(hull_estimates) == 2:
        print("There are only two estimates to get an interpolation result.")
        log.warning("There are only two estimates to get an interpolation result.")        
    else:
        log.info("Computing the complex hull the estimates can be reduced:  hull_estimates = "+gen.toString(hull_estimates))
        log.info("Check whether estimates on the boundary need to be readded to get optimal results.")
        ## TODO Einfügen der Randabschätzungen innerhalb eines Segments, wenn dadurch die Interpolationseigenschaften verbessert werden
        for i in range(len(all_estimates_merged)):
            est = all_estimates_merged[i]
            ## Finde eine Abschätzung auf dem Rand der konvexen Hülle, die nicht selbst Teil der definierenden Abschätzungen ist.
            ## Hierbei handelt es sich um solche Abschätzungen, die innerhalb eines Randsegments liegen.
            if est in gen.boundary_estimates(all_estimates_merged) and est not in hull_estimates:            
                for j in range(len(hull_estimates)):
                    hull_est1 = hull_estimates[j]
                    hull_est2 = hull_estimates[j+1] if j<len(hull_estimates)-1 else hull_estimates[0]
                    if between([est[0],est[1]],[[hull_est1[0],hull_est1[1]],[hull_est2[0],hull_est2[1]]]):
                        #log.info("The estimate "+gen.toString(est)+" is strictly between the two edges of the convex polygon: "+gen.toString(hull_est1)+" and "+gen.toString(hull_est2))
                        if better_interpolant(est,[hull_est1,hull_est2]):
                            ## est liegt zwischen hull_est1 und hull_est2 
                            ## Es bleibt zu prüfen, ob die Abschätzung aufgenommen werden sollte.                    
                            log.info("The estimate "+gen.toString(est)+" is better than the interpolated estimate of these two edges. So this estimate is added.")
                            hull_estimates.insert(j+1,est)
                        #else:
                        #    log.info("The estimate "+gen.toString(est)+" is not better than the interpolated esimate of these two edges. So this estimate is ignored.")
                    #else:
                    #    log.info("The estimate "+gen.toString(est)+" is not between the two edges of the convex polygon: "+gen.toString(hull_est1)+" and "+gen.toString(hull_est2))
        log.info("Check completed. The result is:   hull_estimate = "+gen.toString(hull_estimates))

    return hull_estimates
    
def admissible_estimates_and_lines(v,estimates):
    # Transform [[x0,y0,swf0],[x1,y1,swf1],...] into
    # pts = [[x0,y0,True],[x1,y1,False],...]  where True and False indicate whether the estimate itself is admissible
    # lines = [[pts[0],pts[1],True],[pts[1],pts[2],False],[pts[2],pts[3],False],...] open segment joining point0 and point1 is admissible
   
    def adm_swf(v,swf):                
        if v==1 and swf!='f': # ww estimates 
            return True
        elif v==2 and 'Lo' in swf: #Lorentz estimates 
            return True
        elif v==3 and ('ws' in swf or 'Lo' in swf or 'ss' in swf): #ws estimates 
            return True
        elif v==4 and ('sw' in swf or 'Lo' in swf or 'ss' in swf): #sw estimates 
            return True
        elif v==5 and 'ss' in swf: #Lebesgue estimates 
            return True
        else:
            return False
        
    def interpol_swf(est1,est2):
        if est1[2]=='f' or est2[2]=='f':
            return 'f'
        if 'ss' in est1[2] and 'ss' in est2[2]:  # complex interpolation
            if est1[0]!=est2[0] and est1[1]!=est2[1]:  # real interpolation           
                return 'ssLo'  
            else:
                return 'ss'
        elif est1[0]!=est2[0] and est1[1]!=est2[1]:   
            if est1[0]<est1[1] or est2[0]<est2[1]:
                return 'Lo'
            else:                
                return 'ssLo'
        elif est1[0]==est2[0] and est1[1]!=est2[1]:            
            if est1[2].startswith('w') or est2[2].startswith('w'):
                return 'ws'
            else: 
                return 'ss'            
        elif est1[0]!=est2[0] and est1[1]==est2[1]:
            if (est1[2].endswith('w') or est2[2].endswith('w')):
                return 'sw'
            else:
                return 'ss'
        else:
            return est1[2]
 

    def segment_hits_diagonal(est1,est2):
        x1=est1[0]
        y1=est1[1]
        x2=est2[0]
        y2=est2[1]
        if x1-y1-x2+y2 == 0:
            return (False,None)
        theta = (x1-y1)/(x1-y1-x2+y2)        
        x = (1-theta)*x1+theta*x2
        return (theta>0 and theta<1 and x>0 and x<1,x)

 
    if v in [1,2,3,4]:        
        pts = [[est[0],est[1],adm_swf(v,est[2])] for est in estimates]        
        log.info("points = "+gen.toString(pts))                        
        lines = []
        for i in range(len(estimates)):
            inext = i+1 if i<len(estimates)-1 else 0
            est1 = estimates[i]            
            est2 = estimates[inext] 
            if i<len(estimates)-1 or (i==len(estimates)-1 and len(estimates)>2):  
                lines.append([est1,est2,adm_swf(v,interpol_swf(est1,est2))])            
                log.info("Step "+str(i+1)+": treat the line joining "+gen.toString(est1)+" and "+gen.toString(est2))            
                log.info("--> lines = "+gen.toString(lines))
    if v==5:
        pts = []
        lines = []                      
        for i in range(len(estimates)):
            inext = i+1 if i<len(estimates)-1 else 0
            est1 = estimates[i]            
            est2 = estimates[inext]          
            ## Append the next point along with a True/False according to whether this point is admissible
            pts.append([est1[0],est1[1],adm_swf(v,est1[2])])

            ## A new line is only append if it is not the "way back" line between two estimates
            if not (i==len(estimates)-1 and len(estimates)==2):                         
                ## Append the next line along with a True/False according to whether the open segment is admissible.
                ## The admissibility is determined in interpol_swf                
                swf = interpol_swf(est1,est2)                     

                ## Now decide whether new boundary estimates need to be included. 
                # This is only the case if the two new lines have different validity and this is only the case if the "upper left" estimate is not of type ss.
                try: 
                    s = segment_hits_diagonal(est1,est2)                     
                except:
                    log.error("Problem in segment_hits_diagonal with estimates ",gen.toString(est1)," and ",gen.toString(est2))
                    exit()                
                if s[0] and 'Lo' in swf and not ((est1[0]<est1[1] and "ss" in est1[2]) or (est2[0]<est2[1] and "ss" in est2[2])):                                
                    new_est = [s[1],s[1],'ssLoA']
                    pts.append([new_est[0],new_est[1],adm_swf(v,new_est[2])])                
                    if est1[0]<est1[1]:
                        ## This is the case if est1 lies to the left of the diagonal                                        
                        if 'ss' in est1[2]:
                            lines.append([est1,new_est,adm_swf(v,'ssLo')])
                        else:
                            lines.append([est1,new_est,adm_swf(v,'Lo')])
                        lines.append([new_est,est2,adm_swf(v,'ssLo')]) 
                    else:
                        ## This is the case if est1 lies to the right of the diagonal                    
                        lines.append([est1,new_est,adm_swf(v,'ssLo')])
                        if 'ss' in est2[2]:
                            lines.append([new_est,est2,adm_swf(v,'ssLo')])                
                        else:
                            lines.append([new_est,est2,adm_swf(v,'Lo')])     
                elif (est1[0]<est1[1] and "ss" in est1[2]) or (est2[0]<est2[1] and "ss" in est2[2]): 
                    lines.append([est1,est2,True])                                                                  
                else:     
                    lines.append([est1,est2,adm_swf(v,interpol_swf(est1,est2))])            

            log.info("Step "+str(i+1)+": treat the point "+gen.toString(est1))
            log.info("--> points = "+gen.toString(pts))            
            log.info("Step "+str(i+1)+": treat the line joining "+gen.toString(est1)+" and "+gen.toString(est2))            
            log.info("--> lines = "+gen.toString(lines))
    return (pts,lines)            