def deco1(fun):
    fun()
    return "string"


def deco2(fun):
    def wrapper(*args, **kwargs):
        fun()
        print("装饰器的操作")
        return 123
    return wrapper


@deco1
def say():
    print("函数执行")


print(say)

# 被装饰器装饰的函数可能不再是函数, 装饰是彻彻底的装饰
