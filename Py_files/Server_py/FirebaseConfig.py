import pyrebase

configuracion = {
    "apiKey": "AIzaSyCOrf0ICAsZ8tfqrLmCzMObyjFb75uotAE",
    "authDomain": "tvpost-d2d68.firebaseapp.com",
    "databaseURL": "https://tvpost-d2d68-default-rtdb.firebaseio.com/",
    "projectId": "tvpost-d2d68",
    "storageBucket": "tvpost-d2d68.appspot.com",
    "messagingSenderId": "483684083896",
    "appId": "1:483684083896:web:db53ac7c6c90dd7ba96c4d",
    "measurementId": "G-H15VK4PNKB"
}

def GetInitialization():
    return pyrebase.initialize_app(configuracion)