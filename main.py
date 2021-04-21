from pprint import pprint
import csv
import re


with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


result_list = []
p_list = []


def full_name(iteration):
  sep = re.findall('\s', iteration[0])
  if not sep:
    lastname = iteration[0]
    sep_firstname = re.findall('\s', iteration[1])
    if sep_firstname:
      wrong_sep_firstname = re.split('\s',iteration[1])
      firstname, surname = wrong_sep_firstname
      return lastname, firstname, surname
    else:
      firstname = iteration[1]
      surname = iteration[2]
      return lastname, firstname, surname
  else:
    wrong_sep = re.split('\s',iteration[0])
    if len(wrong_sep) > 2:
      lastname, firstname, surname = wrong_sep
      return lastname, firstname, surname
    else:
      lastname, firstname = wrong_sep
      surname = iteration[2]
      return lastname, firstname, surname
  

def phone(iteration):
  num = iteration[5]
  regex_num = r'(\+7|8)[-\s]?\((\d+\s*)\)\s*(\d+)[-\s]?(\d+)[-\s]?(\d+)[-\s]?'
  subst_num = "+7(\\2)\\3-\\4-\\5"
  num_match = re.match(regex_num, num)

  if num =='phone':
    return num
  elif num_match:
    num = re.sub(regex_num, subst_num, num)
  else:
    regex_num = r"(\+7|8)\s*(\d{3})[-\s]?\s*(\d{3})[-\s]?(\d{2})[-\s]?(\d+)[-\s]?"
    num = re.sub(regex_num, subst_num, num)
  
  regex_add = r"(\+7\(\d+\s*\)\d{3}\-\d{2}\-\d{2})\D+[\s]?(\d{4})\D?"
  subst_add = "\\1 доб.\\2"
  num_match_add = re.match(regex_add, num)
  if num_match_add:
    num = re.sub(regex_add, subst_add, num)
    return num
  else:
    return num
  

for item in contacts_list:
  contact = []
  lastname, firstname, surname = full_name(item)
  num = phone(item)
  contact.append(lastname)
  contact.append(firstname)
  contact.append(surname)
  contact.append(item[3])
  contact.append(item[4])
  contact.append(num)
  contact.append(item[6])
  result_list.append(contact)


blacklist = []


for item in result_list:
  n = 0
  count = 0
  original = item
  lastname = item[0]
  while n != len(result_list):
    if lastname == result_list[n][0]:
      count += 1
      if count == 2:
        blacklist.append(item)
    n += 1
  if count < 2:
    p_list.append(item)
  else:
    pass


for element in blacklist[1]:
    if element not in blacklist[0] and element != None:
        blacklist[0].append(element)



with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(result_list)