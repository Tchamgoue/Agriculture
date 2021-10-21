import odoorpc
from django import forms
from django.http.request import HttpRequest
from django.shortcuts import render, redirect

# Create your views here.

# HOST = "127.0.0.1"
HOST = "62.171.170.214"
PROTOCOL = "jsonrpc"
# PORT = 8070
PORT = 8069
TIMEOUT = 360
# DB = "ipm_local_db"
DB = "agriculture_db"
# ADMIN_LOGIN = "adess.demo@gmail.com"
ADMIN_LOGIN = "admin"
# ADMIN_PASSWORD = "admin"
ADMIN_PASSWORD = "Dschang1"


def connection():
    odoo = odoorpc.ODOO(host=HOST, protocol=PROTOCOL, port=PORT, timeout=TIMEOUT)
    odoo.login(db=DB, login=ADMIN_LOGIN, password=ADMIN_PASSWORD)
    return odoo


def connect_farmer(login, passwd):
    odoo = odoorpc.ODOO(host=HOST, protocol=PROTOCOL, port=PORT, timeout=TIMEOUT)
    odoo.login(db=DB, login=login, password=passwd)
    return odoo


adminOdoo = connection()


def get_user_model():
    Users = adminOdoo.env['res.users']
    return Users


def get_partner_model():
    Partner = adminOdoo.env['res.partner']
    return Partner


# get odoo farmer model
def get_farmer_registration_model():
    FarmerRegistration = adminOdoo.env['farmer.registration.request']
    return FarmerRegistration


# get odoo crop request model
def get_crop_request_model():
    CropRequest = adminOdoo.env['farmer.cropping.request']
    return CropRequest


def get_crops_model():
    Crop = adminOdoo.env['farmer.location.crops']
    return Crop


def get_farm_location_model():
    FarmLocation = adminOdoo.env['res.partner']
    return FarmLocation


def get_farmer_model():
    Farmer = adminOdoo.env['res.partner']
    return Farmer


# decorators
def authenticate(func):
    def wrapper(request):
        if "uid" in request.session.keys():
            return func(request)
        else:
            return redirect('login')
    return wrapper


# for each views bellow we always check if user is connected or not.


def farmer_registration_view(request):
    if 'uid' in request.session:
        redirect('user_account')
    else:
        if isinstance(request, HttpRequest):
            if len(request.POST) > 0:
                FarmerRegistration = get_farmer_registration_model()
                try:
                    farmer = {
                        'name': request.POST['name'],
                        'name_local_lang': request.POST['name_local_lang'],
                        'mobile': int(request.POST['mobile']),
                        'phone': int(request.POST['phone']),
                        'email': request.POST['email']
                    }
                    farmer_id = FarmerRegistration.create(farmer)
                    farmer_number = FarmerRegistration.browse(farmer_id).number
                except Exception as e:
                    return redirect('farmer_registration')
                request.session['farmer_number'] = farmer_number
                adminOdoo.logout()
                return redirect('farmer_registration_success')
            else:
                return render(request, 'farmer_management/farmer_registration.html', {
                    "title":"Famer registration -JLK",
                    'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
                    'username': request.session['username'] if 'username' in request.session.keys() else None
                })
        else:
            print("error")


def farmer_registration_success_view(request, **kwargs):
    if 'uid' in request.session:
        redirect('user_account')
    else:
        if isinstance(request, HttpRequest):
            if len(request.POST) > 0:
                pass
            else:
                if 'farmer_number' in request.session:
                    return render(request, 'farmer_management/farmer_registration_success.html', {
                        "title":"Famer Registration-JLK",
                        'farmer_number': request.session['farmer_number'],
                        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
                        'username': request.session['username'] if 'username' in request.session.keys() else None
                    })
                else:
                    return render(request, 'farmer_management/farmer_registration_success.html', {
                        'error': 'Registration Failed',
                        "title":"Famer registration-JLK",
                        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
                        'username': request.session['username'] if 'username' in request.session.keys() else None
                    })
        else:
            print("error")


def all_farmers_view(request):
    if isinstance(request, HttpRequest):
        if len(request.POST) > 0:
            pass
        else:
            Partner = get_partner_model()
            farmer_ids = Partner.search([('is_farmer', '=', True)])
            farmers = []
            print(farmer_ids)
            for id in farmer_ids:
                farmer = Partner.browse(id)
                farmers.append(farmer)
            return render(request, 'farmer_management/all_farmers.html', {
                'title':"Famers list-JLK",
                'farmers': farmers,
                'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
                'username': request.session['username'] if 'username' in request.session.keys() else None
            })
    else:
        print("error")


def login_view(request):
    if 'uid' in request.session:
        return redirect('user_account')
    else:
        if request.method == 'POST':
            login = request.POST['email']
            password = request.POST['password']
            try:
                odoo = connect_farmer(login=login, passwd=password)
                request.session['uid'] = odoo._env.uid
                return redirect('user_account')
            except Exception as e:
                return render(request, 'farmer_management/login.html', {'error': 'Registration Failed',"title":"Login-JLK"})
        else:
            return render(request, 'farmer_management/login.html', {})


def contact_view(request):
    return render(request, 'farmer_management/contact.html', {
        "title":"Contact us-JLK",
        'contact': 'contact',
        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
        'username': request.session['username'] if 'username' in request.session.keys() else None
    })


def about_view(request):
    return render(request, 'farmer_management/about.html', {
        "title":"About-JLK",
        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
        'username': request.session['username'] if 'username' in request.session.keys() else None
    })


def user_account(request, **kwargs):
    # get user account state on odoo "confirm" or "not"
    if 'uid' in request.session:
        uid = int(request.session['uid'])
        Users = get_user_model()
        user = Users.browse(int(uid))
        Partner = get_partner_model()
        farmer = {}
        if user:
            request.session['username'] = user.name
            farmer = Partner.browse(int(user.partner_id))
            Crop = get_crops_model()
            crops = Crop.search([])
            FarmLocation = get_farm_location_model()
            farm_location = FarmLocation.search([('is_location', '=', True)])
            CropRequest = get_crop_request_model()
            crop_requests = CropRequest.search([('user_id', '=', int(uid))])
            farmers = Partner.search([
                ('id', '!=', int(uid)),
                ('is_farmer', '=', True)
            ])
            if farmer.is_farmer:
                return render(request, 'farmer_management/user_account.html', {
                    "title":"User account-JLK",
                    'status': 'confirmed' if user else 'unconfirmed',
                    'uid': uid,
                    'user': user,
                    'username': request.session['username'] if 'username' in request.session.keys() else None,
                    'farmer': farmer[0] if farmer else None,
                    'crops_count': len(crops),
                    'farm_location_count': len(farm_location),
                    'crop_requests_count': len(crop_requests),
                    'farmers_count': len(farmers)
                })
            else:
                return redirect('login')
    else:
        return redirect('login')


def logout(request, **kwargs):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect('home')

@authenticate
def new_crop_request(request):
    uid = request.session['uid'] if 'uid' in request.session.keys() else None
    if request.method == 'POST':
        Crop = get_crops_model()
        crops = Crop.search([])
        f_crops = []
        for crop_id in crops:
            crop = Crop.browse(crop_id)
            f_crops.append(crop)

        crop_ids = int(request.POST["crop_id"])
        description = request.POST['description']
        end_date = request.POST['start_date']
        start_date = request.POST['end_date']
        name = request.POST['name']

        values = {
            "user_id": uid,
            "crop_ids": crop_ids,
            # TODO add fields to get warehouse and location information
            # "warehouse_id": int(request.POST['warehouse_id']),
            # "location_id": int(request.POST['location_id']),
            "description": description,
            "end_date": end_date,
            "start_date": start_date,
            "name": name
        }
        # write value
        if crop_ids and description \
                and end_date and start_date \
                and name:
            CropRequest = get_crop_request_model()
            res = CropRequest.create(values)
        else:
            res = None
        return render(request, 'farmer_management/new_crop_request.html', {
            "title":"Crops request-JLK",
            'crops': f_crops,
            'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
            'username': request.session['username'] if 'username' in request.session.keys() else None,
            'error': 'error creating request' if not res else None,
            'success': 'Request submitted successfully' if res else None
        })
    else:
        Crop = get_crops_model()
        crops = Crop.search([])
        f_crops = []
        for crop_id in crops:
            crop = Crop.browse(crop_id)
            f_crops.append(crop)
        return render(request, 'farmer_management/new_crop_request.html', {
            "title":"Crop request -JLK",
            'crops': f_crops,
            'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
            'username': request.session['username'] if 'username' in request.session.keys() else None
        })


def farmer_crops(request):
    Crop = get_crops_model()
    crops = Crop.search([])
    f_crops = []
    for crop_id in crops:
        crop = Crop.browse(crop_id)
        f_crops.append(crop)
    return render(request, 'farmer_management/farmer_crops.html', {
        "title":"Farmer Crops-JLK",
        'crops': f_crops,
        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
        'username': request.session['username'] if 'username' in request.session.keys() else None
    })


def farmer_farms(request):
    Farms = get_farm_location_model()
    farms = Farms.search([('is_location','=',True)])
    f_farms = []
    for f_id in farms:
        farm = Farms.browse(f_id)
        farm.count_crop = len(farm.crop_ids)
        f_farms.append(farm)
    return render(request, 'farmer_management/farmer_farms.html', {
        "title":"Farmer fams-JLK",
        'farms': f_farms,
        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
        'username': request.session['username'] if 'username' in request.session.keys() else None
    })

@authenticate
def farmer_requests(request):
    uid = request.session['uid'] if 'uid' in request.session.keys() else None
    Crops = get_crop_request_model()
    c_rs = Crops.search([('user_id', '=', int(uid))])
    f_cr = []
    for cr_id in c_rs:
        cr = Crops.browse(cr_id)
        f_cr.append(cr)
    return render(request, 'farmer_management/farmer_crop_requests.html', {
        "title":"Crops request-JLK",
        'crop_requests':f_cr,
        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
        'username': request.session['username'] if 'username' in request.session.keys() else None
    })


@authenticate
def crops_registration_view(request):
    if isinstance(request, HttpRequest):
        if len(request.POST) > 0:
            crop = forms.CropsRegistration(request.POST)
            if crop.is_valid():
                print("ok")
            else:
                print(crop.data)
                return render(request, "farmer_management/crops_registration.html", {
                    'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
                    'username': request.session['username'] if 'username' in request.session.keys() else None
                })
        else:
            return render(request, "farmer_management/crops_registration.html", {
                "title":"Crops registration-JLK",
                'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
                'username': request.session['username'] if 'username' in request.session.keys() else None
            })
    else:
        return redirect('home')


@authenticate
def farm_location_registration_view(request):
    if isinstance(request, HttpRequest):
        if len(request.POST) > 0:
            crop = forms.CropsRegistration(request.POST)
            if crop.is_valid():
                print("ok")
            else:
                print(crop.data)
                return render(request, "farmer_management/crops_registration.html", {
                    'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
                    'username': request.session['username'] if 'username' in request.session.keys() else None,
                    "title":"Crops registration-JLK"
                })
        else:
            return render(request, "farmer_management/crops_registration.html", {
                'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
                'username': request.session['username'] if 'username' in request.session.keys() else None,
                "title":"Crops registration-JLK"
            })
    else:
        return redirect('home')

@authenticate
def agro_similarity_view(request):
    return render(request,"farmer_management/agro_similarity.html",{
        "uid":request.session.get("uid",None),
        "username":request.session.get("username",None),
        "title":"Similarity-JLK"
    })
    
