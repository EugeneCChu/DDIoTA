import speech_recognition as sr
import time

def transcribe():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		
		print('Speak into the microphone:')
		audio = r.listen(source)

	#t1 = time.time()
	#print('Start recognizing.')

	try:
		text = r.recognize_google(audio)
		print('-'*(len(text)+17))
		print('|'+'Transcription: {}'.format(text)+'|')
		print('-'*(len(text)+17))
		#t2 = time.time()
		#print('Total transcription time is: %.2fs' %(t2-t1))
		return text
	except sr.UnknownValueError:
		print("Audio Intelligible")
		return "Audio Intelligible"
	except sr.RequestError as e:
		print('Can not obtain results: {0}'.format(e))
		return 'Can not obtain results'
	
	

if __name__ == '__main__':
	out_msg = ''
	while 'exit the program' not in out_msg:
		out_msg = transcribe()
		#print(out_msg)
	print('Thank you for using the system, please pay 100 dollars.')
