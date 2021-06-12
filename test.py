import ecard
import datetime

now = datetime.datetime.now().strftime('%Y-%m-%d')
e = ecard.Ecard(username, password, url)
e.Login()
e.ObtainIntervalBill('1', '10', now, now)
e.ObtainDormitoryElectricity('0', '5', '237')
