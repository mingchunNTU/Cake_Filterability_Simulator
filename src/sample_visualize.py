import os 


#######################################################
# setting_dir="../examples/non-uniform/"
setting_dir="../examples/non-uniform/restart/"


sample_width= 171
sample_height= 400
iteration= 160000
time_step= 10000

#######################################################

Result_dir=setting_dir+"Result/vtk_file/"
for fname in os.listdir(Result_dir):
	if fname.startswith("sample"):
		os.remove(os.path.join(Result_dir,fname))

number=int(iteration/time_step)

for i in range(number):
	path=setting_dir+"Result/vtk_file/sample_region_"+str(int((i+1)*time_step))+".vtk"
	f=open(path,"w")
	f.write("# vtk DataFile Version 4.0 "+"\n")
	f.write("Generated by LIGGGHTS"+"\n")
	f.write("ASCII"+"\n")
	f.write("DATASET RECTILINEAR_GRID"+"\n")
	f.write("DIMENSIONS 2 2 2"+"\n")
	f.write("X_COORDINATES 2 double"+"\n")
	f.write(str(-1*sample_width)+" "+str(sample_width)+"\n")
	f.write("Y_COORDINATES 2 double"+"\n")
	f.write(str(-1*sample_width)+" "+str(sample_width)+"\n")
	f.write("Z_COORDINATES 2 double"+"\n")
	f.write("0 "+str(sample_height)+"\n")
	f.close()
