import random

# Function for generation random password string
def passwd_generator(count_chars = 8):
    symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890$#%_"
    return "".join(random.sample(symbols, count_chars)) 

# Call the function
print(passwd_generator(60))