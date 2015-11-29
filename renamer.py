__author__ = 'hng'
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import musicbrainzngs as mbz
from shutil import move
from glob import glob
import os

"""
	PackSongs pack songs into folders according to property choosen
	by the user making easy to manage songs and keep them into folders
"""


class PackSongs(object):
    """ Initializing info to use for creating folders """

    def __init__(self, input_folder, tag=''):
        self.tag = tag
        self.folder = input_folder
        self.change_cwd()
        self.list_mp3files(self.folder)
        self.song_info = None
    """ Finding song info """

    def find_info_from_filename(self, song_name):
        info = dict()
        # Loading Song
        self.head, self.ext = os.path.splitext(song_name)

        self.data = self.head.split(" - ")
        if self.data[1] != "Unknown Album":
            info['album'] = self.data[1]
        else:
            info['album'] = ''

        if self.data[2] != "00":
            info['tracknumber'] = int(self.data[2])

        info['artist'] = self.data[3]

        print(self.data)
        self.file = self.data[4]
        info['title'] = self.file
        return info
    def find_info(self, song_name):
        info = dict()
        # Loading Song
        self.head, self.ext = os.path.splitext(song_name)
        try:

            if self.ext == ".mp3":
                self.mp3file = MP3(song_name, ID3=EasyID3)
                print(self.mp3file)
                # print(self.mp3file['tracknumber'][0].split('/')[0])
                # Storing all details of song into "info" dictionary
                try:
                    info['title'] = str(self.mp3file['title'][0])
                except:
                    info['title'] = ''
                try:
                    info['artist'] = str(self.mp3file['artist'][0])
                except:
                    info['artist'] = ''
                try:
                    info['album'] = str(self.mp3file['album'][0])
                except:
                    info['album'] = ''
                try:
                    info['performer'] = str(self.mp3file['performer'][0])

                except:
                    info['performer'] = ''

                try:
                    info['year'] = str(self.mp3file['date'][0])
                except:
                    info['year'] = ''
                try:
                    info['duration'] = int(self.mp3file.info.length * 1000)

                except:
                    info['duration'] = ''
                try:
                    info['tracknumber'] = int(self.mp3file['tracknumber'][0])
                except:
                    try:
                        info['tracknumber'] = int(self.mp3file['tracknumber'][0].split("/")[0])
                    except:
                        info['tracknumber'] = ''
                try:
                    info['discnumber'] = int(self.mp3file['discnumber'][0])
                except:
                    try:
                        info['discnumber'] = int(self.mp3file['discnumber'][0].split('/')[0])
                    except:
                        info['discnumber'] = ''
            elif self.ext == ".m4a":
                self.mp3file = MP4(song_name)
                # print(self.mp3file['trkn'])
                print("----------------")
                print(self.head)
                print(self.mp3file['disk'])
                # Storing all details of song into "info" dictionary
                try:
                    info['title'] = str(self.mp3file['©nam'][0])
                except:
                    info['title'] = ''
                try:
                    info['artist'] = str(self.mp3file['aART'][0])
                except:
                    info['artist'] = ''
                try:
                    info['album'] = str(self.mp3file['©alb'][0])
                except:
                    info['album'] = ''
                try:
                    info['performer'] = str(self.mp3file['©wrt'][0])

                except:
                    info['performer'] = ''

                try:
                    info['year'] = str(self.mp3file['date'][0])
                except:
                    info['year'] = ''
                try:
                    info['duration'] = int(self.mp3file.info.length * 1000)

                except:
                    info['duration'] = ''
                try:
                    info['tracknumber'] = int(self.mp3file['trkn'][0][0])
                except:
                    info['tracknumber'] = ''
                try:
                    # print("disk number:")
                    # print(self.mp3file['disk'][0][0])
                    # print(self.mp3file['disk'][0][0].split(",")[0])
                    info['discnumber'] = int(self.mp3file['disk'][0][0])

                except:

                    info['discnumber'] = ''



        except:
            info = {}
        # print(info)
        self.song_info = info

    """
		Changing current working directory to user input folder to access songs
	"""

    def change_cwd(self):
        print("changing folder")
        os.chdir(self.folder)

    """ Checking if required folder exists otherwise create a new one """

    def check_folder(self, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    """ Storing list of all .mp3 files """

    def list_mp3files(self, folder=''):
        # All posibilities of writing mp3 considered ;)
        self.songs = []
        for dirName, subdirList, fileList in os.walk(folder):
            for fname in fileList:
                self.head, self.extension = os.path.splitext(fname)
                if self.extension == ".mp3":
                    self.songs.append(dirName + "/" + fname)
                elif self.extension == ".m4a":
                    self.songs.append(dirName + "/" + fname)



        # self.songs = glob('*.??3')
        # else:
        #     return glob(folder + '/*.??3')

    """ Moving song to specific folder """

    def move_song(self, song, folder_name):
        try:
            move(song, folder_name)
        except:
            pass

    """
		Generate a log file stating the songs inside each newly created
		directory
	"""

    def generate_log(self):
        # Listing all newly made folders
        new_folders = [i for i in os.listdir('.') if (os.path.isdir(i))]
        # Writing nfo data into log file
        fh = open('PackLog.txt', 'w')
        for folder in new_folders:
            text = 'Folder	:	' + folder + '\n' + "-" * (12 + len(folder)) + \
                   '\n\n' + 'Track Listing' + '\n' + "-" * len('Track Listing') + '\n'
            try:
                songs = os.listdir(folder)
                for index, name in enumerate(songs):
                    text += str(index + 1) + '. ' + name + '\n'
            except:
                continue
            fh.write(text + '\n\n\n')
        fh.close()

    """ Putting all songs in folders according to user choice """


    def put_songs(self):
        # Traversing all songs

        for song in self.songs:
            # Calling function to find song info
            self.find_info(song)
            info = self.song_info
            if info != {}:
                # print(info['artist'] + " - " + info['album'])
                # print(info['tracknumber'])
                self.head, self.tail = os.path.split(song)
                self.path, self.ext = os.path.splitext(song)

                # if info['tracknumber'] != '':
                #     if info['title'] != '':
                #         self.tracknumber = "0"
                #
                #         if info['tracknumber']<10:
                #             self.tracknumber += str(info['tracknumber'])
                #         else:
                #             self.tracknumber = str(info['tracknumber'])
                #
                #
                #         # print(self.head + "/" + self.tracknumber  + " - "  + info['title'] + self.ext)
                #         print(str(info['discnumber']))
                #         os.rename(song, self.head + "/disc " + str(info['discnumber']) + "/" + self.tracknumber  + " - "  + info['title'] + self.ext)
                #         # os.rename(song, self.head + "/" + self.tracknumber  + " - "  + info['title'] + self.ext)
                # else:
                #     os.rename(song, self.head + "/ - " + info['title'] + self.ext)



                folder_name = info['album']
                if folder_name in [None, '', 'Unknown']:
                    folder_name = 'Random'

                self.check_folder(folder_name)
                self.move_song(song, folder_name)



class UpdateSongInfo(PackSongs):

    def convert_to_unicode(self, string):
        return string.decode('utf-8')
    def save_info_from_file(self, song_name):
        info = self.find_info_from_filename(song_name)
        self.mp3file = MP3(song_name, ID3=EasyID3)
        print(info['title'])
        self.mp3file['title'] = info['title']
        self.mp3file['artist'] = info['artist']
        if info['album'] != '':
            self.mp3file['album'] = info['album']
        # if info['tracknumber'] != '':
        #     self.mp3file['tracknumber'] = info['tracknumber']

        try:
            # Saving new info back to song properties
            self.mp3file.save()
        except:
            pass
    def save_info(self, song_path, key, value):
        # Loading new changed song info
        self.head, self.ext = os.path.splitext(song_path)
        if self.ext == ".mp3":
            self.mp3file = MP3(song_path, ID3=EasyID3)
            self.mp3file['performer'] = value
            print("mp3")
        elif self.ext == ".m4a":
            self.mp3file = MP4(song_path)
            self.mp3file['aArt'] = value
            print(self.mp3file['aArt'])



        # print(self.mp3file['aART'])

        # # Loading Song
        # try:
        #     # Updating title of song
        #     try:
        #         self.mp3file[key] = value
        #     except:
        #         print("error")
        #         pass
        # except:
        #     pass
        #
        try:
            # Saving new info back to song properties
            self.mp3file.save()
        except:
            print("error saving")
            pass

    def updateSong(self):
        for file in self.songs:
            self.head, self.extension = os.path.split(file)
            self.performer = (os.path.basename(self.head).split(" - ")[0])
            self.save_info(file,'performer','Cafe Buddha')
    def updateSongFromFile(self):
        for file in self.songs:
            # self.find_info_from_filename(file)
            self.save_info_from_file(file)





"""
	UpdateSongInfo class updates all the songs information using online
	Music Brainz database.
"""


class UpdateSongInfoOld(PackSongs):
    """ Authenticate the client to query the Music Brainz Server """

    def authenticate(self):
        mbz.set_useragent('mp3fm', 1.0, 'akshit.jiit@gmail.com')

    """ Searching music brainz db for particular song """

    def search_musicbrainz(self, song_name):
        info = self.song_info
        if info['title'] == '' or 'Track' in info['title']:
            # Converting song_name into lower case so that we don't have to
            # search for all .MP3 combination like(mp3,mP3,Mp3,MP3)
            song_name = song_name.lower()
            if '.mp3' in song_name:
                pos = song_name.find('.mp3')
            info['title'] = song_name[:pos]

        # Finding song information in DB of music brainz and taking only 1
        # result in response by using limit=1
        self.data = mbz.search_recordings(query=info['title'], limit=1,
                                          artist=info['artist'], release=info['album'],
                                          date=str(info['year']), qdur=str(info['duration'])
                                          )

    """ Extracting information from result found in above function """

    def extract_info(self):
        info = self.song_info
        data = self.data
        if data['recording-list'] != []:
            result = data['recording-list'][0]
            try:
                title = result['title']
                if title != '':
                    info['title'] = title
            except:
                pass
            try:
                artist = result['artist-credit'][0]['artist']['name']
                if artist != '':
                    info['artist'] = artist
            except:
                pass
            try:
                for res in result['release-list']:
                    if 'title' in res and res['title'] != title:
                        album = res['title']
                        break
                if album != '':
                    info['album'] = album
            except:
                pass
            try:
                for res in result['release-list']:
                    if 'date' in res:
                        date = res['date'].split('-')
                        year = [i for i in date if len(i) == 4][0]
                        break
                if year != '':
                    info['year'] = year
            except:
                pass
            try:
                dur = data['recording-list'][0]['length'] / 1000
                if dur != '':
                    info['duration'] = dur
            except:
                pass
        else:
            info = {}
        # Updating old song info with new info found from net
        self.song_info = info

    """ Converting string into unicode string using UTF-8 format """

    def convert_to_unicode(self, string):
        return string.decode('utf-8')

    """ Saving new song info """



    def save_info(self, song_name):
        # Loading new changed song info
        info = self.song_info
        # Loading Song
        try:
            # Updating title of song
            try:
                self.mp3file['title'] = self.convert_to_unicode(info['title'])
            except:
                pass
            # Updating artist of song
            try:
                self.mp3file['artist'] = self.convert_to_unicode(info['artist'])
            except:
                pass
            # Updating song album
            try:
                self.mp3file['album'] = self.convert_to_unicode(info['album'])
            except:
                pass
            # Updating release_date of song
            try:
                self.mp3file['date'] = self.convert_to_unicode(info['year'])
            except:
                pass
        except:
            pass

        try:
            # Saving new info back to song properties
            self.mp3file.save()
        except:
            pass

        # Updating song name to title of song
        try:
            if info['title'] != '':
                os.rename(song_name, info['title'] + '.mp3')
        except:
            pass

    """ Function calling all other functions to update song info """

    def update_id3(self):
        self.authenticate()
        for song in self.songs:
            self.find_info(song)
            if self.song_info != {}:
                self.search_musicbrainz(song)
                self.extract_info()
                self.save_info(song)


"""
	UnpackFolders class is unpacking all the folders so that all songs comes
	out from folders and reside at one place
"""


class UnpackFolders(PackSongs):
    """ Listing all folders """

    def list_folders(self):
        self.folders_to_unpack = [i for i in os.listdir('.')
                                  if (os.path.isdir(i))]

    """ Redefining the function which is Moving song to specific folder """

    def move_song(self, folder_name, song):
        folder = folder_name
        try:
            # Moving a song from folder to current directory
            move(song, '.')
            # Storing songs list for creating log file
            try:
                self.moved_songs[folder].append(song)
            except:
                self.moved_songs[folder] = [song]
        except:
            # Storing songs list for creating log file
            try:
                self.unmoved_songs[folder].append(song)
            except:
                self.unmoved_songs[folder] = [song]

    """
		Redefining the function which is Generating log according to
		different types
	"""

    def generate_log(self):
        prev_songs = self.existing_songs
        moved_songs = self.moved_songs
        unmoved_songs = self.unmoved_songs
        # Opening a log file for
        fh = open('UnpackLog.txt', 'w')
        # Writing previously existing songs in log file
        fh.write('*** Previously existing Songs before unpacking ***\n\n')
        for index, song in enumerate(prev_songs):
            fh.write(str(index) + '. ' + str(song) + '\n')

        # Writing moved songs in log file
        fh.write('\n\n\n*** Songs MOVED while unpacking ***\n')
        for folder in moved_songs:
            fh.write('\n\n' + str(folder) + ':\n')
            for index, song in enumerate(moved_songs[folder]):
                fh.write(str(index) + '. ' + str(song) + '\n')

        # Writing unmoved songs in log file
        fh.write('\n\n\n*** Songs UNMOVED while unpacking ***\n')
        for folder in unmoved_songs:
            fh.write('\n\n' + str(folder) + ':\n')
            for index, song in enumerate(unmoved_songs[folder]):
                fh.write(str(index) + '. ' + str(song) + '\n')

    """ Running all other functions to unpack folders """

    def unpack(self):
        # Making folders to create log file
        self.existing_songs = self.songs
        self.moved_songs = {}
        self.unmoved_songs = {}
        # Listing all folders inside given folder
        self.list_folders()

        # Traversing all folder to unpack them
        for folder in self.folders_to_unpack:
            # Listing all songs under a folder
            songs = self.list_mp3files(folder)
            # Traversing all songs and moving them
            for song in songs:
                self.move_song(folder, song)


def main():
    input_folder = '/Volumes/music/input/dave matthews band'
    mp3fm = PackSongs(input_folder, 'album')
    mp3fm.put_songs()
    mp3fm.generate_log()

    #
    # mp3fm = UnpackFolders(input_folder)
    # mp3fm.unpack()

    # mp3fm = UpdateSongInfo(input_folder)
    # mp3fm.updateSong()
    # mp3fm = UpdateSongInfo(input_folder)
    # mp3fm.updateSongFromFile()

def main2():
    # User Choice Menu
    options = "1. Pack Songs into Folders.\n2. Unpack all Songs from Folders\n\
3. Update Properties(ID3) of songs.\nEnter Choice:"
    menu = "1. TITLE\n2. ARTIST\n3. ALBUM\n4. YEAR\n5. DURATION\n6. COMMENT"
    tags = {1: 'title', 2: 'artist', 3: 'album', 4: 'year', 5: 'duration',
            6: 'comment'}

    print(options)
    choice = input()
    choice = int(choice)

    # Input folder would be the folder which contains all songs.
    input_folder = 'M:/original soundtrack/'

    if choice == 1:
        print("'mp3fm' gives you the choice to move songs into folders according to given 6 categories:")
        print(menu)
        print("Enter Number corresponding to above given choices: ")

        tag = tags[int(input())]

        print("jeje")
        mp3fm = PackSongs(input_folder, tag)
        mp3fm.put_songs()
        mp3fm.generate_log()

        print("*** Folders made with a LOG file containing Songs Info. \
present in every folder ***")

    elif choice == 2:
        mp3fm = UnpackFolders(input_folder)
        mp3fm.unpack()
        mp3fm.generate_log()

    elif choice == "3":
        mp3fm = UpdateSongInfo(input_folder)
        mp3fm.update_id3()


if __name__ == '__main__':
    main()
# class c_Rename():
#     def __init__(self):
#         #self.run()
#
#     def RenameDirectory(self, dir):
#         self.dir = dir
#         self.dir = self.dir.replace("'", "")
#         self.dir = self.dir.replace(".", "")
#         self.dir = self.dir.replace("&", "and")
#         self.dir = self.dir.replace(" (Unprocessed)", "")
#         self.dir = self.dir.replace("_", "")
#         self.dir = self.dir.replace("!", "")
#         os.rename(dir, self.dir)
#         return self.dir
#
#     def run(self):
#         self.rootDir = 'U:\mp3\Various Artists'
#         for dirName, subdirList, fileList in os.walk(self.rootDir):
#
#             self.dir = dirName
#
#
#             #print('Found directory: %s' % self.RenameDirectory(self.dir))
#             #rename the directory too
#
#
#             for fname in fileList:
#
#
#                 self.CurrentFile = fname
#
#                 self.head, self.tail = os.path.splitext(self.CurrentFile)
#                 if self.tail == ".mp3" or self.tail == ".mpa":
#                     self.TrackNumber = fname[:2]
#                     try:
#                         self.tracknumber = int(self.TrackNumber)
#                     except:
#                         logging.debug("File does not have a tracknumber,%s", fname)
#                         continue
#
#
#                     self.bRenameIt = False
#                     if self.CurrentFile.find("'")>-1:
#                         self.CurrentFile = self.CurrentFile.replace("'", "")
#                         self.bRenameIt = True
#
#                     if self.CurrentFile.find("_")>-1:
#                         self.CurrentFile = self.CurrentFile.replace("_", "")
#                         self.bRenameIt = True
#                     if self.CurrentFile.find("+")>-1:
#                         self.CurrentFile = self.CurrentFile.replace("+", "and")
#                         self.bRenameIt = True
#                     if self.CurrentFile.find(",")>-1:
#                         self.CurrentFile = self.CurrentFile.replace(",", "")
#                         self.bRenameIt = True
#                     if self.CurrentFile.find("!")>-1:
#                         self.CurrentFile = self.CurrentFile.replace("!", "")
#                         self.bRenameIt = True
#
#                     if self.CurrentFile.find("&")>-1:
#                         self.CurrentFile = self.CurrentFile.replace("&", "and")
#                         self.bRenameIt = True
#
#                     self.tokens = self.head.split(".")
#                     if len(self.tokens) > 1:
#                         self.bRenameIt = True
#                         self.CurrentFile = self.head.replace(".","")
#                         self.CurrentFile += self.tail
#
#                     if self.CurrentFile[3] != "-":
#                         #print("file does not have a dash")
#                         self.TrackNumber = self.CurrentFile[:2]
#                         self.rest = self.CurrentFile[2:]
#                         self.CurrentFile = (self.TrackNumber + " -" + self.rest)
#                         # self.TrackName = fname.split("-")[2][1:]
#                         self.bRenameIt = True
#
#                     if self.bRenameIt:
#                         try:
#                             logging.debug(self.dir)
#                             logging.debug("%s ==> %s", self.dir + "/" + fname, self.dir + "/" + self.CurrentFile)
#                         except:
#                             logging.debug("something went wrong")
#
#                         if os.path.exists(self.dir + "/" + self.CurrentFile):
#                             os.remove(self.dir + "/" + self.CurrentFile)
#
#                         os.rename(self.dir + "/" + fname, self.dir + "/" + self.CurrentFile)
#
#
#
#
#
#
#
#
#
#
#             # for fname in fileList:
#             #     self.TrackNumber = fname[:2]
#             #     self.TrackName = fname.split("-")[2][1:]
#             #
#             #     self.newTrackName = (dirName + "/" + self.TrackNumber + " - " + self.TrackName)
#
#             #     #print("renamed :" + dirName + "/" + fname + " ==> " +  self.newTrackName)
#
# main = c_Rename()
