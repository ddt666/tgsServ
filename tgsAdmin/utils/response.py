class BaseResponse(object):
    def __init__(self):
        self.code = 1000
        self.msg = ""
        self.data = None


    @property
    def dict(self):
        return self.__dict__


if __name__ == '__main__':
    res=BaseResponse()
    print(res)
