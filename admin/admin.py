
class Admin:
    USERNAME = "admin"
    PASSWORD = "1234"

    @staticmethod
    def login():
        print("\n------ Admin Login ------")
        u = input("Enter Username: ")
        p = input("Enter Password: ")

        if u == Admin.USERNAME and p == Admin.PASSWORD:
            print("\nLogin Successful!\n")
            return True
        else:
            print("\nInvalid Credentials!\n")
            return False


