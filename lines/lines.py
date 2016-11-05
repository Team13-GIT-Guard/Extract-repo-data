import subprocess
import webbrowser
import os
import csv

def repo():
    return input('pls input repo')

def take_repo():
    address = raw_input("Type in local repo address: ")
    return address

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

def git_check(dir):
	ret = []
	res = subprocess.Popen(u"git ls-files | while read f; do git blame --line-porcelain $f | grep '^author '; done | sort -f | uniq -ic | sort -n",stdout=subprocess.PIPE,shell=True,cwd=dir)
	lines =  res.stdout.readlines()
	for line in lines:
	    try:
	    	tmp = line.strip().split(' author ')
	    	ret.append((tmp[1],tmp[0]))
	    except IndexError:
	    	tmp = line.strip()
	write(ret)

def write(s):
	csvfile = file('lines.csv', 'wb')
	writer = csv.writer(csvfile)
	writer.writerow(['contributor', 'lines'])
	writer.writerows(s)
	csvfile.close()

if __name__ == '__main__':
	#rmb to clone first
	repo_address = take_repo()
	git_check(repo_address)
	path = os.path.abspath('lines_of_codes.html')
	url = 'file://' + path
	webbrowser.open(url)
