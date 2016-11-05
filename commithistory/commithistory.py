import subprocess
import webbrowser
import os
import csv

def repo():
	return input('pls input repo')

def take_repo():
    address = raw_input("Type in local repo address: ")
    return address

def take_file():
    address = raw_input("Type in file address: ")
    return address

def take_start_line():
    line = raw_input("Type in start line: ")
    return line

def take_end_line():
    line = raw_input("Type in end line: ")
    return line

def take_line():
        choice = raw_input("Type 'l' for specific lines;\nType others for deafult: ")
        if choice == "l":
                start_line = take_start_line()
                end_line = take_end_line()
                return (start_line,end_line)
        else:
                return 0

def git_clone(url,dir):
	subprocess.call('git clone '+url +' '+ dir, shell=True)

def git_contributors(dir):
	res = subprocess.Popen('git log --pretty="%an"',stdout=subprocess.PIPE, shell=True,cwd=dir)
	res = res.stdout.readlines()
	ret = []
	for i in res:
		if i not in ret:
			ret.append(i)
	return ret

def git_check(dir,file,beg=0,end=0):
	if (beg<>0)&(end<>0):
		res = subprocess.Popen('git log  --pretty="%an" -L '+beg+','+end+':'+file,stdout=subprocess.PIPE,shell=True,cwd=dir)
	else:
		res = subprocess.Popen('git log  --pretty="%an" '+file,stdout=subprocess.PIPE,shell=True,cwd=dir)
	res = res.stdout.readlines()
	cons = git_contributors(dir)
	ret = []
	for con in cons:
		num = res.count(con)
		if (num<>0):
			ret.append((con.replace('\n',''),num))
	write(ret)
	return ret

def write(s):
	csvfile = file('commithistory.csv', 'wb')
	writer = csv.writer(csvfile)
	writer.writerow(['contributor', 'times'])
	writer.writerows(s)
	csvfile.close()

if __name__ == '__main__':
	#rmb to clone first
	repo_address = take_repo()
	file_address = take_file()
	line = take_line()
	if line == 0:
		git_check(repo_address,file_address)
	else:
		git_check(repo_address,file_address,line[0],line[1])
	path = os.path.abspath('commit_history.html')
	url = 'file://' + path
	webbrowser.open(url)
