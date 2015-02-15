## Setup

Update `auth_data.py` before using the app!


## Usage

Create a new rescue entry

    curl -u admin:secret --data 'ip_address=10.10.1.1' http://localhost:5000/rescue
    # 201 on success
    # 409 if there is already an entry

Check if there is an entry currently

    curl -u admin:secret http://localhost:5000/rescue/10.10.1.1
    # 200 if found
    # 404 if not found

Destroy an entry

    curl -u admin:secret -X DELETE http://localhost:5000/rescue/10.10.1.1
    # 204 on success

