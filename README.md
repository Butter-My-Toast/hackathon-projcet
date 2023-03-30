
<h1>Yelp Guru</h1>

## Overview
This website allows users to input a yelp restaurant link and receive the top dishes in terms of user rating, user popularity, and health. 

## Technologies used
<p>Front-end: <b>React.js</b>
  
   React is used for the entire webview of the project


  Back-end: <b>Flask </b>

  [insert here how its used and whatnot] 


## Demo

https://user-images.githubusercontent.com/103217739/228711281-91235783-2191-48af-ab53-08050db4aa3c.mp4


## Usage
<p> To run this project on your own you must do the following steps 
  1. Navigate to a command line and clone the repository 
</p>

```
git clone https://github.com/butter-my-toast/yelp-guru/ 
```
<p>
  2. Start the server and take note of the ip 
</p>

```
cd yelp-guru
python main.py
```
<p>
  the output should be something similar to the following codesegment
</p>

```
 * Serving Flask app 'main' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://10.1.126.35:43/ (Press CTRL+C to quit)
```
<p>
  Then open a new terminal and navigate back into the yelp-guru directory and modify the HomePage.jsx file located at pioneerHacksFrontEnd/pioneerHacksFrontEnd/src/components/Homepage/Homepage.jsx
  Find the fetch function on line 29 and replace the url with your server ip given in the previous command.
  Then navigate to the pioonerHacksFrontEnd/pioonerHacksFrontEnd folder and run the following command
</p>

```
npm install
npm run dev
```
<p>
  with that it should all be up and running !
</p>
