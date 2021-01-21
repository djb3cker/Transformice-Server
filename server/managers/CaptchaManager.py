import time, random, string
from captcha.image import ImageCaptcha

class CaptchaManager:
	__captcha__ = {}
	__timer__ = 0
	__image__ = ImageCaptcha(fonts=["./utils/fonts/arial.ttf", "./utils/fonts/arialbd.ttf"])

	@staticmethod
	def captcha():
		if len(CaptchaManager.__captcha__) >= 150:
			letter = random.choice(list(CaptchaManager.__captcha__))
			return letter, CaptchaManager.__captcha__[letter]
		else:
			letter = random.choice(list(string.ascii_lowercase))

			captcha = CaptchaManager.__image__.generate(letter)

			CaptchaManager.__captcha__[letter] = captcha.data

			return letter, captcha.data