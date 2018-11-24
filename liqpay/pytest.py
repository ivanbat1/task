from googletrans import Translator
import win32com.client as wincl
translator = Translator()



a=translator.translate(u'안녕하세요.')
a=translator.translate('I am robot',src='en',dest='hi')
print (a.text)
speak = wincl.Dispatch("SAPI.SpVoice")
speak.Speak(a.text)