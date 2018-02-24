from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from InventoryApp.views import *

urlpatterns = [
	url(r'^login/',csrf_exempt(login),name = 'login'),
    url(r'^add_employee/',csrf_exempt(add_employee),name = 'add_employee'),
    url(r'^update_employee/',csrf_exempt(update_employee),name = 'update_employee'),
    url(r'^get_employee/',csrf_exempt(get_employee),name = 'get_employee'),
    url(r'^search_employee/',csrf_exempt(search_employee),name = 'search_employee'),
    url(r'^get_departments/',csrf_exempt(get_departments),name = 'get_departments'),
    url(r'^get_emplocation/',csrf_exempt(get_emplocation),name = 'get_emplocation'),
    url(r'^get_empjobrole/',csrf_exempt(get_empjobrole),name = 'get_empjobrole'),
    url(r'^get_hr/',csrf_exempt(get_hr),name = 'get_hr'),
    url(r'^get_user/',csrf_exempt(get_user),name = 'get_user'),
    url(r'^add_userrole/',csrf_exempt(add_userrole),name = 'add_userrole'),
    url(r'^update_userrole/',csrf_exempt(update_userrole),name = 'update_userrole'),
    url(r'^forget_password/',csrf_exempt(forget_password),name = 'forget_password'),
    url(r'^add_familydetails/',csrf_exempt(add_familydetails),name = 'add_familydetails'),
    url(r'^update_familydetails/',csrf_exempt(update_familydetails),name = 'update_familydetails'),
    url(r'^get_familydetails/',csrf_exempt(get_familydetails),name = 'get_familydetails'),
    url(r'^add_warehouse/', csrf_exempt(add_warehouse),name = 'add_warehouse'),
    url(r'^get_warehouse/',csrf_exempt(get_warehouse),name = 'get_warehouse'),
    url(r'^active_warehouse/',csrf_exempt(active_warehouse),name = 'active_warehouse'),
    url(r'^del_warehouse/',csrf_exempt(del_warehouse),name = 'del_warehouse'),
    url(r'^update_warehouse/',csrf_exempt(update_warehouse),name = 'update_warehouse'),
    url(r'^add_location/',csrf_exempt(add_location),name = 'add_location'),
    url(r'^get_location/',csrf_exempt(get_location),name = 'get_location'),
    url(r'^active_location/',csrf_exempt(active_location),name = 'active_location'),
    url(r'^del_location/',csrf_exempt(del_location),name = 'del_location'),
    url(r'^update_location/',csrf_exempt(update_location),name = 'update_location'),
    url(r'^add_status/',csrf_exempt(add_status),name = 'add_status'),
    url(r'^get_status/',csrf_exempt(get_status),name = 'get_status'),
    url(r'^update_status/',csrf_exempt(update_status),name = 'update_status'),
    url(r'^add_product/',csrf_exempt(add_product),name = 'add_product'),
    url(r'^add_productquantity/',csrf_exempt(add_productquantity),name = 'add_productquantity'),
    url(r'^update_productquantity/',csrf_exempt(update_productquantity),name = 'update_productquantity'),
    url(r'^get_productquantity/',csrf_exempt(get_productquantity),name = 'get_productquantity'),
    url(r'^update_product/',csrf_exempt(update_product),name = 'update_product'),
    url(r'^get_product/',csrf_exempt(get_product),name = 'get_product'),
    url(r'^get_productcategory/',csrf_exempt(get_productcategory),name = 'get_productcategory'),
    url(r'^active_product/',csrf_exempt(active_product),name = 'active_product'),
    url(r'^search_product/',csrf_exempt(search_product),name = 'search_product'),
    url(r'^del_product/',csrf_exempt(del_product),name = 'del_product'),
    url(r'^get_category/',csrf_exempt(get_category),name = 'get_category'),
    url(r'^add_position/', csrf_exempt(add_position),name = 'add_position'),
    url(r'^update_position/', csrf_exempt(update_position),name = 'update_position'),
    url(r'^get_position/',csrf_exempt(get_position),name = 'get_position'),
    url(r'^active_position/',csrf_exempt(active_position),name = 'active_position'),
    url(r'^del_position/',csrf_exempt(del_position),name = 'del_position'),
    url(r'^get_materialtype/',csrf_exempt(get_materialtype),name = 'get_materialtype'),
	url(r'^get_uom/',csrf_exempt(get_uom),name = 'get_uom'),
	url(r'^add_requisition/',csrf_exempt(add_requisition),name = 'add_requisition'),
	url(r'^del_requisition/',csrf_exempt(del_requisition),name = 'del_requisition'),
	url(r'^get_requisition/',csrf_exempt(get_requisition),name = 'get_requisition'),
	url(r'^get_newrequisition/',csrf_exempt(get_newrequisition),name = 'get_newrequisition'),
	url(r'^add_requisitiondetails/',csrf_exempt(add_requisitiondetails),name = 'add_requisitiondetails'),
	url(r'^get_requisitiondetails/',csrf_exempt(get_requisitiondetails),name = 'get_requisitiondetails'),
	url(r'^get_storerequisition/',csrf_exempt(get_storerequisition),name = 'get_storerequisition'),
	url(r'^get_todayrequisition/',csrf_exempt(get_todayrequisition),name = 'get_todayrequisition'),
	url(r'^get_storerequisitiondetails/',csrf_exempt(get_storerequisitiondetails),name = 'get_storerequisitiondetails'),
    url(r'^get_zerorequisitiondetails/',csrf_exempt(get_zerorequisitiondetails),name = 'get_zerorequisitiondetails'),
	url(r'^update_requisition/',csrf_exempt(update_requisition),name = 'update_requisition'),
	url(r'^update_requisitiondetails/',csrf_exempt(update_requisitiondetails),name = 'update_requisitiondetails'),
]
