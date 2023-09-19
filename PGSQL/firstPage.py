import click
import time
import loginModuleStudent
# import loginModuleStudent_

current_sem = 1
current_year = 2022

def firstPage():
    click.clear()

    while(1):
        
        print("***** Welcome to AIMS Portal *****")
        print("1. Academics Office")
        print("2. Faculty")
        print("3. Student")
        print("4. Exit")

        choice = input()

        if(choice == str(1) or choice == str(2) or choice == str(3)):
            loginModuleStudent.loginModule(current_sem, current_year)
        elif(choice == str(4)):
            return
        else:
            input("\n\nWrong Input. Please try again! \n Press any key to continue")

            click.clear()
            continue


firstPage()


# CREATE EVENT deleteUser ON SCHEDULE EVERY 1 MINUTE DO DELETE FROM SESSION WHERE 'Time' < DATE_SUB(NOW(), INTERVAL 15 MINUTE);
# CREATE EVENT delFromSession ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL 30 MINUTE DO DELETE FROM SESSION; 
# CREATE EVENT deleteUser ON SCHEDULE EVERY 1 SECOND DO DELETE FROM SESSION WHERE Time <= DATE_SUB(NOW(), INTERVAL 15 MINUTE);
# 