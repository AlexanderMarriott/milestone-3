# milestone-project-3

    Table of Contents

# 1. Introduction
# 2. Project Goals
# 3. Deployment
# 4. Website Structure and Design
## i. Design Choices
## ii. WireFrames
### a. Proposed Layout
### b. Revised Layout
# 5. Built With
# 6. Testing
## i. Manual
## ii. Validation
## iii. Live Testing
# 7. Contact
# 8. Acknowledgements
Introduction
This website is an online platform called ‘SkillSync’ as part of the Code Institute Milestone 3 Project, that enables users to create professional profiles that showcase their qualifications, certifications, interests, and personal information to potential employers. Enhancing job seekers’ visibility and connecting them with potential employment opportunities is the key purpose of SkillSync. 
Project Goals
The primary objectives of this project have been to provide a user-friendly interface for creating and managing professional profiles, to enable users to list their qualifications, certifications, and interests, ensure data privacy and security for all user information, and to facilitate connections between job seekers and employers, all whilst fulfilling the criteria of the Code Institute Milestone 3 Project. 
Deployment
Following the steps below will allow for deployment of SkillSync:
1	Setup Development Environment 
Clone the repo: git clone
[GitHub Repo](https://github.com/AlexanderMarriott/milestone-3.git)
Navigate to the project directory: cd milestone-3
Install the required dependencies: pip install -r requirements.txt
## 2. Deployment to Heroku
Create a new Heroku app: heroku create
Add MongoDB as the databade: Use an add-on like mLab or MongoDB Atlas.
Deploy the app: git push heroku main
Configure environment variabilities: Set up the MongoDB URI and any other necessary environment variable in Heroku
Access the live site at the Heroku URL provided.

Website Structure and Design
Design Choices
I first decided what key design principles I wanted SkillSync to follow. Considering the platform is to showcase professional profiles, I wanted the visual design of SkillSync to utilise a clean and professional aesthetic with a consistent colour scheme and typography. I felt this visual design reflects and compliments the purpose of the platform. 
To ensure all the features of the platform are accessible to users with disabilities, I set all values where required for screen readers, using contrasting colours to ensure clear definitions between back and foreground elements.
I designed the site to be clear and logical in its structure to help users find information quickly and easily. Throughout the design process, navigation and ease of use were prioritised. I wanted to ensure a user-friendly platform, leaving people with an exceptional user experience.
        
WireFrames
The proposed layout provided a basic layout of the homepage, profile creation page, and user dashboard.
Revisions were then made based on user feedback and testing, including improved navigation and additional profile customisation options. 
Please see the proposed layout below: 

HomePage:
 
Sign in Page:
 
Sign Up Page:
 
Profile Page:
 
Built With
SkillSync was built using the following technologies:
-Frontend: HTML, CSS and JavaScript
-Backend: Python and Flask
-Database: MongoDB
-Deployment: Heroku

Testing
Manual Testing
Manual testing included:
-A functional test, whereby I ensured all features were working as intended. 
-A usability test, where verifying ease of use for end-users took place. 
-A responsiveness test to check the compatibility across different devices and screen sizes.
Validation
Validation includes: - links and screenshots to be added
-HTML: Validated with W3C Validator. 
-CSS: Validated with Jigsaw Validator.
-JavaScript: Linted with ESLint. 
Live testing
Live testing involves: Deploying the app on Heroku, gathering user feedback and addressing any reported issues, and continuous monitoring for bugs and performance.
Initial testing was done via dev tools testing different devices and screen widths. all tests returned working as intended.
      
Google lighthouse results
 
Contact
Reach out to me (Alexander Marriott) at [alexmarriott590@gmail.com](mailto:alexmarriott590@gmail.com) for any enquiries. Please utilise the subject matter with a brief description of the nature of your enquiry.
Acknowledgements
The following acknowledgements are made to all contributors to SkillSync, libraries and frameworks used, and any other third-party resources:
Materialisecss.com- for elements
MongoDB Atlas for viewing the database
Fontawesome for icons
Heroku for the project deployment.
