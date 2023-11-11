import glob, os, re, sys, time

# Get the current folder
folder = os.path.abspath(os.path.dirname(sys.argv[0]))

norm = open(os.path.join("normalized-files-20221109","all.year-modfr-smtnorm.tsv"), "r", encoding="utf-8", errors="ignore")
bestNorm = open(os.path.join("normalized-files-20221109","all.norm.smt+lefff.fr.txt"), "r", encoding="utf-8", errors="ignore").readlines()
denorm = {}
for d in range(160,170):
   denorm[str(d)] = open(os.path.join(os.path.join("normalized-files-20221109","smt_norm+denorm_decade"),"all.denorm-decade." + str(d) + ".fr"), "r", encoding="utf-8", errors="ignore").readlines()

bestNormByYear = {}
normDenormByYear = {}
allYears = []

year = ""
lineNb = 0
for line in norm:
   res = re.search("^([^\t]+)\t([^\t]+)\t([^\t]+)", line)
   if res:
      currentYear = res.group(1)
      orig = res.group(2)
      norm = bestNorm[lineNb]
      if currentYear != year:
         year = currentYear
         print(year)
         bestNormByYear[year] = []
         normDenormByYear[year] = []
         allYears.append(year)
      bestNormByYear[year].append(orig + "\t" + norm)
      normDenormByYear[year].append(denorm[year[0:3]][lineNb][1:len(denorm[year[0:3]][lineNb])].replace("\r","").replace("\n","") + "\t" + norm)
      #print(orig + "\t" + norm)
   lineNb += 1

for year in allYears:
   print(year)
   print("lines:" + str(len(bestNormByYear[year])))
   #outputFile = open("year"+str(year)+".tsv", "w", encoding="utf-8", errors="ignore")
   outputFile = open(os.path.join("yearNormBest","year"+str(year)+".tsv"), "w", encoding="utf-8", errors="ignore")
   lineNb = 0
   for line in bestNormByYear[year]:
      outputFile.writelines(line)
   outputFile.close()

for year in allYears:
   print(year)
   print("lines:" + str(len(normDenormByYear[year])))
   #outputFile = open("year"+str(year)+".tsv", "w", encoding="utf-8", errors="ignore")
   outputFile = open(os.path.join("yearNormDenorm","year"+str(year)+".tsv"), "w", encoding="utf-8", errors="ignore")
   lineNb = 0
   for line in normDenormByYear[year]:
      outputFile.writelines(line)
   outputFile.close()