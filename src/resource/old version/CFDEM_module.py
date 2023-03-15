from data import *
from document import *
import subprocess

class CFDEM_file():
    def initialize(self,template,target):
        self.template=template
        self.target=target
        self.document=document()
        self.document.read_template(template)
        
    def set_parameter(self,parameter,value):
        self.document.substitute(parameter,value)
        
    def output(self):
        self.document.output_document(self.target)
        
class CFDEM():
    def DEM_initialize(self):
        self.DEM_init=CFDEM_file()
        self.DEM_init.initialize("template/liggghts_init_template.txt","CFDEM/DEM/liggghts_init.txt")
        self.DEM_run=CFDEM_file()
        self.DEM_run.initialize("template/liggghts_run_template.txt","CFDEM/DEM/liggghts_run.txt")
        
        initialize_file="csv_file/DEM_initialization.csv"
        tmp1=csv_input(initialize_file)
        for i in range(len(tmp1)-1):
            key_word="<"+tmp1[i+1][0]+">"
            value=tmp1[i+1][2]
            self.DEM_init.set_parameter(key_word,value)
            self.DEM_run.set_parameter(key_word,value)
            
    def DEM_set_radius(self,radius,fraction):
        self.DEM_radius=radius
        self.DEM_fraction=fraction
        
        # remove the original size distribution
        for i in range(len(self.DEM_init.document.file)):
            tmp1=self.DEM_init.document.file[i].split()
            if len(tmp1)<2:
                pass
            elif tmp1[1]=="pts1":
                self.DEM_init.document.file.pop(i)
                self.DEM_init.document.file.pop(i)
                index=i
                break
        
        # read the prime table
        file="csv_file/prime_table.csv"
        prime=csv_input(file)    
        
        # generate the particle template
        for i in range(len(radius)):
            new_line="fix pts"+str(i+1)+" all particletemplate/sphere "+str(prime[i][0])+" atom_type 1 density constant ${DEM_density} radius constant "+str(radius[i])+" \n"
            self.DEM_init.document.file.insert(index+i,new_line)
        
        # generate the particle distribution
        new_line="fix pdd all particledistribution/discrete/massbased 32452843 "+str(len(radius))
        for i in range(len(fraction)):
            new_line=new_line+" pts"+str(i+1)+" "+str(fraction[i])
        new_line=new_line+" \n"
        self.DEM_init.document.file.insert(index+len(radius),new_line) 
            
    def DEM_output(self):
        self.DEM_init.output()
        self.DEM_run.output()
        
    def DEM_run(self):
        subprocess.run(["/bin/bash","script/DEM_run.txt"])
        
    def CFDEM_initialize(self):
        initialize_file="csv_file/CFDEM_initialization.csv"
        tmp1=csv_input(initialize_file)
        self.CFDEM_file=[]
        for i in range(len(tmp1)-1):
            template="template/"+tmp1[i+1][3]
            target="CFDEM/CFD/"+tmp1[i+1][4]
            key_word="<"+tmp1[i+1][0]+">"
            value=tmp1[i+1][2]
            
            overlap=0
            index=-1
            if len(self.CFDEM_file)>0:
                for j in range(len(self.CFDEM_file)):
                    if template==self.CFDEM_file[j].template:
                        overlap=1
                        index=j
                        
            if overlap==0:
                tmp2=CFDEM_file()
                tmp2.initialize(template,target)
                tmp2.set_parameter(key_word,value)
                self.CFDEM_file.append(tmp2)
            elif overlap==1:
                self.CFDEM_file[index].set_parameter(key_word,value)
    
    def CFDEM_output(self):
        for i in range(len(self.CFDEM_file)):
            self.CFDEM_file[i].output()
    
    def CFDEM_run(self):
        subprocess.run(["/bin/bash","script/CFDEM_run.txt"])
                