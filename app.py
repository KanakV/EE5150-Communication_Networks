import time
from client.userClient import User

# user = User(102)
# while not user.associated:
#     user.associate()

# print(user.get())


user1 = User(102)

while not user1.associated:
    user1.associate()

user1.send(101, "Hello from 102")
print("SLEEPING FOR 5 MINUTES")
time.sleep(305)
print("WOKE UP")
user1.send(101, "2 Messages")

# user2 = User(103)

# while not user2.associated:
#     user2.associate()

# user2.send(101, "Hello from 103")
# user2.send(101, "2 Messages")


# user1.send(102, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum")

# user2 = User(102)

# user2.associate()
# print(user2.get())
