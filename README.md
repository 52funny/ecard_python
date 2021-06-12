# Ecard

智慧一卡通 Python

## Demo

- 获取电费

  ```python
  e = ecard.Ecard(username, password, url)
  e.Login()
  e.ObtainBalance()
  ```

- 获取余额
  ```python
  e = ecard.Ecard(username, password, url)
  e.Login()
  e.ObtainDormitoryElectricity('0', '5', '237')
  ```
- 获取今天的消费记录

  `typeFlag 1 消费 2 充值 3 补助 4 互转`

  ```python
  import ecard
  import datetime

  now = datetime.datetime.now().strftime('%Y-%m-%d')
  e = ecard.Ecard(username, password, url)
  e.Login()
  e.ObtainIntervalBill('1', '10', now, now)
  ```

## Acknowledgements

- [pytesseract](https://github.com/madmaze/pytesseract)
- [requests](https://github.com/psf/requests)
- [PyExecJS](https://github.com/doloopwhile/PyExecJS)