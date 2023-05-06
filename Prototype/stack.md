# why we chose this stack

## Frontend
1. Ivan is familiar with react, none of the rest of us are familiar with any other frontend framework
2. React is a popular frontend framework, so it will be easy to find help online

## Backend
1. Ezra is the most familiar with Django/python (I use it at work) and John has some experience with it
2. Django is very "batteries included" which will make it easy to move fast

## Database
1. We just went with the default Django database, which is SQLite

## Other things we considered
1. We considered Rocket.rs for the backend or some Golang based server framework 
because we thought it would be cool to learn a new language, but we decided that it would be better to move fast
2. We considered using a NoSQL serverless database like Firebase, but we decided that it would be better to use SQL because it works well with django
3. We considered using Firebase auth, but we weren't sure if it met the OAuth requirement for this project