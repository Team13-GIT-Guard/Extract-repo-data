import urllib.request
import webbrowser
import os
import time
import dateutil.parser as dp



def take_repo():
    address = input("Type in repo address: ")
    return address

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
    user = take_user()
    time = input_time()

    url = "https://api.github.com/repos/"
    seperated_address = repo_address.split('/')
    url += (seperated_address[3]+'/'+seperated_address[4])
    url += "/stats/contributors"

    response = urllib.request.urlopen(url)
    content = response.read()
    content = content.decode("utf-8")
    
    if user not in content:
        print("No such user exist!")
        return
    
    format_content = content.strip('[]').split(',')

    start_time = int(format_content[1].split(':')[2])

    if time != 0:
        if int(time) < start_time:
            print("Invalid time input!")
            return

    file = open("onecontributor.csv","w")
    file.write(user + '\n')

    url = "https://api.github.com/repos/"
    url += (seperated_address[3]+'/'+seperated_address[4])
    url += "/commits"

    response = urllib.request.urlopen(url)
    content = response.read()
    content = content.decode("utf-8")

    format_content = content.strip('[]').split(',')

    for i in range(len(format_content)):
        if "\"committer\":{\"name\"" in format_content[i]:
            time_slot = format_content[i+2].strip('\"{}').split(':')[1:]
            print_time = "{}:{}:{}".format(time_slot[0],time_slot[1],time_slot[2]).strip('\"')
        if "\"committer\":{\"login\"" in format_content[i]:
            if user in format_content[i].split(':')[2]:
                if time == 0:
                    file.write(print_time + '\n')
                else:
                    parsed_print_time = dp.parse(print_time)
                    print_time_in_seconds = int(parsed_print_time.strftime('%s'))
                    if print_time_in_seconds >= time:
                        file.write(print_time + '\n')
    file.close()
    return
        
main()
