# from datetime import datetime
# import pytz

# # # datetime object containing current date and time
# # dt = datetime.now(pytz.timezone('Singapore'))
 
# # print("now =", dt)

# # dd/mm/YY H:M:S
# dt_string = datetime.now(pytz.timezone('Singapore')).strftime("%d%m%Y%H%M%S")
# print("date and time =", dt_string)

# d = {}

# d[(69, 420)] = "the funny"
# d[(66, 66)] = "chaos"
# # print("hello" if "chaotic" in [*d.values()] else "tite")
# print("hello" if "chaos" in d else "tite")

# l = {"aaa": 1, "bbb": 2, "ccc": 5, "ddd": 6}
# s = [key for key in l.items() if key == "ccc"][0]

# print(l, s)

name = ["me", "Mitsuha", "Taki", "Tang ina mo", "Kimi no Yawa"]

def foo():
  global name
  for i in name:
    print(i)

foo()