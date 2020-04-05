from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/image',methods = ['POST', 'GET'])
def image():
   if request.method == 'POST':
      user = request.form['file']
      #print(user)
      return redirect(url_for('success',name = "Vandit"))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)