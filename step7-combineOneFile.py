import glob, os, sys, time, requests

# Get the current folder
folder = os.path.abspath(os.path.dirname(sys.argv[0]))

outputFile = open("wholeCorpus.txt", "w", encoding="utf-8")

for file in glob.glob(os.path.join(os.path.join(os.path.join(folder, "text"), "texts-pages-20-24"), "*.txt")):
   outputFile.writelines("\n¤¤File "+file+"¤¤\n")
   inputFile = open(file, "r", encoding="utf-8", errors="ignore")
   for line in inputFile:
      outputFile.writelines(line)


for file in glob.glob(os.path.join(os.path.join(os.path.join(folder, "text"), "texts-pages-40-44"), "*.txt")):
   outputFile.writelines("\n¤¤File "+file+"¤¤\n")
   inputFile = open(file, "r", encoding="utf-8", errors="ignore")
   for line in inputFile:
      outputFile.writelines(line)