import re
import json
import time
from bot import login_and_reviews

print("Let's get your preferences\n")

print("Just 4 questions\n")

while True:

    # asks user for email id and checks for the validity of the email id
    while True:
        email = input("Enter your Silicon Labs Full Email ID: ").strip()
        if bool(re.search("^[a-zA-Z]+\.[a-zA-Z]+@silabs\.com$", email)):
            break
        else:
            print("You have entered wrong Email ID. Please enter your Email ID in the form: FirstName.LastName@silabs.com\n")

    # shows reference and asks for password
    print("\n\nTo setup your HungerBox Password, refer this link: https://www.office.com/")
    password = input("Enter your HungerBox Password: ")

    # asks for dietary preference (veg/non-veg) and checks for the validity
    while True:
        print("\n\nNow let's get your dietary preference")
        print("Choose one out of the below two options")
        print("1. Veg")
        print("2. Non-veg")
        dietary = input("\nWhat's your preference? ").strip()

        if bool(re.search("^\d$", dietary)) and (dietary == '1' or dietary == '2'):
            dietary = int(dietary) - 1
            break
        else:
            print("You have entered an invalid option. Please enter value only from the below options")

    # asks for meal preference (breakfast/lunch/both) and checks for the validity
    while True:
        print("\n\nChoose your meal(s)")
        print("Choose one out of the below three options")
        print("1. Breakfast only")
        print("2. Lunch only")
        print("3. Both Breakfast and Lunch")
        meal = input("\nWhat's your choice? ").strip()

        if bool(re.search("^\d$", meal)) and (meal == '1' or meal == '2' or meal == '3'):
            meal = int(meal) - 1
            break
        else:
            print("You have entered an invalid option. Please enter value only from the below options")

    print("\n\n\nSummary:")
    print("Email ID       : " + email)
    print("Password       : " + password)
    print("Dietary Choice : " + ("Veg" if (dietary==0) else "Non-veg"))
    print("Meal(S)        : " + ("Breakfast only" if (meal==0) else "Lunch only" if (meal==1) else "Both Breakfast and Lunch"))

    if "Y" == input("\nPress 'Y' to confirm your choice, else press enter to re-fill the details: "):
        print("\nLet's test whether the credentials are working")
        print("\nOpening the browser")
        print("\n\nDO NOT DO ANYTHING UNTIL BROWSER CLOSES\n\n")
        time.sleep(5)

        driver = login_and_reviews(5, email, password)
        time.sleep(5)
        
        driver.quit()
        if "Y" == input("\nPress 'Y' to confirm whether the credentials worked, else press enter to re-fill the details: "):
            break

# create a dictionary to dump as json
json_dict = {
    "email" : email,
    "password" :password,
    "dietary" : dietary,
    "meals" : meal
}

# dumps the preference to config json file
with open(".\config\config.json", mode="w") as file:
   json.dump(json_dict, file, indent=4)

print("\nYour preference has been recorded.\n\nTo change your preference, re-run this file.")
