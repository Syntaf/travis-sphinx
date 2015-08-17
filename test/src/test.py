class Doc(object):
    "This uses some autodocs and looks great"

    def __init__(self):
        pass

    def foo(self, n):
        """
        Foo does lots of stuff

        :param str n: a string n
        :rtype: int
        """

def r_foo(x, y):
    """
    local function doc

    :param int x: integer x
    :param int y: integer y
    :rtype: int
    """

if __name__ == '__main__':
    print 'test case'