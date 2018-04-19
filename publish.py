import sys
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

if __name__ == '__main__':
    thingName = sys.argv[1]
    host = sys.argv[2]
    rootCAPath = sys.argv[3]
    certificatePath = sys.argv[4]
    privateKeyPath = sys.argv[5]

    myAWSIoTMQTTClient = AWSIoTMQTTClient('test')
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    myAWSIoTMQTTClient.connect()

    while 1:
        topic_data = {
            "EE122/project": '"HELLO WORLDS!"',
            "EE122/final-sol": '"NOT AVAILABLE UNTIL MAY 15th"'
        }

        for topic in topic_data:
            print("Publishing data...")
            myAWSIoTMQTTClient.publish(topic, topic_data[topic], 1)

        time.sleep(30)
