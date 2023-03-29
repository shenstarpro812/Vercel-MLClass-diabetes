from flask import Flask,request,render_template
import urllib
import json

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("templates/form.html")

@app.route('/aml', methods=['GET','POST'])
def aml():
    data =  {
    "Inputs": {
        "input1": [       
        {
            "Pregnancies": request.values['p1'],
            "Glucose": request.values['p2'],
            "BloodPressure": request.values['p3'],
            "SkinThickness": request.values['p4'],
            "Insulin": request.values['p5'],
            "BMI": request.values['p6'],
            "DiabetesPedigreeFunction": request.values['p7'],
            "Age": request.values['p8'],
            "Outcome": 1
        }
        ]
    },
    "GlobalParameters": {}
    }

    body = str.encode(json.dumps(data))

    url = 'http://6f57411f-c6bf-4b5b-b532-d42d944114e1.southeastasia.azurecontainer.io/score'
    # Replace this with the primary/secondary key or AMLToken for the endpoint
    api_key = 'MdjPyoyzwjY5IRYQ0HcLIgFGLHrfcrlS'

    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")


    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    htmlstr="<html><body>"

    try:
        response = urllib.request.urlopen(req)

        result = json.loads(response.read())
        htmlstr=htmlstr+"依據您輸入的參數，經過數據分析模型比對，罹患糖尿病的機率為"
        htmlstr=htmlstr+str(result['Results']['WebServiceOutput0'][0]['Scored Labels'])
        # print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        # print(json.load(error.read().decode("utf8", 'ignore')))

    htmlstr=htmlstr+"</body></html>"

    # return "hello"
    return htmlstr

@app.route('/about')
def about():
    return 'About'