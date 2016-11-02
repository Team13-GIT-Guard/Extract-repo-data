import urllib.request
import webbrowser
import os
import datetime
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

    file = open("onecontributor.tsv","w")
    file.write("date\tvalue\n")

    start_line = 0;
    end_line = 0;
    for line in format_content:
        if "\"site_admin\"" in line:
            start_line = end_line + 1
        if user in line:
            end_line += 1
            break;
        end_line+=1


    for i in range(start_line,end_line):
        if time == 0:
            if "\"weeks\"" in format_content[i]:
                commit = format_content[i+3].strip('{}[]').split(':')[1]
                print_time = datetime.datetime.fromtimestamp(int(format_content[i].split(':')[2])).strftime('%Y-%m-%d %H:%M:%S')
                file.write(print_time.split(' ')[0] + '\t' + commit + '\n')
            elif "\"w\"" in format_content[i]:
                commit = format_content[i+3].strip('{}[]').split(':')[1]
                print_time = datetime.datetime.fromtimestamp(int(format_content[i].split(':')[1])).strftime('%Y-%m-%d %H:%M:%S')
                file.write(print_time.split(' ')[0] + '\t' + commit + '\n')
        else:
            if "\"weeks\"" in format_content[i]:
                if time <= int(format_content[i].split(':')[2]):
                    commit = format_content[i+3].strip('{}[]').split(':')[1]
                    print_time = datetime.datetime.fromtimestamp(int(format_content[i].split(':')[2])).strftime('%Y-%m-%d %H:%M:%S')
                    file.write(print_time.split(' ')[0] + '\t' + commit + '\n')
            elif "\"w\"" in format_content[i]:
                if time <= int(format_content[i].split(':')[1]):
                    commit = format_content[i+3].strip('{}[]').split(':')[1]
                    print_time = datetime.datetime.fromtimestamp(int(format_content[i].split(':')[1])).strftime('%Y-%m-%d %H:%M:%S')
                    file.write(print_time.split(' ')[0] + '\t' + commit + '\n')

    file.close()
    return
        
main()
