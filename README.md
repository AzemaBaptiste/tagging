Tagging 
===========
ReST APIs for music tagging purpose.

    
## Run with Docker

## Server

Build and run server exposed to localhost:5000

    docker build . -t tagging-server -f docker/server.dockerfile
    docker run -d -p 5000:5000 tagging-server

## Client
Build and run client exposed to localhost:8080

    docker build . -t tagging-client -f docker/client.dockerfile
    docker run -d -p 8080:80 tagging-client
    
## Development

    # server
    virtualenv -p python3 venv
    source venv/bin/activate
    
    pip install -r requirements
    python app.py
    
    # client
    cd client/
    npm install
    npm run serve
