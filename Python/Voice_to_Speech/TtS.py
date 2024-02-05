import pyttsx3

bot = pyttsx3.init()
contain = input("say: ")
voices = bot.getProperty("voices")
bot.setProperty("voice", voices[1].id)
bot.say(contain)
bot.runAndWait()
