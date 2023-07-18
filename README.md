# Barker and Stonehouse Clearance Webscraper

This tool scrapes the clearance area of the Barker and Stonehouse website to provide the information in a basic Bootstrap html file. All stores will be sorted and stored on one page with an image, enabling easy searching and viewing of multiple stores. 

Information is stored in a .pkl file for usage later on or further analysis. 

# Hosting the site

Running the code should expose the 8080 port for a local webserver enabling viewing of the file in the web browser. This can be deployed as a container to run in the cloud by exposing this port as well. 

This is a little bloated as it runs as a python3 webserver so would not be optimised for running concurrently with numerous programmes. 