'''Module to define one implementation of the general interface to the chatbot'''
import rivescript
import rivescript_loader
import bot_abstract


class BotRivescript(bot_abstract.BotInterface):
    '''Concrete class to define a general interface for the chatbot'''
    def __init__(self, preprocessor=None,
                       brain="./brain",
                       interpreter=rivescript.RiveScript(),
                       postprocessor=None):
        '''The chatbot interface includes an optional message preprocessing and
        reply postprocessing layers'''
        self._preprocessor   = preprocessor
        self._interpreter    = rivescript_loader.loadBrain(interpreter, brain)
        self._postprocessor  = postprocessor

    def createUserSession(self, userInfo):
        # userinfo is expected to be just the userid *by this implementation!*
        userid = userInfo
        self._enterGlobalTopicFor(userid)
        self._moveToFirstConcernFor(userid)

    def _enterGlobalTopicFor(self, userid):
        reply = self._interpreter.reply(userid, "set glob")

    def _moveToFirstConcernFor(self, userid):
        reply = self._interpreter.reply(userid, "internal matcher to start the conversation")

    def reply(self, message):
        userid = message.getUserid()
        messagecontent = self._preprocess(message.getContent())
        reply = self._interpreter.reply(userid, messagecontent)
        reply = self._postprocess(reply)

        return reply

    def _preprocess(self, message):
        '''To tell the preprocessor to preprocess the message (if the
        preprocessor has been initialized)'''
        if self._preprocessor is not None:
            return self._preprocessor.process(message)
        else:
            return  message

    def _postprocess(self, reply):
        '''To tell the postprocessor to postprocess the message (if the
        postprocessor has been initialized)'''
        if self._postprocessor is not None:
            return self._postprocessor.process(reply)
        else:
            return reply
