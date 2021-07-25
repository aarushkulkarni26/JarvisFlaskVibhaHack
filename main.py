from flask import Flask, render_template, request
import wolframalpha
import requests
import wikipedia
import pyttsx3
import math
# import pyttsx3
app = Flask(__name__)
# engine = pyttsx3.init()
# engine.say('hello')
# engine.runAndWait()
def speak(text):
  engine = pyttsx3.init()
  engine.say(text)
  rate = engine.getProperty('rate')
  engine.setProperty('rate', 100)
  print(rate)
  engine.runAndWait()
answer=''
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
      query = request.form.get('query')
      if 'weather' in query:
        res = requests.get('https://api.openweathermap.org/data/2.5/weather?q=massachusetts&appid=c021529d0b3016bbed9a8ab4a6150631')
        json = res.json()
        ans = json['main']['temp']
        def kel_to_far(kel):
          kel_273 = kel - 273.15
          far = kel_273 * 9/5 + 32
          ans = math.floor(far)
          return ans
        answer = f'{kel_to_far(ans)}F'
      if 'who is' in query:
        wikipedia.summary("Facebook", sentences=1)
      else:
        lower_query = query.lower()
        client = wolframalpha.Client('VWT5QG-5E4H3T6LHQ')
        res = client.query(lower_query)
        answer = next(res.results).text
      speak(answer)
      return render_template('answer.html', answer=answer)
    return render_template("index.html")

@app.route('/math',methods=['GET', 'POST'])
def math_page():
    if request.method == "POST":
      query = request.form.get('query')
      lower_query = query.lower()
      client = wolframalpha.Client('VWT5QG-5E4H3T6LHQ')
      res = client.query(lower_query)
      answer = next(res.results).text
      speak(answer)
      return render_template('answer.html', answer=answer)
    return render_template("math.html")
@app.route('/people',methods=['GET', 'POST'])
def people():
  if request.method == "POST":
    query = request.form.get('query')
    answer = wikipedia.summary(query,sentences=1)
    speak(answer)
    return render_template('answer.html', answer=answer)
  return render_template('people.html')
@app.route('/team')
def team():
    return render_template('team.html')
@app.route('/weather',methods=['GET', 'POST'])
def weather():
  if request.method == "POST":
    query = request.form.get('query')
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={query}&appid=c021529d0b3016bbed9a8ab4a6150631')
    json = res.json()
    ans = json['main']['temp']
    def kel_to_far(kel):
      kel_273 = kel - 273.15
      far = kel_273 * 9/5 + 32
      ans = math.floor(far)
      return ans
    answer = f'{kel_to_far(ans)}F'
    speak(answer)
    return render_template('answer.html', answer=answer)
  return render_template('weather.html')
@app.route('/science',methods=['GET', 'POST'])
def science():
  if request.method == "POST":
    query = request.form.get('query')
    answer = wikipedia.summary(query,sentences=1)
    speak(answer)
    return render_template('answer.html', answer=answer)
  return render_template('science.html')
  
app.run(port=5000, debug=True)
