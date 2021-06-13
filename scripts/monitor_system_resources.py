import pymsteams
import psutil
import os
import socket

ACCESS_KEY = "https://niyatainfotech1.webhook.office.com/webhookb2/154c1208-39a9-4804-9d58-2babb82179a6@d2884742-ac3f-49b3-9834-7139f07fa308/IncomingWebhook/ab2c749966214cc89ba161dcf04ae7eb/845373b4-6d2b-4a82-b24f-1f569e551d68"
IMG1 = "https://gitlab.com/pravinmj.cs/testdevops/uploads/61a203eeaf07e6998356d44d9872633d/sd.png"
IMG2 = "https://gitlab.com/pravinmj.cs/testdevops/uploads/916439a4ba14e6e484d2915df7a53346/saa.png"

SET_CPU_LIMIT = 10
SET_MEMORY_LIMIT = 10


def connect_teams(access_key):
    """ Create and returns a msteams connection object"""
    connection = pymsteams.connectorcard(ACCESS_KEY)
    return connection


def add_section(**data):
    """ Get data, create and return a card section """
    section = pymsteams.cardsection()
    section.title(f"Alert-from server - {data['host_ip']}")
    # Activity Elements
    section.activityTitle(f"Current {data['type']} usage at {data['value']}%")
    section.activityImage(data["img"])
    return section


def get_host_data():
    """ Get the current host details """
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        msg = "success"
    except:
        host_name = ""
        host_ip = ""
        msg = "Unable to get host details"

    return host_ip, host_name, msg


def usage_stats():
    """ Get system cpu and memory usage stats """
    load1, load5, load15 = psutil.getloadavg()
    cpu_usage = (load15 / os.cpu_count()) * 100
    memory_usage = psutil.virtual_memory()[2]
    return cpu_usage, memory_usage


def send_message(host_ip, host_name, msg):
    """ Invoke connection, get connector card, add section and send message"""
    my_teams_message = connect_teams(ACCESS_KEY)
    my_teams_message.title("Resource Usage Alert")
    if msg == "success":
        my_teams_message.text(f"<h1>You have received usage alert from {host_name}</h1>")
    else:
        my_teams_message.text(f"<h1>You have received usage alert. Unable to retrieve host details</h1>")
    my_teams_message.color("#006cab")
    section = pymsteams.cardsection()
    cpu_usage, memory_usage = usage_stats()

    if cpu_usage > SET_CPU_LIMIT:

        cpu_section = add_section(connection_obj=section, type="CPU", host_ip=host_ip, value=cpu_usage, img=IMG1)
    else:
        cpu_section = None

    if memory_usage > SET_MEMORY_LIMIT:
        section = pymsteams.cardsection()
        memory_section = add_section(connection_obj=section, type="Memory", host_ip=host_ip, value=memory_usage, img=IMG2)
    else:
        memory_section = None

    try:
        if cpu_section is not None and memory_section is None:
            print(True, 1)
            my_teams_message.addSection(cpu_section)
            my_teams_message.send()
        elif cpu_section is None and memory_section is not None:
            print(True, 2)
            my_teams_message.addSection(memory_section)
            my_teams_message.send()
        elif cpu_section is not None and memory_section is not None:
            print(True, 3)
            my_teams_message.addSection(cpu_section)
            my_teams_message.addSection(memory_section)
            my_teams_message.send()
    except Exception as err:
        my_teams_message.text(err)
        my_teams_message.send()


if __name__ == "__main__":
    host_ip, host_name, msg = get_host_data()
    send_message(host_ip, host_name, msg)
