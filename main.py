#Project - CRUD Operations with python
#Author 
import os
from pathlib import Path 
def readffileandfolder():
    p = Path('')
    items = list(p.rglob('*'))
    for index,file in enumerate(items):
        print(f'{index+1} - {file}')

def create_file():
    try:
        readffileandfolder()
        file_name = input("Enter name of your file: ")
        p = Path (file_name)
        if p.exists():
            print("File already exists")
        else:
            with open(file_name,'w') as file:
                content = input("Enter your file content: ")
                file.write(content)
                print("File added!")
    except Exception as e:
        print(e)




def  read_file():
    try:
        readffileandfolder()
        file_name = input("Enter name of your file: ")
        p = Path (file_name)
        if p.exists():
            with open(file_name,'r') as file:
                print(file.read())
        else:
            print("File not found!")
    except Exception as e:
        print(e)
        



def update_file():
    try:
        readffileandfolder()
        file_name = input('Enter name of your file: ')
        p = Path(file_name)
        if p.exists():
            with open(file_name,'r') as file:
                print(file.read())
            print('Press 1 to overwrite the content')
            print('Press 2 to append new content')



            option = int(input('Enter your choice for updating a file: '))
            if option == 1:
                with open (file_name,'w') as file:
                    content = input('Enter your content: ')
                    file.write(content)
                    print('Content Changed')


            elif option == 2:
                with open (file_name,'a') as file:
                    content = input('Enter your content: ')
                    file.write(content)
                    print('Content Changed')
            else:
                print("INVALID INPUT")
        else:
            print("File does not exists!")
    except Exception as e:
        print(e)



def delete_file():
        readffileandfolder()
        file_name = input ("Enter name of your file: ")
        p = Path (file_name)
        if p.exists():
            os.remove(p) #OS is removing path of that file completely from the system.
            print("FILE DELETED")
        else:
            print ("FILE DOES NOT EXITS")


def rename_file():
    readffileandfolder()
    file_name = input("Enter name of your file: ")
    p = Path (file_name)
    if p.exists():
        new_file = input ("Enter new name of your file: ")
        p.rename(new_file)
        print('File renamed')
    else:
        print("File not found!")

def create_folder():
    readffileandfolder()
    folder_name = input('Enter name of your folder: ')
    p = Path(folder_name)
    if p.exists():
        print("Folder not found!")
    else:
        p.mkdir()
        print('Folder created!')

def delete_folder():
    readffileandfolder()
    folder_name = input('Enter name of your folder: ')
    p = Path(folder_name)
    if p.exists():
        p.rmdir()
        print("Folder deleted!")
    else:
        print('Folder not found!')


def create_file_in_folder():
    folder_name = input("Enter your folder name: ")
    file_name = input("Enter name of your file: ")
    p = Path (folder_name)/file_name
    if p.exists():
        print('File already exists!')
    else:
        pass

while True:
    print("Press 1 for creating a file")
    print("Press 2 for reading a file")
    print("Press 3 for updating a file")
    print("Press 4 for deleting a file")
    print("Press 5 for renaming a file")
    print("Press 6 for creating a folder")
    print("Press 7 for deleting a folder")
    print("Press 0 for exiting...")



    option = int(input("Enter your choice:"))
    if option ==1:
        create_file()

    if option == 2:
        read_file()

    if option == 3:
        update_file()

    if option == 4:
        delete_file()

    if option == 5:
        rename_file()

    if option == 6:
        create_folder()

    if option == 7:
        delete_folder()

    if option == 0:
        break