import os

videos_path="/content/drive/MyDrive/videos/"


def get_frame_number(frame_name:str):
    return int(frame_name[5:])

def Sort_Tuple(tup): 
 
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of 
    # sublist lambda has been used 
    tup.sort(key = lambda x: x[3],reverse=True) 
    return tup



if __name__=="__main__":

    videos=os.listdir(videos_path)
    for video in videos:
        file="/content/drive/MyDrive/formatted/"+video+"/"+video+"_Objectness.txt"
        f=open(file,"r")
        all_frames=[]
        for line in f:
            if line!="0,0,0,0\n":
                splitted=line.split(" | ")
                all_frames.append(splitted[0])
        all_frames=set(all_frames)
        f.close()

        all_frames=sorted(all_frames,key=get_frame_number)

        f=open(file,"r")
        bbs={}
        for frame in all_frames:
            bbs[frame]=[]

        for bb in bbs:
            for line in f:
                if line!="0,0,0,0\n":
                    splitted=line.split(" | ")
                    splitted.append(float(splitted[2].split(",")[4]))
                    bbs[splitted[0]].append(tuple(splitted))
        f.close()

        for frame in all_frames:
            bbs[frame]=Sort_Tuple(bbs[frame])

        root="/content/drive/MyDrive/videos/"+video+"/color/"
        frame_number=len(os.listdir(root))

        output_file="/content/drive/MyDrive/formatted/"+video+"/"+video+"_Objectness_new.txt"
        os.system("touch "+output_file)

        g=open(output_file,"a")
        for i in range(1,frame_number+1):
            frame="frame"+str(i)
            if frame in all_frames:
                g.write(bbs[frame][0][0]+" | "+bbs[frame][0][1]+" | "+bbs[frame][0][2])
            else:
                g.write("0,0,0,0\n")
        g.close()
