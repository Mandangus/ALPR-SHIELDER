import base64
from flask import Flask, Response, request
from flask_restful import Api
from flask_cors import CORS
import engineALPR as recon
from PIL import Image
from io import BytesIO
from openalpr import Alpr 
import numpy as np


app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route('/alpr',methods = ['GET','POST'])
def alpr():
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        # ----- SECTION 1 -----  
        #File naming process for nameless base64 data.
        #We are using the timestamp as a file_name.
        from datetime import datetime
        dateTimeObj = datetime.now()
        file_name_for_base64_data = dateTimeObj.strftime("%d-%b-%Y--(%H-%M-%S)")

        # ----- SECTION 2 -----
        try:
            # Base64 DATA JPG
            if "data:image/jpeg;base64," in data:
                base_string = data.replace("data:image/jpeg;base64,", "")
                decoded_img = base64.b64decode(base_string)
                img = Image.open(BytesIO(decoded_img))

                file_name = file_name_for_base64_data + ".jpg"
                img.save(file_name, "jpeg")

            # Base64 DATA PNG
            elif "data:image/png;base64," in data:
                base_string = data.replace("data:image/png;base64,", "")
                decoded_img = base64.b64decode(base_string)
                img = Image.open(BytesIO(decoded_img))

                file_name = file_name_for_base64_data + ".png"
                img.save(file_name, "png")
            
        # ----- SECTION 3 -----    
            status = "Image has been succesfully sent to the server."
        except Exception as e:
            status = "Error! = " + str(e)
            return status
            
        alpr = Alpr("gb", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data/")
        image = Image.open(file_name)
        arr = np.array(image)
        result = alpr.recognize_ndarray(arr)
        resultado = recon.main_image_procedure(file_name)
        print("\n" + str(result) + "\n")
        if type(resultado) == tuple:
            resultado_bytes = str.encode(resultado[0])
        else:
            resultado_bytes = str.encode(resultado)

        response = Response(resultado_bytes,200,content_type='text/plain')
        return response

    if request.method == 'GET':
        return "OK"



if __name__ == '__main__':
    app.run()