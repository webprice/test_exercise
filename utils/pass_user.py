import re
str_regex = r'[A-Za-z0-9-]{4,30}'

#Function check if there is no spaces in between password/username
#and lengh more than 4, less than 30 and have no special chars
#must contain only chars and numbers
def pass_user(*args):
    #print(args)
    for str1 in args:
        #print(len(str))
        #print(str1)
        #print((bool(re.match(str_regex, str(str1)))))
        if (' ' in str1) or (str1.isascii()==False) or (4 > len(str1)) or  (len(str1) > 30) or (bool(re.match(str_regex, str(str1))) == False):
            return False

    return True