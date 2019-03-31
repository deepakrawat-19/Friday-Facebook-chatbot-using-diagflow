from fbchat import Client,log
from fbchat.models import *
import loginCredentials
import apiai,codecs,json

class myBot(Client):

    def onMessage(self,author_id=None,message_object=None,thread_id=None,thread_type=ThreadType.USER,**kwargs):
        self.markAsRead(author_id)
        log.info('Message {} from {} in {}'.format(message_object,thread_id,thread_type))

        self.apiConf()

        msg_txt=message_object.text

        self.request.query=msg_txt

        #resposne=self.request.getresponse()


        bot_response = json.loads(self.request.getresponse().read().decode('utf-8'))
       #reader=codecs.getdecoder("utf-8")

        #reply_obj=json.load(reader(resposne))

        reply=bot_response["result"]["fulfillment"]["speech"]

        if author_id!=self.uid:
            self.send(Message(text=reply),thread_id=thread_id,thread_type=thread_type)
            self.markAsDelivered(author_id,thread_id)

    def apiConf(self):
        self.CLIENT_ACCESS_TOKEN="85110c56fb0e44cfaf3c8804257f6244"
        self.ai=apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request=self.ai.text_request()
        self.request.lang="en"
        self.request.session_id="<SESSION ID, UNIQUE FOR EACH USER>"

client=myBot(loginCredentials.facebook_username,loginCredentials.facebook_password)
client.listen()