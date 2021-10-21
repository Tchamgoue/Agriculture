from django.shortcuts import render, redirect
from django.http.request import HttpRequest
import odoorpc


# Create your views here.

def connection(model='farmer.registration.request'):
    odoo = odoorpc.ODOO(host='localhost', protocol='jsonrpc', port=8069, timeout=360)
    odoo.login('custom_hr', 'admin', 'admin')
    model = odoo.env[model]
    return odoo, model


def add_crops_to_farm(request):
    if isinstance(request, HttpRequest):
        if len(request.POST) > 0:
            Crops = connection(model='farmer.location.crops')[1]
            Warehouse = connection(model='stock.warehouse')[1]
            Location = connection(model='stock.location')[1]

            # warehouse = Warehouse.browse(int(request.POST['warehouse_id']))
            # location = Location.browse(int(request.POST['location_id']))

            crop = {
                'name': request.POST['name'],
                'crop_period_start': request.POST['crop_period_start'],
                'crop_period_end': request.POST['crop_period_end'],
                'warehouse_id': int(request.POST['warehouse_id']),
                'location_id': int(request.POST['location_id']),
            }

            Crops.create(crop)

            crop_ids = Crops.search([])
            crops = []
            for id in crop_ids:
                crops.append(Crops.browse(id))

            # print(crops)
            print(request.POST)
            return redirect('farm_crops')
        else:
            Crops = connection(model='farmer.location.crops')[1]
            Warehouse = connection(model='stock.warehouse')[1]
            Location = connection(model='stock.location')[1]
            crop_ids = Crops.search([])
            warehouse_ids = Warehouse.search([])
            location_ids = Location.search([])
            crops = []
            for id in crop_ids:
                crop = Crops.read(id)
                print(crop)
                crops.append(crops)

            warehouses = []
            for id in warehouse_ids:
                warehouse = Warehouse.read(id)
                print(warehouse)
                warehouses.append(warehouse)

            locations = []
            for id in location_ids:
                location = Location.read(id)
                print(location)
                locations.append(location)

            return render(request, 'farm/farm_crops.html',
                          {'crops': crops, 'warehouses': warehouses, 'locations': locations,"title":"Crops-JLK"})
    else:
        return redirect('home')


def add_farm_location(request):
    if isinstance(request, HttpRequest):
        if len(request.POST) > 0:
            Crops = connection(model='farmer.location.crops')[1]

            # warehouse = Warehouse.browse(int(request.POST['warehouse_id']))
            # location = Location.browse(int(request.POST['location_id']))

            crop_ids = Crops.search([])
            crops = []
            for id in crop_ids:
                crops.append(Crops.read(id))

            # print(crops)
            print(request.POST)
            return redirect('farm_location')
        else:
            Crops = connection(model='farmer.location.crops')[1]

            crop_ids = Crops.search([])
            crops = []
            for id in crop_ids:
                crop = Crops.read(id)
                # print(crop)
                crops.append(crop)
            print(crops[0])
            return render(request, 'farm/farm_plantation.html', {'crops': crops,"title":"Farm-JLK"})
    else:
        return redirect('home')
