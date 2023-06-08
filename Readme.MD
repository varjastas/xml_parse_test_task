Test task for applying to python developer job. Parses xml mentioned in test task and sends results using web site or by running python application.

Parser was written using SAX and server was created using Flask. Then server was deployed on Heroku.

Parser covered three scenarios:

1. Count all products.
2. Print names and codes of every product.
3. Print product and his spare parts.

How to run:

1. You can visit https://xml-parser-test-task.herokuapp.com/ and try it without needing to run anything
2. You can run main.py and choose scenario. Results will be in directory resources if you`ve chosen to write results to file.
3. You can start flask server on your PC by simply running flask, but before that you`ll need to install it using pip install flask
4. You can build container using docker and server on localhost or run main.py in container terminal. How to build:
   1. Download docker and start it
   2. Open directory with project and paste:
      1. docker build -t xml_parser .
      2. docker run -p 5000:5000 --name xml_parser xml_parser
   3. Then open docker container xml_parser or go directly to http://localhost:5000/. If you want to run main.py then go to terminal of container and run it simply by pasting python main.py
