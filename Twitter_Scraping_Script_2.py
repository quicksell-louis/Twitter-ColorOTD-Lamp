import tweepy 
import sys
import serial
import struct

#Create Serial port object called arduinoSerialData
ser = serial.Serial("COM1", 57600)
connected = False
ser.close()

#Twitter API credentials
consumer_key = 'YOUR CONSUMER KEY HERE'
consumer_secret = 'YOUR CONSUMER SECRET HERE'
access_key = 'YOUR ACCESS KEY HERE'
access_secret = 'YOUR ACCESS SECRET HERE'

def get_user_tweets(user_name, num_tweets):
    # Open the Serial Connection
    ser.close()
    ser.open()
    loopVar = True
    
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize list to hold tweet colors
    tweets_colors = []
    
    #Initialize string to hold current tweet
    this_tweet = ""
    
    #Initialize string to hold current color
    this_color = ""

    #Initialize tuple to hold rgb values
    rgb = ()

    #Initialize list to hold rgb values
    rgb_values =[]


    #Call to get access tweets from specified user
    tweets = api.user_timeline(screen_name='color_OTD',count=num_tweets)


    if (ser.isOpen()):
    # Start a main loop
        while (loopVar):
            #Loop through all tweets accessed
            for tweet in tweets:

                #If the tweet isn't a retweet
                if not tweet.retweeted:
                    
                    #Get # with hex color value
                    this_tweet = str(tweet.entities.get('hashtags'))

                    #Access hex value within hashtag string
                    this_color = this_tweet[11:17]

                    #Append all colors to list
                    tweets_colors.append(this_color)

                    #Convert from hex to rgb
                    rgb = tuple(int(this_color[i:i+2], 16) for i in (0, 2 ,4))

                    #Add individual rgb values to list
                    rgb_values = [rgb[0], rgb[1], rgb[2]]
                    #Write rgb values to csv
                    #writer.writerow(rgb_values)
                    print(rgb[0])
                    print(rgb[1])
                    print(rgb[2])
                    
                    #Send Red value
                    redVal = rgb[0]
                    print(struct.pack('>B', redVal))
                    ser.write(b"r" + struct.pack('>B',redVal))

                    #Send Green value
                    greenVal = rgb[1]
                    print(struct.pack('>B', greenVal))
                    ser.write(b"g" + struct.pack('>B',greenVal))

                    #Send Blue value
                    blueVal = rgb[2]
                    print(struct.pack('>B', blueVal))
                    ser.write(b"b" + struct.pack('>B',blueVal))

                    #Print out tweet text to check for correct color
                    print(tweet.text.encode('utf-8'))
                    
                    # Check if user wants to end
                    loopCheck = input('Loop (y/N):')
                    if (loopCheck == 'N'):
                        loopVar = False
                        break

        # After loop exits, close serial connection
        ser.close()



            
		
if __name__ == '__main__':
    get_user_tweets('color_OTD', 5)
