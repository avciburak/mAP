import os

videos_path="/content/drive/MyDrive/videos/"
mAP_path="/content/Object-Detection-Metrics/"
detect_root="/content/drive/MyDrive/final_results/"
#finalscore_mAP_result_path="/content/FinalScore_mAP_results.txt"



#IoU function
def IoU(boxA, boxB):
# determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
# compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
# compute the area of both the prediction and ground-truth
# rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
# compute the intersection over union by taking the intersection
# area and dividing it by the sum of prediction + ground-truth
# areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
# return the intersection over union value
    return iou



if __name__== "_main_":

    videos=os.listdir(videos_path)


    for file in os.listdir(mAP_path+"/groundtruths/"):
        os.remove(mAP_path+"/groundtruths/"+file)
    for file in os.listdir(mAP_path+"/detections/"):
        os.remove(mAP_path+"/detections/"+file)

    #results_file=open(finalscore_mAP_result_path,"a")
    #results_file.write(" ____________________________________________________________________\n")
    #results_file.write("|*video            |   AP(%50)   |   FN   |   GT   |   BB   |   TP   |\n")
    #results_file.write("|------------------|-------------|--------|--------|--------|--------|\n")


    for video in videos:

    
        frame_number=len(os.listdir(videos_path+video+"/color/"))

        for i in range(1,frame_number+1):
            file=open(mAP_path+"/groundtruths/frame"+str(i)+".txt","w")
            file.close()
        for i in range(1,frame_number+1):
            file=open(mAP_path+"/detections/frame"+str(i)+".txt","w")
            file.close()

        with open(videos_path+video+"/groundtruth.txt","r") as f:
            i=1
            for line in f:
                if "nan" not in line:
                    splitted=line.split(",")
                    file=open(mAP_path+"/groundtruths/frame"+str(i)+".txt","a")
                    file.write(video+" "+
                               splitted[0]+" "+
                               splitted[1]+" "+
                               str(float(splitted[0])+float(splitted[2]))+" "+
                               str(float(splitted[1])+float(splitted[3]))+"\n\n")
                    file.close()
                i+=1

        with open(detect_root+video+"/"+video+"_FinalScore_new.txt","r") as f:
            for line in f:
                if "0,0,0,0" not in line:
                    splitted_raw=line.split(" | ")[2]
                    frame_no_str=line.split(" | ")[0][5:]
                    splitted=splitted_raw.split(",")
                    file=open(mAP_path+"/detections/frame"+frame_no_str+".txt","a")
                    file.write(video+" "+
                               splitted[4].split("\n")[0]+" "+
                               splitted[0]+" "+
                               splitted[1]+" "+
                               splitted[2]+" "+
                               splitted[3]+"\n\n")
                    file.close()


        gts={}
        with open(videos_path+video+"/groundtruth.txt","r") as f:
            i=1
            for line in f:
                if "nan" not in line:
                    splitted=line.split(",")
                    gts["frame"+str(i)]=[float(splitted[0]),float(splitted[1]),float(splitted[0])+float(splitted[2]),float(splitted[1])+float(splitted[3])]
                i+=1


        bbs={}
        with open(detect_root+video+"/"+video+"_FinalScore_new.txt","r") as f:
            i=1
            for line in f:
                if "0,0,0,0" not in line:
                    splitted_raw=line.split(" | ")[2]
                    splitted=splitted_raw.split(",")
                    bbs["frame"+str(i)]=[float(splitted[0]),float(splitted[1]),float(splitted[2]),float(splitted[3])]
                i+=1


        print("Video Name: "+video)
        print("Video Frame Number: "+frame_number)
        print("Video Groundtruth Number: "+len(list(gts.keys())))

        keys=list(gts.keys())
        ious=[]
        for key in keys:
            if key in bbs:
                ious.append(IoU(bbs[key],gts[key]))

        print("Video Total Bounding Box Number: "+len(ious))

        TP=0
        for iou in ious:
            if iou>=0.5:
                TP+=1
        print("Video 0.5 IoU. Number of True Positives: "+TP)

        TP=0
        for iou in ious:
            if iou>=0.75:
                TP+=1
        print("Video 0.75 IoU. Number of True Positives: "+TP)

        os.system("python pascalvoc.py -detformat xyrb -gtformat xyrb")
        os.system("python pascalvoc.py -detformat xyrb -gtformat xyrb -t 0.75")

        #results_file.write(" ____________________________________________________________________")
        #results_file.write("|"+video+"           |      |   "+frame_number+"   |   "+len(list(gts.keys()))+"   |   "+ious+"   |   "+TP+"   |")

        





