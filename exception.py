class EofException(RuntimeError):
    def __init__(self, msg):
        """
        """
        self.msg = msg

class InvalidCharException(RuntimeError):
    def __init__(self, msg):
        """
        """
        self.msg = msg
        
