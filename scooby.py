import glob
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

deleted = []


class MyHandler(FileSystemEventHandler):
    def on_deleted(self, event):
        deleted.append(str(event.src_path))

    def on_created(self, event):
        temp = str(event.src_path)
        if event.is_directory:
            return
        if ".txt" not in temp:
            print(f'Encrypt Alert: {event.event_type}  path : {event.src_path}')

    def on_modified(self, event):
        temp = str(event.src_path)

        if event.is_directory or '.bu' in temp:
            return

        # if change is legal
        # then backup the file

        if self.isLegal(event.src_path):
            self.backup(event.src_path)
        # if it isn't legal
        # send alert
        else:
            print(f'Encrypt Alert: {event.event_type}  path : {event.src_path}')

    def backup(self, path):
        '''
        Backup a file and save it to current folder
        With extension bu
        :param path: the file
        :return: None
        '''
        text = ''
        with open(path, 'r') as f:
            text = f.read()
        with open(self.get_back_file_path(path), 'w') as f:
            f.write(text)

    def isLegal(self, path):
        '''
        A method to check if a file is completely ASCII
        and doesn't contain \=+^/
        :param path:
        :return:
        '''
        text = ''
        with open(path, 'r') as f:
            text = f.read()

        backup_path = self.get_back_file_path(path)
        backup_text = ''
        with open(backup_path, 'r') as f:
            backup_text = f.read()

        condition1 = text.isascii()
        condition2 = '=' in text or '+' in text or '^' in text
        condition3 = self.count_spaces(backup_text, text)
        condition4 = self.capital_letters(text)

        if condition1 == False or condition4 == True:
            return False
        if condition2 or condition3:
            return False

        return True

    def count_spaces(self, text1, text2):
        '''
        Method that counts the difference in spaces

        :param text1: backup
                text2: text to be checked
        :return: true if there are more (by some amount) spaces in backup then in
                text to be checked
                otherwise - false
        '''
        count1 = 0
        count2 = 0
        for char in text1:
            if char == ' ':
                count1 += 1

        for char in text2:
            if char == ' ':
                count2 += 1

        diff = count1 - count2
        if diff < len(text1) / (-10):
            # too many spaces are missing
            return True
        return False

    def capital_letters(self, text):
        '''
        Another method. I noticed that there are approximately
        close amount of capital letters and lower-case letters
        That is my try to use that property
        :return: true if encrypted
        '''
        count1 = 0
        count2 = 0
        for char in text:
            if char.isupper():
                count1 += 1
            if char.islower():
                count2 += 1
        if abs(count1 - count2) < len(text) / 10:
            # encrypted
            return True
        return False

    def get_back_file_path(self, path):
        '''
        A method to get the backup file path
        :param path: of freely edited file
        :return: path of backupfile
        '''
        lastslash_index = path.rfind('/')
        toReplace = path[lastslash_index + 1:]
        path_wo_file = path[:lastslash_index] + "/"
        backup_path = path_wo_file + "." + toReplace + '.bu'
        return backup_path


if __name__ == "__main__":
    event_handler = MyHandler()
    path = 'data/'
    txtfiles = []
    for file in glob.glob(path + "*.txt"):
        txtfiles.append(file)
    for i in range(len(txtfiles)):
        event_handler.backup(txtfiles[i])

    observer = Observer()

    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
