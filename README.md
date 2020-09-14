# Django Shopper Challenge

A RESTful django development challenge for shopping in a shop.

## Introduction
In this challenge you are going to develop a small django web application for ordering simple products.

The user must be able to log in to app according to rules explained ahead, and order some of them. Also he/she must be able to see and edit his/her profile.

App parts:
### Entry:
User can login in two ways:
- first, direct and with providing email and password. If a user with this email does not exist, must be created in database, and if it already exists, must be verified with password and in response get the token for steps ahead.
- second, indirect and with third party authentication. The user must be able to enter app with his/her google account, note that if this part needs a client, you must implement the client part too with minimum UI.

### View products:
For simplicity, the user can get the list of all available and not sold products with providing the token for authorization, note that he/she should get a 401 error if the token is expired or wrong.

### Order:
The user can select some products and buy them with a list of product's ids and the number of each product he/she wants to buy. In response he/she must get the result of his/her attempt. Note that he/she must be authorized to do so, also if any of the ids provided by user was wrong, the related error must be returned in response. 

### Profile:
The user must be able to see his/her profile, and also must be able to patch or post an update to edit it. Note that authorization is required.

## Expectations:
We want a clean, readable and maintainable code with meaningful comments and docstrings. Also you need to provide postman API doc for web app. For task managing, you have to break your work to smaller and manageable tasks, and put them on a task managing app, specified by your mentor.

## Tests
You should write unit tests for your code

## Task
1. Fork this repository
2. break and specify your tasks in project management tool
3. Develop the challenge with Django 2 or higher
4. Push your code to your repository
5. Send us a pull request, we will review and get back to you
6. Enjoy 
