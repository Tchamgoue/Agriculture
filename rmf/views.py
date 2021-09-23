from django.shortcuts import render, redirect
from django.http.request import HttpRequest
import odoorpc
import pprint


# Create your views here.

def connection():
    odoo = odoorpc.ODOO(host='62.171.170.214', protocol='jsonrpc', port=8069, timeout=360)
    odoo.login('agriculture_db', 'admin', 'Dschang1')
    Farmer = odoo.env['farmer.registration.request']
    return odoo, Farmer


def farmer_registration_view(request):
    if isinstance(request, HttpRequest):
        if len(request.POST) > 0:
            odoo, Farmer = connection()

            try:
                farmer = {
                    'name': request.POST['name'],
                    'name_local_lang': request.POST['name_local_lang'],
                    'mobile': int(request.POST['mobile']),
                    'phone': int(request.POST['phone']),
                    'email': request.POST['email']
                }

                farmer_id = Farmer.create(farmer)
                farmer_number = Farmer.browse(farmer_id).number

            except ValueError:
                return redirect('farmer_registration')

            request.session['farmer_number'] = farmer_number
            odoo.logout()
            return redirect('farmer_registration_success')
        else:
            return render(request, 'rmf/farmer_registration.html')
    else:
        print("error")


def farmer_registration_success_view(request, **kwargs):
    if isinstance(request, HttpRequest):
        if len(request.POST) > 0:
            pass
        else:
            if 'farmer_number' in request.session:
                return render(request, 'rmf/farmer_registration_success.html',
                              {'farmer_number': request.session['farmer_number']})
            else:
                return render(request, 'rmf/farmer_registration_success.html', {'error': 'Registration Failed'})
    else:
        print("error")


def all_farmers_view(request):
    if isinstance(request, HttpRequest):
        if len(request.POST) > 0:
            pass
        else:
            odoo, Farmer = connection()
            farmer_ids = Farmer.search([])
            farmers = []
            print(farmer_ids)
            for id in farmer_ids:
                farmer = Farmer.browse(id)
                print(farmer)
                farmers.append(farmer)
            return render(request, 'rmf/all_farmers.html', {'farmers': farmers})
    else:
        print("error")

def login_view(request):
     return render(request, 'rmf/login.html', {'error': 'Registration Failed'})
    #return redirect('admin_farmer/pages/list_farmers.html')


def contact_view(request):
    return render(request, 'rmf/contact.html', {'contact': 'contact'})

    
def about_view(request):
    return render(request, 'rmf/about.html')



