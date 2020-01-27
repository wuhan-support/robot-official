# # 微信公众号/服务号 token
# TOKEN = ''

# # 机器人监听
# ROBOT_HOST = 'auto'
# ROBOT_PORT = 8000

# # Redis 服务器
# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379

# # SQLite 配置
# DB_FILE = 'feiyan-help.sqlite'

# # App ID 及 secret
# APP_ID = ""
# APP_SECRET = ""



# def mark_repeater(f, n) -> func:
#     if n == 0:
#         return lambda x: x
#     elif n == 1:
#         return f
#     else:
#         return lambda x: f(make_repeater(f, n - 1)(x))

# make_repeater(f, 0) -> x: x
# make_repeater(f, 1) -> x: f(x)
# make_repeater(f, 2) -> x: f(x: f(x)(x))  == x: f(f(x))


inc = lambda x: x + 1
tri = lambda x: x * 3
squ = lambda x: x ** 2

# def rep(f, n):
#     compFunc = lambda x: x
#     for i in range(n):
#         # compFuncs.append(lambda x: f(compFuncs[i](x)))
#         tmp = compFunc
#         compFunc = lambda x: f(compFunc(x))
#     return compFunc


def rep(f, n):
    compFuncs = [lambda x: x] * n
    for i, compFunc in enumerate(compFuncs):
        compFuncs[i] = lambda x: compFunc(compFuncs[i-1](x))
    return compFuncs[-1]
    # for i in range(1, n):
    #     compFuncs[i] = lambda x: f(compFuncs[i-1](x))
    # return lambda x: f(compFuncs[-1](x))

# def rep(f, n):
#     f0 = lambda x: x
#     f1 = lambda x: f(f0(x))
#     f2 = lambda x: f(f1(x))
#     f3 = lambda x: f(f2(x))
#     return f3


rep(inc, 2)(3)
