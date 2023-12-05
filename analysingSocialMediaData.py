'''Social media Analytics project
Libraries used - pandas for data analysis and matplotlib for graphical representation
Dataset used - in comma separated value format(csv)'''

import pandas as pd
from matplotlib import pyplot as plt
from collections import OrderedDict
import datetime as dt

# reading csv file using pandas library
dataframe = pd.read_csv("SocialMediaData.csv")

# list of all unique userIDs
all_userIDs = dataframe['userID'].unique().tolist()


# to find out which user has performed how many actions.
def action_performed():
    action_performed_by_user = dataframe.groupby('userID')['action'].count()

    # creating a file and storing all the record in it
    with open("user_analysed_data.txt", "w") as analysed_file:
        analysed_file.write("----------------Analysed User Data-------------------")
        analysed_file.write(f"\n\n------------------Number of actions performed by each user----------------\n")
        analysed_file.write(action_performed_by_user.to_string())

    # displaying data
    print("\n\033[1m1. Number of actions performed by each "
          "user:\n-----------------------------------------------------------------")
    print(f"{action_performed_by_user.to_string()}")
    print("------------------------------------------------------------------")


# finding out the userID with the highest number of actions performed
def highest_engagement():
    user_with_highest_engagement = dataframe.groupby('userID')['action'].count().idxmax()

    # storing data in the file
    with open("user_analysed_data.txt", "a") as analysed_file:
        analysed_file.write(f"\n------------------UserID has the highest engagement----------------\n")
        analysed_file.write(f"{user_with_highest_engagement}")

    #     displaying data on screen
    print("\n\n\033[1m2. User with the highest "
          "engagement:\n-----------------------------------------------------------------")
    print(f"\033[1m{user_with_highest_engagement}\033[0m has the highest engagement with the platform.")
    print("-----------------------------------------------------------------")


# finding out most common action performed
def common_action_performed():
    most_common_action_performed = dataframe['action'].mode().values[0]

    # getting total count of every action
    action_counts = dataframe['action'].value_counts()

    # Find the most common action and its count
    most_common_count = action_counts.max()

    print("\n\n\033[1m3. Most common action "
          "performed:\n------------------------------------------------------------------")
    if most_common_action_performed == "like":
        emoji = "❤"
    elif most_common_action_performed == "share":
        emoji = "🔗"
    else:
        emoji = "💬"

    # storing data in the file
    with open("user_analysed_data.txt", "a") as analysed_file:
        analysed_file.write(f"\n------------------Most common action performed----------------\n")
        analysed_file.write(f"{action_counts}")


    # displaying data on screen
    print(action_counts.to_string() + "\n")
    print(
        f"\033[1mSo {most_common_action_performed}{emoji} \033[0mis the most common action performed with \033[1m{most_common_count}\033[0m occurences.")
    print("------------------------------------------------------------------")


# # analysing usage trends
def convertingIntoSeconds(data):
    data = data.split(":")
    seconds = int(data[0]) * 3600 + int(data[1]) * 60 + int(data[2])
    return int(seconds)


def usage_trends():
    for_graph = {}
    session_login_time = {}
    session_logout_time = {}
    for index, rows in dataframe.iterrows():
        if rows['action'] == "login":
            datetime = rows['timestamp']
            if rows['userID'] not in session_login_time:
                session_login_time[rows['userID']] = convertingIntoSeconds(datetime)
            else:
                session_login_time[rows['userID']] += convertingIntoSeconds(datetime)

        if rows['action'] == "logout":
            datetime = rows['timestamp']
            if rows['userID'] not in session_logout_time:
                session_logout_time[rows['userID']] = convertingIntoSeconds(datetime)
            else:
                session_logout_time[rows['userID']] += convertingIntoSeconds(datetime)

    # sorting dictionaries alphabetically
    session_login_time = OrderedDict(sorted(session_login_time.items()))
    session_logout_time = OrderedDict(sorted(session_logout_time.items()))

    # storing data in the file
    with open("user_analysed_data.txt", "a") as analysed_file:
        analysed_file.write(f"\n-----------------Statistics of user on Hourly basis-----------------\n")
        analysed_file.write("\nUserID \t\t\t\t Time Spent \n")

        print("\n\n\033[1m4. Statistics of user in "
              "Hours:\n-------------------------------------------------------------------")
        print("UserID \t\t\t\t Time Spent \n")
        for i in all_userIDs:
            time = int((session_logout_time[i] - session_login_time[i]) / 60) / 60
            for_graph[i] = round(time)
            print(f"{i} \t\t\t {round(time)} hr(s)\n")
            analysed_file.write(f"{i} \t\t\t {round(time)} hr(s)\n")
        print("-------------------------------------------------------------------")

    # graph presentation
    status = input("\nDo you want to see graph representation of above statistics:(y/n): ")
    if status == "yes" or status == "y":
        for key in for_graph:
            x = key
            y = for_graph[key]
            plt.bar(x, y)
        plt.title("Statistics of user over time")
        plt.xlabel('Users', fontsize=18)
        plt.ylabel('Time Spent(hrs)', fontsize=16)
        plt.show()
    else:
        print("Have a great day!!")


# # storing user analysis statistics(hourly basis) in a different csv file
# with open(f"user_analysed_data.txt", "w") as file:
#     file.write(f"Analysed Data of users of {dt.date.today()}\n\n\n{action_performed()}"
#                )

# Displaying all the outputs on console

action_performed()
highest_engagement()
common_action_performed()
usage_trends()
