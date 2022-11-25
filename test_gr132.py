import pika
import unittest
import tracemalloc
import json
import random

class TestMessage(unittest.TestCase):

    def setUp(self):
        channel=pika.BlockingConnection(pika.ConnectionParameters('localhost')).channel()
        channel.exchange_declare(exchange='output', exchange_type='fanout')
        channel.queue_declare(queue='outputs', durable=True)
        tracemalloc.start()

    def tearDown(self):
        pika.BlockingConnection(pika.ConnectionParameters('localhost')).channel().stop_consuming()
        tracemalloc.stop()

    def messageSend(self, testList):
        #  convert geted list to Json form
        JsonSend=json.dumps({'input':testList})
        #  send the Json file to the server witch will process the datas
        pika.BlockingConnection(
            pika.ConnectionParameters('localhost')).channel().basic_publish(
                exchange='output', routing_key='', body=JsonSend)
        #  process check the data from the server is it equal to the right parameters
        
        return json.loads(((pika.BlockingConnection(pika.ConnectionParameters('localhost')).channel().basic_get(queue='outputs', auto_ack=True)[2]).decode()))['output']

    def test_short(self):
        testList = []
        #  generate a random list what we will send to the server
        for y in range(0,random.randrange(2,10)):
            testList.append(random.randrange(-1000000,1000000))
        
        self.assertListEqual(sorted(testList),
            list(TestMessage.messageSend(self=self,testList=testList)))