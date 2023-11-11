# -*- coding: utf-8 -*-"
import csv, glob, os, re, requests, sys, time
from lxml import etree
from xml.dom import minidom

"""
    Analyze pages previously downloaded from https://repertoiretheatreimprime.yale.edu
    to extract gallica ids and corresponding bibliographic references
    Copyright (C) 2022 Philippe Gambette

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
"""

# Get the current folder
folder = os.path.abspath(os.path.dirname(sys.argv[0]))

outputCsv = open(os.path.join(folder, "theatreGallica17.tsv"), "w", encoding="utf-8")


# get the text inside the XML node
def displayNodeText(node):
   if node.childNodes.length == 0:
      data = ""
      try:
         data = node.data
      except:
         pass
      return data
   else:
      text = ""
      for child in node.childNodes:
            text += displayNodeText(child)
      return text

# get the gallica links inside the XML node
def getGallicaLinks(node):
   list = []
   if node.childNodes.length > 0:
      for child in node.childNodes:
         if child.nodeName.lower() == "a":
            attributes = dict(child.attributes.items())
            if "href" in attributes:
               link = attributes["href"]
               res = re.search("gallica",link)
               if res:
                  list.append(link)
         list += getGallicaLinks(child)
   return list

for file in glob.glob(os.path.join(os.path.join(folder, "yearPages"), "*.html")):
   print("File " + os.path.basename(file))
   input = open(file, "r", encoding="utf-8", errors="ignore")
   output = open(os.path.join(os.path.join(folder, "yearPagesProcessed"), os.path.basename(file)), "w", encoding="utf-8")
   outputString = ""
   for line in input:
      output.writelines(line.replace("<script","\n<script").replace("◒","").replace("☞",""))
   output.close()

# clean/convert HTML files to XML
gallicaByYear = {}
gallicaNbByYear = []
for file in glob.glob(os.path.join(os.path.join(folder, "yearPagesProcessed"), "*.html")):
   gallicaThisYear = []
   print("===============")
   print("===============")
   print("===============")
   print("===============")
   print("===============")
   print("File " + file+".xml")
   print("===============")
   print("===============")
   print("===============")
   print("===============")
   print("===============")
   # clean file by removing <script> tags
   save = True
   input = open(file, "r", encoding="utf-8", errors="ignore")
   output = open(file+".xml", "w", encoding="utf-8")
   lines = ""

   for line in input:

      res = re.search("<script", line)
      if res:
         save = False
      
      if save:
         line = re.sub(r"<input[^>]*>", r"", line)
         line = re.sub(r"<br[^>]*>", r"", line)
         line = re.sub(r"<link[^>]*>", r"", line)
         line = re.sub(r"<meta[^>]*>", r"", line)
         line = re.sub(r"<img[^>]*>", r"", line)
         lines += line.replace("&nbsp;"," ")
      res = re.search("</script>", line)
      if res:
         save = True
   
   parser = etree.XMLParser(recover=True)
   doc = etree.fromstring(lines, parser=parser)
   output.writelines(etree.tostring(doc).decode('utf-8'))
   output.close()

   page = minidom.parse(file+".xml")
   # get all references in the page
   references = page.getElementsByTagName("div")
   for ref in references:
      attributes = dict(ref.attributes.items())
      if attributes != None:
         if "class" in attributes and attributes["class"]=="entryF":
            id = "?"
            title = ""
            print(len(ref.childNodes[0].childNodes[1].childNodes))
            if len(ref.childNodes[0].childNodes[1].childNodes) == 1:
               nb = 0
               for c in ref.childNodes[0].childNodes:
                  nb += 1
                  display = True
                  if nb > 1:
                    text = displayNodeText(c)
                    res = re.search("Edition : ",text)
                    if res:
                       display = False
                    if display:
                       if nb == 2:
                          id = text
                       else:
                          title += text
            else:
              id = ref.childNodes[0].childNodes[1].childNodes[0].childNodes[0].data
              nb = 0
              for c in ref.childNodes[0].childNodes[1].childNodes:
                 nb += 1
                 display = True
                 if nb > 1:
                      title += displayNodeText(c)
            gallicaLinks = getGallicaLinks(ref)
            if len(gallicaLinks) > 0:
               gallicaThisYear.append(gallicaLinks[0])
               outputCsv.writelines(os.path.basename(file).replace("page","").replace(".html","")+'\t'+gallicaLinks[0]+'\t'+id+'\t'+title.replace('\t'," ").replace('\n',"")+'\n')
              
            """
            if len(ref.childNodes[0].childNodes[1].childNodes) == 6:
               print(ref.childNodes[0].childNodes[1].childNodes[0].childNodes[0].data)
               print(ref.childNodes[0].childNodes[1].childNodes[1].data + ref.childNodes[0].childNodes[1].childNodes[2].childNodes[0].data + ref.childNodes[0].childNodes[1].childNodes[3].data+ ref.childNodes[0].childNodes[1].childNodes[4].childNodes[0].data + ref.childNodes[0].childNodes[1].childNodes[5].data)
            if len(ref.childNodes[0].childNodes[1].childNodes) == 4:
               print(ref.childNodes[0].childNodes[1].childNodes[0].childNodes[0].data)
               print(ref.childNodes[0].childNodes[1].childNodes[1].data + ref.childNodes[0].childNodes[1].childNodes[2].childNodes[0].data + ref.childNodes[0].childNodes[1].childNodes[3].data)
            if len(ref.childNodes[0].childNodes[1].childNodes) == 2:
               print(ref.childNodes[0].childNodes[1].childNodes[0].childNodes[0].data)
               print(ref.childNodes[0].childNodes[1].childNodes[1].data)
            if len(ref.childNodes[0].childNodes[1].childNodes) == 1:
               print(ref.childNodes[0].childNodes[1].childNodes[0].data)
               print(ref.childNodes[0].childNodes[2].data)
            
            """
            """
            print("")
            print("")
            print("")
            """
   gallicaByYear[os.path.basename(file)] = gallicaThisYear
   gallicaNbByYear.append(len(gallicaThisYear))
print(gallicaByYear)
print(gallicaNbByYear)
outputCsv.close()