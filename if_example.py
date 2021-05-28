userDefaultPassword = {132:0x0B, 133:0x0C, 134:0x0D, 135:0x0E, 136:0x0A, 137:0x0B, 138:0x0C, 139:0x0D}

print("{}".format(userDefaultPassword))
print("{}".format(userDefaultPassword.get(132)))
print("{}".format(userDefaultPassword[132]))
print("{}".format(userDefaultPassword.keys()))
print("{}".format(userDefaultPassword.values()))
#print("{132}".format_map(userDefaultPassword))
valArray = list(userDefaultPassword.values())
print("{}".format(valArray))
keyArray = list(userDefaultPassword.keys())
print("{}".format(keyArray))