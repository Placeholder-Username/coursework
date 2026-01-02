import matplotlib.pyplot as plt

def Show_graph(self):
    days = ["Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"]
    minutes_studied = [0,30,45,60,90,99]
    colours = []
    for minutes in minutes_studied:
        if minutes == 0:
            colours.append("red")
        elif minutes < 30:
            colours.append("orange")
        else:
            colours.append("green")
    plt.bar(days,minutes_studied,color = colours)
    plt.title("Graph of Sessions")
    plt.xlabel("Days")
    plt.ylabel("Study Time")
    plt.show()