import requests
import time
import os

print time.asctime().split(' ')[4].split(':')

def get_seconds(datetimet):
#     """
#     Takes a time of day and converts it to seconds.
#     Args:
#         datetime: Time of day as HH:MM:SS
#     """
    time = datetimet.split(' ')[4].split(':')
    # Hours + Minutes + Seconds
    return int(int(time[0])*360 + int(time[1])*60 + int(time[2]))




def downspeed():
    url = "http://speedtest.ftp.otenet.gr/files/test100k.db"
    current_seconds = get_seconds(time.asctime())
    file = requests.get(url)
    file_size = int(file.headers['Content-Length'])/1000
    dl_seconds = get_seconds(time.asctime())
    time_difference = dl_seconds - current_seconds
    try:
        return round(file_size/time_difference)
    except ZeroDivisionError:
        return 'huina'



def upspeed():
    current_seconds = get_seconds(time.asctime())
    dummy_file = os.path.join(os.getenv('APPDATA'), 'dummy.txt')
    post_url = 'http://httpbin.org/post'
    with open(dummy_file, 'wb') as dummy:
        for i in range(1500):
            dummy.write(str.encode('This is a dummy text. Its sole propose is being uploaded to a server. '))
        dummy.close()
    files = {'file' : open(dummy_file, 'rb')}
    request = requests.post(post_url, data=files)
    file_size = int(request.headers['Content-Length'])/1000
    dl_seconds = get_seconds(time.asctime())
    time_difference = dl_seconds - current_seconds
    try:
        return round(file_size/time_difference)
    except ZeroDivisionError:
        return 'huina'
if __name__ == '__main__':
    while True:
        up = None
        down = None

        if up == None and down == None:
            up = upspeed()
            down = downspeed()

            print('At {0} your Downspeed is: {1}, and your Upspeed is: {2}'.format(time.asctime(), down, up))

            time.sleep(5)

            up = None
            down = None
