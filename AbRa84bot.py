import random
import qrcode
from datetime import date
from khayyam import JalaliDate, JalaliDatetime  # تقویم شمسی
import telebot
import gtts  # تبدیل متن به صدا # pip install gtts
from telebot import types  # Reply markup برای
my_keyboard = types.ReplyKeyboardMarkup(row_width=1)
key1 = types.KeyboardButton('/game')


bot = telebot.TeleBot("5813893842:AAFYCn2BWl3ZfF_KXcDtxn44iU-i85i9JMU", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
computer_number=random.randint(1,5)
@bot.message_handler(commands=['start'])
def welcome(message):
  welcome = ( "سلام "+ message.from_user.first_name+"عزیز\n خوش آمدید")
  bot.send_message(message.chat.id,welcome)
  bot.send_message(message.chat.id,"\n /game: بازی حدس عدد\n /age: تبدیل تاریخ تولد به تعداد روز \n /voice: تبدیل متن به صدا "+
	    "\n /max: چاپ بزرگترین عدد از یک لیست \n /argmax : چاپ اندیس بزرگترین عدد لیست \n /qrcode: QrCode تبدیل رشته حروف به ")


	
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id,"/game: بازی حدس عدد\n /age: تبدیل تاریخ تولد به تعداد روز \n /voice: تبدیل متن به صدا "+
	    "\n /max: چاپ بزرگترین عدد از یک لیست \n /argmax : چاپ اندیس بزرگترین عدد لیست \n /qrcode: QrCode تبدیل رشته حروف به ")

#----------------------------------------------------- بازی حدس عدد ----------------------------------------
@bot.message_handler(commands=['game'])
def start_game(message):
   my_keyboard.add(key1)
   msg=bot.send_message(message.chat.id,"یک عدد بین 1 و 5 وارد کنید :" ,reply_markup=my_keyboard)
   bot.register_next_step_handler(msg, game )

def game(message):
   global computer_number
   test_int=(message.text).isdigit()  
   if test_int==False:
    bot.send_message(message.chat.id,"لطفا فقط عدد وارد نمایید")

   if int(message.text)>computer_number:
     msg2=bot.send_message(message.chat.id,"برو پایین")
     bot.register_next_step_handler(msg2, game )

   elif int(message.text)<computer_number: 
      msg2=bot.send_message(message.chat.id,"برو بالا")  
      bot.register_next_step_handler(msg2, game )

   elif int(message.text)==computer_number: 
      msg2=bot.send_message(message.chat.id,"شما برنده شدید")   
      bot.register_next_step_handler(msg2, game )
#-------------------------------------------------------  محاسبه تاریخ تولد به تعداد روز ----------------
@bot.message_handler(commands=['age']) 
def date_birth(message):
 birth=bot.send_message(message.chat.id,"تاریخ تولد را وارد نمایید:\n  (با فرمت: روز/ماه/سال)  ") 
 bot.register_next_step_handler(birth, days)
def days(message):   
   birth_date_list=(message.text).split("/")
   year=birth_date_list[0]
   month=birth_date_list[1]
   day=birth_date_list[2]
   year=int(year)
   month=int(month)
   day=int(day)
   cal_day=JalaliDate.today()-JalaliDate(year,month,day) 
   bot.send_message(message.chat.id, cal_day)
   bot.register_next_step_handler(date, days )
#-------------------------------------------------  تبدیل متن به ویس  --------------
@bot.message_handler(commands=['voice'])
def text_to_voice(message):
 text=bot.send_message(message.chat.id, "متن خود را به انگلیسی وارد نمایید :")
 bot.register_next_step_handler(text, voice)
def voice(message):
  my_text=(message.text)
  x=gtts.gTTS(my_text, lang="en", slow=False)
  x.save("voice.mp3")  
  f = open("voice.mp3",'rb')
  bot.send_audio(message.chat.id,f)
#-------------------------------------------------------چاپ بزرگترین عدد از یک لیست ---------------  

@bot.message_handler(commands=['max'])
def list_num(message):
  num=bot.send_message(message.chat.id, "  عددهای مورد نظر را وارد نمایید : \n ( num1,num2,num3,... )")    
  bot.register_next_step_handler(num, max)
  
def max(message):
 list=(message.text).split(",")
 max_num = 0
 for number in list:
   if max_num<int(number):
    max_num = int(number)
    txt = f"بزرگترین عدد لیست :{max_num}"
 bot.send_message(message.chat.id, txt)

#-------------------------------------------------------چاپ اندیس بزگترین عدد لیست--------------------------------  
@bot.message_handler(commands=['argmax'])
def list_num(message):
  num=bot.send_message(message.chat.id, "  عددهای مورد نظر را وارد نمایید : \n ( num1,num2,num3,... )")    
  bot.register_next_step_handler(num, argmax)
  
def argmax(message):
 list=(message.text).split(",")
 max_num = 0
 i=0
 for number in list:
   if max_num<int(number):
      max_num = int(number)
      index = i
   i += 1
 txt = f"اندیس بزرگترین عدد :{index}"  
 bot.send_message(message.chat.id, txt)
#-------------------------------------------------------تبدیل متن ورودی به QrCode-------------------------------  
@bot.message_handler(commands=['qrcode'])
def text_to_qrcode(message):
 text=bot.send_message(message.chat.id, "متن خود را وارد نمایید :")
 bot.register_next_step_handler(text, text_to_qrcode)
def text_to_qrcode(message):
  my_text=(message.text)
  img=qrcode.make(my_text)
  img.save("QrCode.jpg")
  f = open("QrCode.jpg",'rb')
  bot.send_photo(message.chat.id,f)



bot.infinity_polling()    
	  