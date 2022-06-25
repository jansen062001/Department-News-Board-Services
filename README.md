# Department News Board Services
Department News Board adalah sebuah aplikasi yang digunakan untuk memberikan pengumuman pada aplikasi mobile / website. Pada service ini kita dapat membuat pengumuman. Pada pengumuman terkadang terdapat beberapa file yang bisa diberikan juga sebagai file tambahan / attachment.

## Request: Account registration
![POST](https://badgen.net/badge/Method/POST/yellow)**/api/account**
```json
{
    "email_address": "example@gmail.com",
    "password": "example_password"
}
```


### Responses:
#### Account registration
![Created](https://badgen.net/badge/Created/201/green)
```json
{
    "status": "success",
    "message": "Account created successfully"
}
```
#### Account registration (Email already taken)
![Bad%20Request](https://badgen.net/badge/Bad%20Request/400/red)
```json
{
    "status": "error",
    "message": "Email already taken"
}
```

## Request: Account login
![POST](https://badgen.net/badge/Method/POST/yellow)**/api/account/login**
```json
{
    "email_address": "example@gmail.com",
    "password": "example_password"
}
```


### Responses:
#### Account login
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "status": "success",
    "message": "Logged in successfully"
}
```
#### Account login (Unauthorized)
![Unauthorized](https://badgen.net/badge/Unauthorized/401/red)
```json
{
    "status": "error",
    "message": "Unauthorized: invalid credentials (wrong email/password)"
}
```

## Request: Account logout
![GET](https://badgen.net/badge/Method/GET/green)**/api/account/logout**


### Responses:
#### Account logout
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "status": "success",
    "message": "Logged out successfully"
}
```

## Request: Add news
![POST](https://badgen.net/badge/Method/POST/yellow)**/api/news**
```
Body (form-data)
    file: /D:/xxx/example.jpg
    text: Lorem Ipsum is simply dummy text of the printing and typesetting industry.
```


### Responses:
#### Add news
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "status": "success",
    "message": "Add news successful"
}
```
#### Add news (Unauthorized)
![Unauthorized](https://badgen.net/badge/Unauthorized/401/red)
```json
{
    "status": "error",
    "message": "Login required"
}
```
#### Add news (No file part)
![Bad%20Request](https://badgen.net/badge/Bad%20Request/400/red)
```json
{
    "status": "error",
    "message": "No file part"
}
```
#### Add news (No selected file)
![Bad%20Request](https://badgen.net/badge/Bad%20Request/400/red)
```json
{
    "status": "error",
    "message": "No selected file"
}
```
#### Add news (Unsupported Media Type)
![Unsupported%20Media%20Type](https://badgen.net/badge/Unsupported%20Media%20Type/415/red)
```json
{
    "status": "error",
    "message": "Unsupported Media Type"
}
```

## Request: Edit news text
![PUT](https://badgen.net/badge/Method/PUT/blue)**/api/employee/`<int:news_id>`**
```json
{
    "text": "Lorem Ipsum is simply dummy text of the printing and typesetting industry."
}
```


### Responses:
#### Edit news text
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "status": "success",
    "message": "Edit news text successful"
}
```
#### Edit news text (Unauthorized)
![Unauthorized](https://badgen.net/badge/Unauthorized/401/red)
```json
{
    "status": "error",
    "message": "Login required"
}
```
#### Edit news text (News not found)
![Not Found](https://badgen.net/badge/Not%20Found/404/red)
```json
{
    "status": "error",
    "message": "News not found"
}
```
#### Edit news text (News has been archived)
![Not Found](https://badgen.net/badge/Not%20Found/404/red)
```json
{
    "status": "error",
    "message": "News has been archived"
}
```

## Request: Add news file
![POST](https://badgen.net/badge/Method/POST/yellow)**/api/news/`<int:news_id>`/file**
```
Body (form-data)
    file: /D:/xxx/example.jpg
```


### Responses:
#### Add news file
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "status": "success",
    "message": "Add news file successful"
}
```
#### Add news file (Unauthorized)
![Unauthorized](https://badgen.net/badge/Unauthorized/401/red)
```json
{
    "status": "error",
    "message": "Login required"
}
```
#### Add news file (News not found)
![Not Found](https://badgen.net/badge/Not%20Found/404/red)
```json
{
    "status": "error",
    "message": "News not found"
}
```
#### Add news file (News has been archived)
![Not Found](https://badgen.net/badge/Not%20Found/404/red)
```json
{
    "status": "error",
    "message": "News has been archived"
}
```
#### Add news file (No file part)
![Bad%20Request](https://badgen.net/badge/Bad%20Request/400/red)
```json
{
    "status": "error",
    "message": "No file part"
}
```
#### Add news file (No selected file)
![Bad%20Request](https://badgen.net/badge/Bad%20Request/400/red)
```json
{
    "status": "error",
    "message": "No selected file"
}
```
#### Add news file (Unsupported Media Type)
![Unsupported%20Media%20Type](https://badgen.net/badge/Unsupported%20Media%20Type/415/red)
```json
{
    "status": "error",
    "message": "Unsupported Media Type"
}
```

## Request: Delete News
![DELETE](https://badgen.net/badge/Method/DELETE/red)**/api/news/`<int:news_id>`**


### Responses:
#### Delete News
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "status": "success",
    "message": "Delete news successful"
}
```
#### Delete News (Unauthorized)
![Unauthorized](https://badgen.net/badge/Unauthorized/401/red)
```json
{
    "status": "error",
    "message": "Login required"
}
```
#### Delete News (News not found)
![Not Found](https://badgen.net/badge/Not%20Found/404/red)
```json
{
    "status": "error",
    "message": "News not found"
}
```
## Request: Delete news file
![DELETE](https://badgen.net/badge/Method/DELETE/red)**/api/news/`<int:news_id>`/file/`<int:file_id>`**


### Responses:
#### Delete news file
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "status": "success",
    "message": "Delete news file successful"
}
```
#### Delete news file (Unauthorized)
![Unauthorized](https://badgen.net/badge/Unauthorized/401/red)
```json
{
    "status": "error",
    "message": "Login required"
}
```
#### Delete news file (News not found)
![Not Found](https://badgen.net/badge/Not%20Found/404/red)
```json
{
    "status": "error",
    "message": "News not found"
}
```
#### Delete news file (News has been archived)
![Not Found](https://badgen.net/badge/Not%20Found/404/red)
```json
{
    "status": "error",
    "message": "News has been archived"
}
```
#### Delete news file (File not found)
![Not Found](https://badgen.net/badge/Not%20Found/404/red)
```json
{
    "status": "error",
    "message": "File not found"
}
```

## Request: Get all news
![GET](https://badgen.net/badge/Method/GET/green)**/api/news**


### Responses:
#### Get all news
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "text": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
            "created_on": "2022-06-26T02:24:14",
            "files": [
                {
                    "id": 1,
                    "filename": "0_15.jpg"
                },
                {
                    "id": 2,
                    "filename": "8.png"
                }
            ]
        }
    ]
}
```

## Request: Get news by id
![GET](https://badgen.net/badge/Method/GET/green)**/api/news/`<int:news_id>`**


### Responses:
#### Get news by id
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "status": "success",
    "data": {
        "id": 1,
        "text": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
        "created_on": "2022-06-26T02:24:14",
        "files": [
            {
                "id": 1,
                "filename": "0_15.jpg"
            },
            {
                "id": 2,
                "filename": "8.png"
            }
        ]
    }
}
```
#### Get news by id (News not found)
![Not Found](https://badgen.net/badge/Not%20Found/404/red)
```json
{
    "status": "error",
    "message": "News not found"
}
```

## Request: Download file
![GET](https://badgen.net/badge/Method/GET/green)**/api/news/file/`<int:file_id>`**


### Responses:
#### Download file
![OK](https://badgen.net/badge/OK/200/green)
```
Headers(5)
    Content-Type: image/jpeg
    Content-Length: 30816
    Content-Disposition: attachment; filename=0_15.jpg
    Date: Sat, 25 Jun 2022 17:17:33 GMT
    Connection: keep-alive
```
#### Download file (File not found)
![Not Found](https://badgen.net/badge/Not%20Found/404/red)
```json
{
    "status": "error",
    "message": "File not found"
}
```