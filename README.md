# Notes REST API docs

## Start

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/derfacn/notes_api.git
   ```

2. Create a virtual environment in the project directory:

   ```bash
   cd notes_api
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   
5. Start the app

   ```bash
   flask run --debug
   ```
   
    or run 
    ```bash
    python wsgi.py
    ```

## Routes

| Endpoint                              | Description                             | Method | Request                                | Response                                |
|---------------------------------------|-----------------------------------------|--------|----------------------------------------|-----------------------------------------|
| `/api/admin/users/`                   | Get all users                           | GET    | Query: limit, offset, fields           | 200: OK, 404: Not Found                 |
| `/api/admin/users/<string:user_uuid>` | Get user by uuid                        | GET    | Query: limit, offset, fields           | 200: OK, 404: Not Found                 |
| `/api/admin/users/`                   | Creates a new user                      | POST   | {"username": "...", "password": "..."} | 201: Created, 409: Conflict             |
| `/api/admin/users/<string:user_uuid>` | Edit user information                   | PUT    | {"username", "password", "is_admin"}   | 200: OK, 404: Not Found                 |
| `/api/admin/users/<string:user_uuid>` | Delete a user by uuid                   | DELETE | -                                      | 200: OK, 404: Not Found                 |
| `/api/auth/login`                     | Login, using token in cookie            | POST   | {"username": "...", "password": "..."} | 200: OK, 403: Forbidden, 404: Not Found |
| `/api/auth/logout`                    | Logout, deletes a cookie                | DELETE | -                                      | 200: OK                                 |
| `/api/auth/signup`                    | Signup, create a user and give a cookie | POST   | {"username": "...", "password": "..."} | 201: Created, 409: Conflict             |
| `/api/notes/`                         | Get all notes                           | GET    | -                                      | 200: OK, 404: Not Found                 |
| `/api/notes/<int:note_id>`            | Get note by id                          | GET    | -                                      | 200: OK, 404: Not Found                 |
| `/api/notes/`                         | Creating new note.                      | POST   | -                                      | 201: Created, 403: Forbidden            |
| `/api/notes/<int:note_id>`            | Update note by id                       | PUT    | {"text": "..."}                        | 200: OK, 404: Not Found                 |
| `/api/notes/<int:note_id>`            | Delete note.                            | DELETE | -                                      | 200: OK, 404: Not Found                 |


## Commands

`flask --help` -- get all commands  
`flask create-admin` -- creating a new admin user  
`flask user-seeder` -- creating a certain number of users