__author__ = 'hng'
import os
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class c_Rename():
    def __init__(self):
        self.run()
    def RenameDirectory(self, dir):
        self.dir = dir
        self.dir = self.dir.replace("'", "")
        self.dir = self.dir.replace(".", "")
        self.dir = self.dir.replace("&", "and")
        self.dir = self.dir.replace(" (Unprocessed)", "")
        self.dir = self.dir.replace("_", "")
        self.dir = self.dir.replace("!", "")
        os.rename(dir, self.dir)
        return self.dir

    def run(self):
        self.rootDir = 'U:\mp3\Various Artists'
        for dirName, subdirList, fileList in os.walk(self.rootDir):

            self.dir = dirName


            #print('Found directory: %s' % self.RenameDirectory(self.dir))
            #rename the directory too


            for fname in fileList:


                self.CurrentFile = fname

                self.head, self.tail = os.path.splitext(self.CurrentFile)
                if self.tail == ".mp3" or self.tail == ".mpa":
                    self.TrackNumber = fname[:2]
                    try:
                        self.tracknumber = int(self.TrackNumber)
                    except:
                        logging.debug("File does not have a tracknumber,%s", fname)
                        continue


                    self.bRenameIt = False
                    if self.CurrentFile.find("'")>-1:
                        self.CurrentFile = self.CurrentFile.replace("'", "")
                        self.bRenameIt = True

                    if self.CurrentFile.find("_")>-1:
                        self.CurrentFile = self.CurrentFile.replace("_", "")
                        self.bRenameIt = True
                    if self.CurrentFile.find("+")>-1:
                        self.CurrentFile = self.CurrentFile.replace("+", "and")
                        self.bRenameIt = True
                    if self.CurrentFile.find(",")>-1:
                        self.CurrentFile = self.CurrentFile.replace(",", "")
                        self.bRenameIt = True
                    if self.CurrentFile.find("!")>-1:
                        self.CurrentFile = self.CurrentFile.replace("!", "")
                        self.bRenameIt = True

                    if self.CurrentFile.find("&")>-1:
                        self.CurrentFile = self.CurrentFile.replace("&", "and")
                        self.bRenameIt = True

                    self.tokens = self.head.split(".")
                    if len(self.tokens) > 1:
                        self.bRenameIt = True
                        self.CurrentFile = self.head.replace(".","")
                        self.CurrentFile += self.tail

                    if self.CurrentFile[3] != "-":
                        #print("file does not have a dash")
                        self.TrackNumber = self.CurrentFile[:2]
                        self.rest = self.CurrentFile[2:]
                        self.CurrentFile = (self.TrackNumber + " -" + self.rest)
                        # self.TrackName = fname.split("-")[2][1:]
                        self.bRenameIt = True

                    if self.bRenameIt:
                        try:
                            logging.debug(self.dir)
                            logging.debug("%s ==> %s", self.dir + "/" + fname, self.dir + "/" + self.CurrentFile)
                        except:
                            logging.debug("something went wrong")

                        if os.path.exists(self.dir + "/" + self.CurrentFile):
                            os.remove(self.dir + "/" + self.CurrentFile)

                        os.rename(self.dir + "/" + fname, self.dir + "/" + self.CurrentFile)










            # for fname in fileList:
            #     self.TrackNumber = fname[:2]
            #     self.TrackName = fname.split("-")[2][1:]
            #
            #     self.newTrackName = (dirName + "/" + self.TrackNumber + " - " + self.TrackName)

            #     #print("renamed :" + dirName + "/" + fname + " ==> " +  self.newTrackName)

main = c_Rename()




