# Ransom Detector
A cross-platform detection (with naive protection) of ransomware. The name of the file is `scooby.py` , for Scooby-Doo - the cartoon dog.


## Prequisets 
Install watchdog and glob using pip
    
    pip install watchdog
    pip install glob

If you would like to run an encryption example, you're welcome to do so.
The file `cryptit.py` will encrypt `h3.txt` . The script uses the PyCrypto module installed with

    pip install pycrypto



## Notice
* Files must be plain text at initial run.
* It will detect the malicious change only on `.txt` files.
* After a file has been encrypted (or identifies as such) the script won't back up it's content again.

## How does it work

The script lies in the source folder, while it protects the `.txt` files in `data` folder
In it's initialization it will create backup files in the same folder. Those backup files will have a `.bc` extension added to file name. Moreover, backup files will be in hidden mode (both in Windows and Linux). 

### How does it detect malicious change / encrypting
The script runs in the background, waiting to detect one of the following conditions:
1. Check if the change is in ASCII.
2. Check if there are characters like `=,+,^` , which I identified as a pattern in AES encryption for example.
3. Check for amount of spaces before the change and after the change. I found that a cipher has significantly less spaces then a plain text would have. Therefore, if the amount of spaces changed drastically - it is considered encrypted.
4. Check for the ratio between lower and upper case letter. I found in ciphers that there is a different distribution of upper and lower case letters between ciphers and plain text. I check for that ratio and it can identify a file as encrypted.


### The Backup Proccess
In this script there is a safe backing up routine.
With every change made to the text files, the script is backing up the files (explained earlier). If it detects an encrypting txt in the next change - it does not back up the data, the CLI will prompt a notification of a possible encryption and the user can still save his data by using the back up files.

### By Steps
Steps:
1. Initialization: 
    Edit the text files as you like (with plain text)
2. Run:
    Run the script `scooby.py` in it's folder. On the CLI you will see the results.
3. Once a suspicious change has been identified:
   1. `Suspicious File Alert` - A file that isn't a txt file has been created.
   2. `Encrypt Alert` - If the script indetifies a change as an encryption to one of the txt files.
4. While an encrypt alert arises, the back-up files will not change and will stay protected.