import urllib.request
import webbrowser
import os
import time
import dateutil.parser as dp



def take_repo():
    address = input("Type in repo address: ")
    return address

def compare_number():
    number = input("Type in the number of users to compare:")
    return int(number)

def take_user():
    user = input("Type in the user name: ")
    return user

def input_time():
    choice = input("Type 'u' for entering unix timestamp;\nType 't' for entering ISO 8601 time;\nType others for default: ")
    if choice == "u":
        time = int(input("Enter unix timestamp: "))
    elif choice == "t":
        time = input("Enter ISO 8601 time: ")
        parsed_t = dp.parse(time)
        time = int(parsed_t.strftime('%s'))
    else:
        time = 0
    return time

def main():
    repo_address = take_repo()
    number = compare_number()
    users = []
    for i in range(number):
        users.append(take_user())
    time = input_time()

    url = "https://api.github.com/repos/"
    seperated_address = repo_address.split('/')
    url += (seperated_address[3]+'/'+seperated_address[4])
    url += "/stats/contributors"

    response = urllib.request.urlopen(url)
    content = response.read()
    content = content.decode("utf-8")

    for user in users:
        if user not in content:
            print("No such user exist!")
            return
    
    format_content = content.strip('[]').split(',')

    start_time = int(format_content[1].split(':')[2])

    if time != 0:
        if int(time) < start_time:
            print("Invalid time input!")
            return

    file = open("compare.csv","w")
    file.write(users[0])
    for user in users[1:]:
        file.write(',' + user)
    file.write('\n')

    url = "https://api.github.com/repos/"
    url += (seperated_address[3]+'/'+seperated_address[4])
    url += "/commits"

    response = urllib.request.urlopen(url)
    content = response.read()
    content = content.decode("utf-8")

    format_content = content.strip('[]').split(',')

    users_commit_list = []
    max_length = 0

    for user in users:
        temp_user_list = []
        for i in range(len(format_content)):
            if "\"committer\":{\"name\"" in format_content[i]:
                time_slot = format_content[i+2].strip('\"{}').split(':')[1:]
                print_time = "{}:{}:{}".format(time_slot[0],time_slot[1],time_slot[2]).strip('\"')
            if "\"committer\":{\"login\"" in format_content[i]:
                if user in format_content[i].split(':')[2]:
                    if time == 0:
                        temp_user_list.append(print_time)
                    else:
                        parsed_print_time = dp.parse(print_time)
                        print_time_in_seconds = int(parsed_print_time.strftime('%s'))
                        if print_time_in_seconds >= time:
                            temp_user_list.append(print_time)
        if len(temp_user_list) > max_length:
            max_length = len(temp_user_list)
        users_commit_list.append(temp_user_list)

    for i in range(max_length):
        write_string = ""
        for sub in users_commit_list:
            if i < len(sub):
                write_string += (sub[i] + ',')
            else:
                write_string += ','
        file.write(write_string[0:-1] + '\n')
        
    file.close()
    return
        
main()
