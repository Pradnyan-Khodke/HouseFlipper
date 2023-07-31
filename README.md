# HouseFlipper

## Description
TripVisor is a web app that allows users to explore surrounding cities with promising real estate.

Individuals who are looking to enter the real estate market may find it difficult to find valuable property in the area. Currently, users must decide which locations they would like to invest in, manually track and research them, calculate their expected value, and determine if its profitable. By integrating the entire 'flipping' experience into a single page, HouseFlipper allows users to save time in the exploration stage and streamline all aspects of their research process.

### Features
- Users can search for corresponding housing markets in the area to see houses with the highest potential 'flip'/resale value
- Users can view Zestimates:tm: of any property they so choose
- Users can customize their search to filter out houses that meet their specific demand (House Type, #Beds, #Bath, ...)
- Users can navigate to the Redfin listing of a specific house if they are interested in learning more
- Users can save their searches to an account linked to a Google or Personal Account allowing them to save and view housing data across devices

## Technical Architecture
- Tech Stack: 
    - Next.js/React
    - Python
    - Flask
    - Typescript
    - Material UI
- Database: 
    - MongoDB - NoSQL
- Development Tools
    - Visual Studio Code
    - ESLint
- APIs:
    - Zillow Zestimate API
    - Zillow Public Data API
    - Redfin API
    - Google Maps Places API
- Backend Packages:
    - Sklearn
    - Beautiful Soup
    - Redfin Scraper
    - Support Vector Machine (SVM)
    - CatBoostRegressor
 
## Note
This application uses the Zillow and Places API which need special permission from Bridge Interactive and Google Cloud. To gain access to Zillow APIs email api@bridgeinteractive.com, and for Google Maps APIs navigate to https://developers.google.com/maps. After gaining access, create a a folder in backend/flask and backend/ called secret.py. Additionally add a config.js file to frontend/src/app/dashboard/. To these files, add constants `export const BRIDGE_API` and `export const MAPS_API` and set them to the API keys that you have gotten approval for. 

## How to run the project
HouseFlipper has not yet been deployed. For development, we use NPM to build and run the project locally. To run the project, follow these steps:
1. Clone the repository
2. Ensure you have Node.js installed
3. Run `npm i` to install all the dependencies
4. Run `npm run dev` in the frontend folder to build the front-facing website 
5. Run `flask run` in the backend folder to start model
6. Open up a browser and navigate to the corresponding server URL
7. You should then be able to see the app running on your device


