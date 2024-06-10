import os
import shutil
gmname=input(r"Enter Game Name:")
imgspth=input(r"Enter Images Path(full path):")
images=os.listdir(imgspth)
gmimages=[]
for image in images:
    if gmname in image:
        gmimages.append(image)
images=gmimages
length=len(images) / 2
trainp="0.45"
validp="0.45"
testp="0.10"
trainf=length*float(trainp)
validf=length*float(validp)
testf=length*float(testp)
if type(trainf) == float:
    trainf=int(trainf-1)
print(f"Train Images:{trainf}")
if type(validf) == float:
    validf=int(validf-1)
print(f"Valid Images:{validf}")
if type(testf) == float:
    testf=int(testf-1)
print(f"Test Images:{testf}")
print("Left Images:"+str(length-round(trainf+validf+testf)))
trainf2=trainf
validf2=validf
testf2=testf
try:
    os.mkdir("train")
    os.mkdir(r"train\images")
    os.mkdir(r"train\labels")
    os.mkdir("test")
    os.mkdir(r"test\images")
    os.mkdir(r"test\labels")
    os.mkdir("valid")
    os.mkdir(r"valid\images")
    os.mkdir(r"valid\labels")
except:
    shutil.rmtree("train")
    shutil.rmtree("test")
    shutil.rmtree("valid")
    os.mkdir("train")
    os.mkdir(r"train\images")
    os.mkdir(r"train\labels")
    os.mkdir("test")
    os.mkdir(r"test\images")
    os.mkdir(r"test\labels")
    os.mkdir("valid")
    os.mkdir(r"valid\images")
    os.mkdir(r"valid\labels")
for image in gmimages:
    image=imgspth+"\\"+image
    if gmname in image and image.endswith(".png"):
        if len(os.listdir(r"train\images")) != trainf:
            shutil.copy(image,r"train\images")
        elif len(os.listdir(r"valid\images")) != validf:
            shutil.copy(image,r"valid\images")
        elif len(os.listdir(r"test\images")) != testf:
            shutil.copy(image,r"test\images")
    elif gmname in image and image.endswith(".txt"):
        if len(os.listdir(r"train\labels")) != trainf:
            shutil.copy(image,r"train\labels")
        elif len(os.listdir(r"valid\labels")) != validf:
            shutil.copy(image,r"valid\labels")
        elif len(os.listdir(r"test\images")) != testf:
            shutil.copy(image,r"test\labels")
print("Creating data.yaml")
try:
    namespth=imgspth.replace(imgspth.split("\\")[-1],"")+gmname+".names"
    print("Names File Path ="+namespth)
    names=open(namespth,"r")
    names=[line.rstrip() for line in names]
    datay=rf"""
train: {os.getcwd()}\train\images
val: {os.getcwd()}\valid
test: {os.getcwd()}\test\images

nc: 1
names: {names}

roboflow:
  workspace: yolo-rl65m
  project: yolofinder
  version: 1
  license: CC BY 4.0
  url: https://universe.roboflow.com/yolo-rl65m/yolofinder/dataset/1
"""
    open(os.getcwd()+"\\data.yaml","w").writelines(datay)
except:
    print("Either Skill Issue or No .Names File in The Path You Gave")
print("Done Saved Files")
try:
  ytrainyn=input("Do you want to Train the yolo model(Yes or No)?:")
  if ytrainyn== "Yes":
    epochsn=int(input("Enter Epochs Number(Enter Without Numbers=100)(4000 for best detections):"))
    if epochsn == "":
        epochsn=100
    open("trainer.bat","w").write(f"yolo task=detect mode=train model=yolov8m.pt imgsz=640 data=data.yaml epochs={epochsn} batch=-1 name=yolov8m_custom")
    import subprocess
    subprocess.run("trainer.bat", shell=True)
except:
    print("How Did you make an error?")
    exit()

