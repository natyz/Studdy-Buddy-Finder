# Study Buddy Finder

Website: http://project-1-08.herokuapp.com/

## About Us
Our project is a Virtual Study Buddy Finder App. We hope to assist UVA students struggling to find other peers to study with due to COVID-19, whether it is for a specific class or to simply have someone to study with. We hope that this site supports the UVA community and brings students closer together despite online learning!

This project was programmed in Python 3, with some usages of HTML and JavaScript. The framework used is Django 3.1. The build environment is Travis CI. The source control management is GitHub, and the cloud hosting used is Heroku. We use Postgres as our database engine. 

Contributers: Natalie Zhang, Anthony Taylor, Josh Mehr, Mariah Tighe

## Login and Profile setup
Users are able to sign in with their Google account and/or their University of Virginia email account. The login feature uses a Google account API to allow anyone with a Google account to login and use the application. Django-allauth is used to support various authentications and verifications for users. After logging in to the app, users are able to edit their profiles to include a nickname, class schedule, major, class year, short bio, zoom id, and a profile picture uploaded from their computer. The zoom id is required in order to post a listing. In their bios, users can put any relevant information like what they want help with, what they are able to help with, or their general study mood at the moment. Users are also able to display their schedule for the current semester as well.

## Create/Find a group
After setting up their account, users are able to post and/or browse listings and join virtual study groups. Creating a listing requires inputting information into a form so that students can identify where they need the most help when forming a study group. Information can include: class title, class number, professor, ideal group size, ideal study time, time zone, and language. To join a group, you click on the join group icon in the top right corner of the desired listing. Once you click this button, a pop-up window will show asking you to confirm joining. After confirming, you are able to see the other group members as well as the Zoom link once you click on the study group you joined. Describe how the listing prevents you from rejoining a study room. Users are able to delete their own listings if they choose to do so.

## Contact us
Another feature of our project is the contact form. This form can be found on the home page after clicking the “Contact Us!” button. The contact form uses an additional third-party API with SendGrid  (https://sendgrid.com/docs/API_Reference/api_v3.html). This form allows users to contact the developers of the app with comments, concerns, suggestions, and/or issues. Users will receive a confirmation email with their message. 

## Basic setup
1. Login with a Google account
2. Go to your profile, which should be your name in the right-hand corner of the navigation bar. Click the "edit" button to fill out information for your profile page - the zoom id field is required to create a listing. If you forget, you will be re-directed when creating a listing.
3. Go to the Listings page. Click "create listing" to create your study group or join one that exists. Feel free to search for a particular class or course!
4. When joining a study group, click the group icon on the top right. It should indicate how many spots are still available.
5. When the day of the meeting comes as indicated on the listing, click the group icon on the top right. You should see a page to join a zoom call.
6. Questions or concerns? Feel free to fill out the form on the contact us and we will get back to you!

## References, Tests, and Licenses
All code that has been used from other sources is cited in each file that used the source code. References are at the top after import statements and each portion used from those references is cited by the title and author. Our tests are under mysite/tests.py. Our project is under the MIT and BSD-3 Licenses. Please note that if you are a student taking CS 3240 at UVA, using any code from this repo may result in an Honor Code Violation.
