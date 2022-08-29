# import libraries
from textblob import TextBlob, Word
from flask import Flask, render_template, request

# initalise app
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/translate')
def translate():
    return render_template('translate.html')

@app.route('/translated', methods=['post'])
def translated():
    from_lang = request.form.get('from_lang')
    to_lang = request.form.get('to_lang')
    text = request.form.get('text')

    text = TextBlob(text)
    output = text.translate(from_lang = from_lang, to = to_lang)

    return render_template('translate.html', input=text, output=output)

@app.route('/spell_check')
def spell_check():
    return render_template('spell_check.html')

@app.route('/corrected', methods=['post'])
def corrected():
    text = request.form.get('text')

    input_text = TextBlob(text)
    correct_text = input_text.correct()

    # Show top 3 other possible correct words
    other_words= ''
    if len(input_text.words) == 1:
        words = Word(text).spellcheck()[1:4]
        if len(words) != 0:
            other_words = [w[0] for w in words]
            other_words = f'Other possible words : {other_words}'

    return render_template('spell_check.html', input=text, output=correct_text, other_words=other_words)

@app.route('/word_counter')
def counter():
    return render_template('word_counter.html')

@app.route('/counted', methods=['post'])
def counted():
    text = str(request.form.get('text'))

    text = TextBlob(text)
    text = text.replace('\r','')  # html text had '\r' (carriage return) at end of every line. So remove.

    words = len(text.words)
    sents = len(text.sentences)

    chars = 0
    paras = 0
    for i in text.split(sep='\n'):
        if len(i) != 0:
            paras += 1
        chars += len(i)

    return render_template('word_counter.html', input=text, chars=chars, words=words, sents=sents, paras=paras )

app.run(debug=True)