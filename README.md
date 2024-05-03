# Important commads for working on this project

1) python manage.py runserver       --      run the server,              
2) python manage.py makemigrations  --      for making the migrations,
3) python manage.py sqlmigrate <app_name><migration_filenumber>     -- you will get the sql query,
4) python migrate       --         it will create the models in the local_server of the postgresql,

# These apis is secured with superuser
python manage.py createsuperuser  -- please create the superuser and then run the endpoints

# API endpoints
1) Create a new vendor:                                 
http://127.0.0.1:8000/POST/api/vendors/       


2) List all the vendors:                                
http://127.0.0.1:8000/GET/api/vendors/    


3) Retrieve a specific vendor's details:                                
http://127.0.0.1:8000/GET/api/vendors/<int:vendor_id>/      


4) Update a vendor's details:                   
http://127.0.0.1:8000/PUT/api/vendors/<int:vendor_id>/     


5) Delete a vendor:                         
http://127.0.0.1:8000/DELETE/api/vendors/<int:vendor_id>/  


6) Create a new purchase order:                         
http://127.0.0.1:8000/POST/api/purchase_orders/ 


7) List all purchase orders with an option to filter by vendor:                     
http://127.0.0.1:8000/GET/api/purchase_orders/ 


8) Retrieve details of a specific purchase order:                       
http://127.0.0.1:8000/GET/api/purchase_orders/<int:po_id>/


9) update a purchase order:                         
http://127.0.0.1:8000/PUT/api/purchase_orders/<int:po_id>/ 


10) Delete a purchase order:                                
http://127.0.0.1:8000/DELETE/api/purchase_orders/<int:po_id>/


11) Retrieve a vendor's performance metrics:                        
http://127.0.0.1:8000/GET/api/vendors/<int:vendor_id>/performance/


12) Update acknowledgment_date in the purchase_order and average_response_time in vendor:       
http://127.0.0.1:8000/POST/api/purchase_orders/<int:po_id>/acknowledge/



# Sample content for the API endpoints
1) Create a new vendor:         
{
    "name": "yourname",
    "contact_details": "your personal number",
    "address": "physical address",
    "vendor_code": "2402",
    "on_time_delivery_rate": 1.0,
    "quality_rating_avg": 1.0,
    "average_response_time": 1.0,
    "fulfillment_rate": 1.0
}


2) Create a new purchase order:             
{
    "po_number": "Your_PO_Number",
    "vendor": 1, 
    "order_date": "2024-05-03T08:00:00Z", 
    "delivery_date": "2024-05-10T08:00:00Z",
    "items": {
        "item1": "Item 1 details",
        "item2": "Item 2 details"
        // Add more items as needed
    },
    "quantity": 100,
    "status": "Pending",
    "quality_rating": 4.5, 
    "issue_date": "2024-05-03T08:00:00Z",  
    "acknowledgment_date": "2024-05-03T08:00:00Z" 
}

3) Update acknowledgment_date:      
{"acknowledgment_date":"2024-05-03"}


# Documentation for each API endpoint
https://docs.google.com/document/d/11q6lsgrNQNuTvYcwpSiutBf1BYidooq8Px-lzftcZKQ/edit?usp=sharing