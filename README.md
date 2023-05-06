# BU_CS411

### Demo Video
https://www.youtube.com/watch?v=6Wh8t40Xz0o&ab_channel=IvanYang

### Project Description:
Our project is an adblocker for podcasts, where users can toggle whether they want to listen to podcasts with ads or without ads. It utilizes revAI to generate a transcription of a podcast and uses NLP to splice out areas where an ad is, and returns both the start and end times of the suspected ad, and skips the playback within those times when a user views the podcast. 

### Table of contents
Built with
Installation
Running the app

### Built with:
React frontend, Django backend.

### Installation: npm and pip
Make sure you have Node.js and npm installed on your system, as well as pip. You can download and install them from https://nodejs.org and https://pip.pypa.io/en/stable/installation/ respectively. Clone this repository to your local machine using:

git clone https://github.com/your-username/your-project.git

To change to the project directory:
cd your-project

### Install the project dependencies:

npm i
This will install all the dependencies required to run the front end of the project. You should see a node_modules directory created in your project directory. The dependencies used are:

- "@react-oauth/google": "^0.11.0"
- "@testing-library/jest-dom": "^5.16.5"
- "@testing-library/react": "^13.4.0"
- "@testing-library/user-event": "^13.5.0"
- "axios": "^1.4.0"
- "react": "^18.2.0"
- "react-dom": "^18.2.0"
- "react-router-dom": "^6.11.1"
- "react-scripts": "5.0.1"
- "web-vitals": "^2.1.4"

### Running the App:
To run the backend, make sure to download all required packages using the command

pip install -r requirements.txt

Then run python3 manage.py runserver to start the backend. 

To start the frontent in the project directory, you can first cd frontend to change directory to the frontend and then run:

npm start

Runs the app in the development mode.
Open http://localhost:3000 to view it in your browser.

The page will reload when you make changes.
You may also see any lint errors in the console.

npm test
Launches the test runner in the interactive watch mode.
See the section about running tests for more information.

npm run build
Builds the app for production to the build folder.
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.
Your app is ready to be deployed!

See the section about deployment for more information.

npm run eject
Note: this is a one-way operation. Once you eject, you can't go back!

If you aren't satisfied with the build tool and configuration choices, you can eject at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except eject will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use eject. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

### Learn More
You can learn more in the Create React App documentation.

To learn React, check out the React documentation.
