from datetime import datetime
import datetime as date
import requests
import smtplib

def gmailLogin():
    global smtpserver
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    # Authentication
    smtpserver.login("alert.drowsiness.system@gmail.com", "drowsiness@123")

def sendPlainEmail(unUploadedSongName,unUploadedSongCount,UploadedSongCount,UploadedSongName):
    gmailLogin()
    message = "Today Youtube data uploaded Details \n\n1. Total Uploaded Song Count = " + str(UploadedSongCount) + '\n 2. Total Uploaded Channel Names = '+ str(UploadedSongName) + "\n 3. Total unUploaded Song Count = "+ str(unUploadedSongCount)+ '\n 4. Total Uploaded Channel Names = '+str(unUploadedSongName)
    smtpserver.sendmail("alert.drowsiness.system@gmail.com", "Technowebtech@gmail.com", message)
    print('Email send Successfully')
    # terminating the session
    smtpserver.quit()

 ## Check time if time is 11:45 then it starting its working
while True:
    unUploadedSongName = []
    unUploadedSongCount = 0
    UploadedSongCount = 0
    UploadedSongName = []
    current_time = datetime.now()
    today_11_45_PM = current_time.replace(hour=20, minute = 54, second=0)
    if current_time == today_11_45_PM:
        print("\n So my time is now lets do my job current time is ", current_time)

        ##### Get the channel Information
        authKey	="AIzaSyCm36OyFY0aOrBD5tVRPlCVSu2gN274EZM";
        resp = requests.get("http://garhkumo.com/Api/channel")
        channel_data = resp.json()
        today_date = str(date.date.today())
        print(channel_data,len(channel_data))
        for channel in  range(len(channel_data)):
                channel_name = channel_data[channel]['c_name']
                channel_id = channel_data[channel]['c_name_id']
                channel_date = channel_data[channel]['channel_add'].split(' ')[0]
                print('\nchannel name = ',channel_name,
                      '\nchanel date = ', channel_date,
                      '\nchannel id = ',channel_id,)
                if today_date==channel_date:
                        print('same date of channel skiping channel')
                        continue
                else:
                        print('NO Same date of channel')
                        #### Get Youtube channel video playlist details
                        resp = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&order=date&q=site%3Ayoutube.com&channelId="+channel_id+"&key="+authKey)
                        data = resp.json()
                        print(data)
                        for i in range(0,3):
                                songId = data['items'][i]['id']['videoId']
                                songName = data['items'][i]['snippet']['title']
                                songPublishdate = data['items'][i]['snippet']['publishedAt'][:10]
                                songImg = data['items'][i]['snippet']['thumbnails']['high']['url']
                                songdescription = data['items'][i]['snippet']['description']
                                print('\nsongId',songId,
                                      '\nsongName',songName,
                                      '\nsongPublishDate',songPublishdate,
                                      '\nSongImage',songImg,
                                      '\nDecrption',songdescription,)
                                if songPublishdate==today_date:
                                        #### Uplooad Song data on API
                                        APIurl = 'http://garhkumo.com/technowebtech/api/index.php'
                                        songData = {'data': 'insert',
                                                    'songId' :  songId,
                                                    'songName' :  songName,
                                                    'songImg' :   songImg,
                                                    'channelId' : channel_id,
                                                    'releaseDate' : songPublishdate ,
                                                    'description' :  songdescription}
                                        try:
                                                APIresponse = requests.post(APIurl, data = songData)
                                                UploadedSongCount = unUploadedSongCount + 1
                                                if channel_name not in unUploadedSongName:
                                                    UploadedSongName.append(channel_name)
                                                print(APIresponse.text,'Song Data Successfully Uploaded because song was uploaded today')
                                        except Exception as e:
                                                print('Data not uploaded due to this error = ',e,'\n\n')
                                else:
                                    unUploadedSongCount = unUploadedSongCount + 1
                                    if channel_name not in unUploadedSongName:
                                        unUploadedSongName.append(channel_name)
                                    print('Song not uoloaded because song not uploaded today')
                                    continue
        sendPlainEmail(unUploadedSongName,unUploadedSongCount,UploadedSongCount,UploadedSongName)
        unUploadedSongName.clear()
        unUploadedSongCount = 0
        UploadedSongName.clear()
        UploadedSongCount = 0
        print(unUploadedSongName,unUploadedSongCount,UploadedSongCount,UploadedSongName)
    else:
        print('Currently skiping bcoz current time is ',current_time)
        continue
