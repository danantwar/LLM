try:
    Value=int(input("Type a number between 1 and 5:"))
except ValueError:
    print("You must type a number between 1 and 5!")
except:
    print("This is a generic error!")
else:
    if (Value>0) and (Value<=5):
        print("You typed:", Value)
    else:
        print("The value you typed is incorrect!")
        
