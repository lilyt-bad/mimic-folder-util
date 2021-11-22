import os
import subprocess
from tkinter import filedialog

print('Select root folder to mimic')
rootdir = filedialog.askdirectory()
print('Select root folder to write into')
newdir = filedialog.askdirectory()

just_list_diffs = False
have = []
dont_have = []

filePaths = []
flagged = []

def getFilePaths():
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            # Make new subfolder
            newFolderPath = subdir.replace(rootdir, newdir)
            if not os.path.exists(newFolderPath):
                os.makedirs(newFolderPath)
        
            filePaths.append({ 'origin': subdir, 'new': newFolderPath, 'file_name': file })


folderProcs = {}
def promptForFiles():
    for path in filePaths:
        # check if matching file does not yet exist
        npf = os.path.realpath(os.path.join(path['new'], path['file_name'])) 
        if not os.path.exists(npf):
            if just_list_diffs:
                dont_have.append(path['file_name'])
            else:
                print('')
                print(path['new'])
                print(path['file_name'])
                p = os.path.realpath(path['new'])
                command = rf'explorer "{p}"'
                try:
                    folderProcs['p'] = subprocess.Popen(command)
                    while True:
                        action = input("Next(n)|Return later(r)|Show origin file(o)|Flag(f)|Exit(e):")
                        if action == 'n': # Next
                            break
                        elif action == 'r': # Return to later
                            dont_have.append(path['file_name'])
                            break
                        elif action == 'f': # Flag with note
                            note = input('Note: ')
                            flagged.append({ 'path': path, 'note': note })
                            break
                        elif action == 'o': # Show path file
                            opf = os.path.realpath(os.path.join(path['origin'], path['file_name'])) 
                            command = rf'explorer /select,"{opf}"'
                            folderProcs['o'] = subprocess.Popen(command)
                        elif action == 'e':
                            return
                finally:
                    for key in folderProcs.keys():
                        folderProcs[key].terminate()
                        folderProcs[key].kill()
        elif just_list_diffs:
            have.append(path['file_name'])
        

if __name__ == "__main__":
    getFilePaths()
    promptForFiles()
    for flag in flagged:
        print(os.path.realpath(flag['path']['origin']))
        print(f"file: {flag['path']['file_name']}")
        print(flag['note'])

    print('')
    print('Have files:')
    for diff in have:
        print(diff)

    print('')
    print('Don\'t have files:')
    for diff in dont_have:
        print(diff)