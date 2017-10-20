import urllib 

def read_text():
    quotes = open("C:/Users/HP/Desktop/udacity_FSND/curriculum_1/Lesson_8/resources/movie_dialogue.txt")
    content = quotes.read()
    #print(content)
    quotes.close()
    check_profanity(content)
    
def check_profanity(text_to_check):
    connection = urllib.urlopen("http://www.wdylike.appspot.com/?q=" + text_to_check)
    output = connection.read()
    if "true" in output:
        print("Profanity Alert!!!")
    if "false" in output:
        print("No curse word in the text.")
    connection.close()
    
read_text()
