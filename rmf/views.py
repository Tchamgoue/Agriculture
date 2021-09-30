import odoorpc
from django.http.request import HttpRequest
from django.shortcuts import render, redirect

# Create your views here.

HOST = "127.0.0.1"
# HOST = "62.171.170.214"
PROTOCOL = "jsonrpc"
PORT = 8070
# PORT = 8069
TIMEOUT = 360
DB = "ipm_local_db"
# DB = "agriculture_db"
ADMIN_LOGIN = "adess.demo@gmail.com"
ADMIN_PASSWORD = "admin"


def connection():
    odoo = odoorpc.ODOO(host=HOST, protocol=PROTOCOL, port=PORT, timeout=TIMEOUT)
    odoo.login(db=DB, login=ADMIN_LOGIN, password=ADMIN_PASSWORD)
    return odoo


def connect_farmer(login, passwd):
    odoo = odoorpc.ODOO(host=HOST, protocol=PROTOCOL, port=PORT, timeout=TIMEOUT)
    odoo.login(db=DB, login=login, password=passwd)
    return odoo


def get_user_model():
    odoo = connection()
    Users = odoo.env['res.users']
    return odoo, Users


def get_partner_model():
    odoo = connection()
    Partner = odoo.env['res.partner']
    return odoo, Partner


# get odoo farmer model
def get_farmer_registration_model():
    odoo = connection()
    FarmerRegistration = odoo.env['farmer.registration.request']
    return odoo, FarmerRegistration

# get odoo crop request model
def get_crop_request_model():
    odoo = connection()
    CropRequest = odoo.env['farmer.cropping.request']
    return odoo, CropRequest


def get_crops_model():
    odoo = connection()
    Crop = odoo.env['farmer.location.crops']
    return odoo, Crop


def get_farm_location_model():
    odoo = connection()
    FarmLocation = odoo.env['res.partner']
    return odoo, FarmLocation


def get_farmer_model():
    odoo = connection()
    Farmer = odoo.env['res.partner']
    return odoo, Farmer


# for each views bellow we always check if user is connected or not.


def farmer_registration_view(request):
    if 'uid' in request.session:
        redirect('user_account')
    else:
        if isinstance(request, HttpRequest):
            if len(request.POST) > 0:
                odoo, FarmerRegistration = get_farmer_registration_model()
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
                odoo.logout()
                return redirect('farmer_registration_success')
            else:
                return render(request, 'rmf/farmer_registration.html', {
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
                    return render(request, 'rmf/farmer_registration_success.html', {
                        'farmer_number': request.session['farmer_number'],
                        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
                        'username': request.session['username'] if 'username' in request.session.keys() else None
                    })
                else:
                    return render(request, 'rmf/farmer_registration_success.html', {
                        'error': 'Registration Failed',
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
            odoo, Partner = get_partner_model()
            farmer_ids = Partner.search([('is_farmer','=',True)])
            farmers = []
            print(farmer_ids)
            for id in farmer_ids:
                farmer = Partner.browse(id)
                print(farmer)
                farmers.append(farmer)
            return render(request, 'rmf/all_farmers.html', {
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
                return render(request, 'rmf/login.html', {'error': 'Registration Failed'})
        else:
            return render(request, 'rmf/login.html', {})


def contact_view(request):
    return render(request, 'rmf/contact.html', {
        'contact': 'contact',
        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
        'username': request.session['username'] if 'username' in request.session.keys() else None
    })


def about_view(request):
    return render(request, 'rmf/about.html', {
        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
        'username': request.session['username'] if 'username' in request.session.keys() else None
    })


def user_account(request, **kwargs):
    # get user account state on odoo "confirm" or "not"
    if 'uid' in request.session:
        uid = int(request.session['uid'])
        odoo, Users = get_user_model()
        user = Users.browse(int(uid))
        odoo, Partner = get_partner_model()
        farmer = {}
        if user:
            request.session['username'] = user.name
            farmer = Partner.browse(int(user.partner_id))
            odoo, Crop = get_crops_model()
            crops = Crop.search([])
            odoo, FarmLocation = get_farm_location_model()
            farm_location = FarmLocation.search([('is_location', '=', True)])
            odoo, CropRequest = get_crop_request_model()
            crop_requests = CropRequest.search([('user_id', '=', int(uid))])
            farmers = Partner.search([
                ('id', '!=', int(uid)),
                ('is_farmer', '=', True)
            ])
            if farmer.is_farmer:
                return render(request, 'rmf/user_account.html', {
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
    return redirect('/')


def new_crop_request(request):
    return render(request, 'rmf/new_crop_request.html', {
        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
        'username': request.session['username'] if 'username' in request.session.keys() else None
    })


def farmer_crops(request):
    odoo, Crop = get_crops_model()
    crops = Crop.search([])
    f_crops = []
    for crop_id in crops:
        crop = Crop.browse(crop_id)
        f_crops.append(crop)
    return render(request, 'rmf/farmer_crops.html', {
        'crops': f_crops,
        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
        'username': request.session['username'] if 'username' in request.session.keys() else None
    })


def farmer_farms(request):
    return render(request, 'rmf/farmer_farms.html', {
        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
        'username': request.session['username'] if 'username' in request.session.keys() else None
    })


def farmer_requests(request):
    return render(request, 'rmf/farmer_crop_requests.html', {
        'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
        'username': request.session['username'] if 'username' in request.session.keys() else None
    })
