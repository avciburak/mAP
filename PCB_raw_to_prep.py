import os

results_path="/content/drive/MyDrive/results/"
formatted_path="/content/drive/MyDrive/formatted/"

                
if __name__=="__main__":

    files=os.listdir(results_path)
    result_files=[]
    names_and_files={}
    for file in files:
        file_name=file.split(".")[0]
        result_files.append(file_name.split("_")[1])

    for name,file in zip(result_files,files):
        names_and_files[name]=file

    formatted_folders=os.listdir(formatted_path)

    for folder in formatted_folders:
        os.system("rm -r "+formatted_path+folder)

    for file in result_files:
        os.system("mkdir "+formatted_path+file)

    for file in result_files:
        g=open(formatted_path+file+"/"+file+"_PCB.txt","w")
        g.close()
    


    for file in result_files:
        f=open(results_path+names_and_files[file],"r")
        g=open(formatted_path+file+"/"+file+"_PCB.txt","a")
        for line in f:
            if line[0]!="0":
                splitted=line.split(",")
                g.write("frame"+splitted[0]+
                        " | "+"bb.jpg"+" | "+
                        splitted[1]+","+
                        splitted[2]+","+
                        str(float(splitted[1])+float(splitted[3]))+","+
                        str(float(splitted[2])+float(splitted[4]))+","+
                        splitted[5]+"\n")
            else:
                g.write("0,0,0,0\n")        
        f.close()
        g.close()
