print("-----Program for Student Information-----")

Dictiondary = dict()
n = 0
while True:
    try:
        n = int(input('[+] Enter Length of list student: '))
        break
    except:
        print('[-] Input accept interger only.')


for i in range(0, n):
    print(f'\n- Student {i+1}:')
    student_name = input("[*] Enter student name: ")
    age = input("[*] Enter student age: ")
    test_score = input('[*] Enter test score: ')
    Dictiondary[student_name] = (age, test_score)

def sort():
    list_student = list()
    for name, details in Dictiondary.items():
        tup = name
        list_student.append(tup)
    list_student = sorted(list_student)
    for i in list_student:
        print(i)
    return


def minmarks():
    list_student = list()
    for name, details in Dictiondary.items():
        list_student.append(details[1])
    list_student = sorted(list_student)
    print("- Minimum marks: ", min(list_student))

    return

def searchdetail(fname):
    list_student = list()
    for name, details in Dictiondary.items():
        tup = name
        list_student.append(tup)
    for i in list_student:
        if i == fname:
            print(f'Student name: i, age:{Dictiondary.get(i)[0]}, test score: {Dictiondary.get(i)[1]}')
    return

def option():
    print('============ MENU ============')
    choice = int(input('Enter the operation detail: \n - 1: Sorting using first name \n - 2: Finding Minimum marks \n - 3: Search contact number using first name: \n - 4: Exit\n - [*] Your option: '))

    if choice == 1:
        sort()
        inp = input('Do you want to do more (Y/n): ')
        if 'y' in inp.lower():
            option()


    elif choice == 2:
        minmarks()
        inp = input('Do you want to do more (Y/n): ')
        if 'y' in inp.lower():
            option()

    elif choice == 3:
        first = input('Enter first name of student: ')
        searchdetail(first)
        inp = input('Do you want to do more (Y/n): ')
        if 'y' in inp.lower():
            option()

    exit('[-] Executed successfully!')


option()