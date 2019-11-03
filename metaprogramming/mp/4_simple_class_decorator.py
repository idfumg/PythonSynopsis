# Question: why this does not working?

@debugmethods
class BrokenSpam:
    @classmethod
    def grok(klass):
        pass
    @staticmethod
    def bar():
        pass
