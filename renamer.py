__author__ = 'hng'
import os

class c_Rename():
    def __init__(self):
        self.run()
    def run(self):
        self.rootDir = 'z:/complete'
        for dirName, subdirList, fileList in os.walk(self.rootDir):
            print('Found directory: %s' % dirName)
            for fname in fileList:


                self.CurrentFile = fname

                self.head, self.tail = os.path.splitext(self.CurrentFile)
                if self.tail == ".mp3" or self.tail == ".mpa":
                    self.TrackNumber = fname[:2]
                    try:
                        self.tracknumber = int(self.TrackNumber)
                    except:
                        print("File does not have a tracknumber")
                        continue


                    self.bRenameIt = False
                    if self.CurrentFile.find("'")>-1:
                        self.CurrentFile = self.CurrentFile.replace("'", "")
                        self.bRenameIt = True

                    if self.CurrentFile.find("_")>-1:
                        self.CurrentFile = self.CurrentFile.replace("_", "")
                        self.bRenameIt = True

                    if self.CurrentFile[3] != "-":
                        #print("file does not have a dash")
                        self.TrackNumber = fname[:2]
                        self.rest = fname[2:]
                        self.CurrentFile = (self.TrackNumber + " -" + self.rest)
                        # self.TrackName = fname.split("-")[2][1:]
                        self.bRenameIt = True

                    if self.CurrentFile.find("&")>-1:
                        self.CurrentFile = self.CurrentFile.replace("&", "and")
                        self.bRenameIt = True

                    self.tokens = self.CurrentFile.split(".")
                    if len(self.tokens) > 2:
                        self.bRenameIt = True
                        self.extension = self.tokens[len(self.tokens)]
                        self.newName = ""
                        for i in range(len(self.tokens)-1):
                            if i < len(self.tokens)-2:
                                self.newName += self.tokens[i] + " "
                            else:
                                self.newName += self.tokens[i]

                        self.CurrentFile = self.newName



                    if self.bRenameIt:
                        print(fname + " ==> " + self.CurrentFile)
                        print("testing")








            # for fname in fileList:
            #     self.TrackNumber = fname[:2]
            #     self.TrackName = fname.split("-")[2][1:]
            #
            #     self.newTrackName = (dirName + "/" + self.TrackNumber + " - " + self.TrackName)
            #     #os.rename(dirName + "/" + fname, self.newTrackName )
            #     #print("renamed :" + dirName + "/" + fname + " ==> " +  self.newTrackName)

main = c_Rename()




