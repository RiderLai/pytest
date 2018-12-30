"""山西省交通运输计算"""

from random import choice


def maxtoubiao(num):
    xiafuxishu = [0.5 + 0.5 * i for i in range(6)]
    return num * (1 - choice(xiafuxishu) * 0.01)


def lilunchengben(maxtou, pinbiaos):
    if len(pinbiaos) > 5:
        pinbiaos.remove(max(pinbiaos))
        pinbiaos.remove(min(pinbiaos))

    pinbiaoavg = 0
    for pinbiao in pinbiaos:
        pinbiaoavg += pinbiao
    pinbiaoavg /= len(pinbiaos)
    return (maxtou * 0.5 + pinbiaoavg * 0.5) * 0.85


def pinbiaojizhunjia(maxtou, pinbiaos):
    if len(pinbiaos) > 5:
        pinbiaos.remove(max(pinbiaos))
        pinbiaos.remove(min(pinbiaos))

    pinbiaoavg = 0
    for pinbiao in pinbiaos:
        pinbiaoavg += pinbiao
    pinbiaoavg /= len(pinbiaos)

    jiaquanxishu = choice([0.3, 0.35, 0.4])
    pingbiaoxishu = choice([0.96, 0.97, 0.98, 0.99])
    return (maxtou * jiaquanxishu + pinbiaoavg * (1 - jiaquanxishu)) * pingbiaoxishu


zuigaotoubiao = int(input("输入最高投标限价"))
pinbiaojias = [int(i) for i in input("输入评标价(以空格分隔)").split(' ')]

zuigaotoubiao = maxtoubiao(zuigaotoubiao)
(pinbiaojias.remove(i) for i in pinbiaojias if i > zuigaotoubiao)

chengben = lilunchengben(zuigaotoubiao, pinbiaojias)
(pinbiaojias.remove(i) for i in pinbiaojias if i < chengben)

pinbiaojizhun = pinbiaojizhunjia(zuigaotoubiao, pinbiaojias)

pinbiaojaavg = 0
for pinbiaojia in pinbiaojias:
    pinbiaojaavg += pinbiaojia
pinbiaojaavg /= len(pinbiaojias)

e = 1
if pinbiaojaavg < pinbiaojizhun:
    e = 0.5

print(100 - 100 * e * abs(pinbiaojaavg - pinbiaojizhun) / pinbiaojizhun)
