import os

def rename_files():
    file_list = os.listdir(r"C:\Users\HP\Desktop\udacity_FSND\Lesson_5\resources\prank")
    os.chdir(r"C:\Users\HP\Desktop\udacity_FSND\Lesson_5\resources\prank")
    for file_name in file_list:
        print("Before renaming file : " + file_name)
        os.rename(file_name, file_name.translate(None, "0123456789"))
        print("After renaming file : " + file_name)
rename_files()
