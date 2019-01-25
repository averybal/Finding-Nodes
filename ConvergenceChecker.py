# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 13:55:18 2018

@author: avery
"""
import subprocess as sp
import os
import numpy as np
n = []
for i in range(15,300,10):
    n.append(i)
def NodeConvergenceChecker(alpha , reynold , airfoil , nodes):
    work_nodes = []
    alpha_out = []
    CL_out = []
    CD_out = []
    CDp_out = []
    CM_out = []
    TopXtr_out = []
    BotXtr_out = []
    for i in nodes:
        ps = sp.Popen(['xfoil.exe'],
                  stdin = sp.PIPE) 
        node_file = str.join("",[airfoil,"with",str(i),"Nodes.dat"])
        inst = str.join('\n', [str.join("",["load ",airfoil,".dat"]),
                                               "ppar",
                                               "N",
                                               str(i),
                                               "",
                                               "",
                                               "oper",
                                               str.join("",["v ",reynold]),
                                               "pacc",
                                               node_file,
                                               "",
                                               str.join("",["alfa ",alpha]),
                                               "pacc",
                                               "v",
                                               ""])
        print(str(i))        
        ps.communicate(inst.encode())
        f = open(node_file,"r")
        fl = f.readlines()
        if len(fl) != 13:
            print(str.join(" ",["Analysis Did Not Converge for",str(i),"Nodes"]))
        else:
            work_nodes.append(i)
            fln = np.genfromtxt([fl[12].encode()])
            alpha_out.append(fln[0])
            CL_out.append(fln[1])
            CD_out.append(fln[2])
            CDp_out.append(fln[3])
            CM_out.append(fln[4])
            TopXtr_out.append(fln[5])
            BotXtr_out.append(fln[6])
        f.close()
        os.remove(node_file)
    print("Analysis converged for the following nodes: ",work_nodes)
    return work_nodes, alpha_out, CL_out, CD_out, CDp_out, CM_out, TopXtr_out, BotXtr_out

def ReConvergenceChecker(alpha , reynold , airfoil):
    work_re = []
    for i in reynold:
        ps = sp.Popen(['xfoil.exe'],
                  stdin = sp.PIPE) 
        node_file = str.join("",[airfoil,"with",str(i),"Re.dat"])
        inst = str.join('\n', [str.join("",["load ",airfoil,".dat"]),
                                               "oper",
                                               str.join("",["v ",str(i)]),
                                               "pacc",
                                               node_file,
                                               "",
                                               str.join("",["alfa ",alpha]),
                                               "pacc",
                                               "v",
                                               ""])
        print(str(i))        
        ps.communicate(inst.encode())
        f = open(node_file,"r")
        fl = f.readlines()
        if len(fl) != 13:
            print(str.join(" ",["Analysis Did Not Converge for Re =",str(i)]))
        else:
            work_re.append(i)
        f.close()
        os.remove(node_file)
    print("Analysis converged for the following Reynolds Numbers: ",work_re)
    return work_re

Result = NodeConvergenceChecker('0','3e7','Aquila',n)
work_nodes = Result[0]
alpha = Result[1]
CL_out = Result[2]
CD_out = Result[3]
CDp_out = Result[4]
CM_out = Result[5]
TopXtr_out = Result[6]
BotXtr_out = Result[7]