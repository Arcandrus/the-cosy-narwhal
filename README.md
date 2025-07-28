# the-cosy-narwhal
Code Institute Project Milestone 4 - Django Full Stack E-Commerce Development


## Table of Contents

1. [Live Demo](#demo)
2. [Database ERD](#database-erd)
   + [Product Model](#product-model)
   + [Order Model](#order-model)
   + [Profile Model](#profile-model)
3. [User Stories](#user-stories)
    + [Product](#product-epic)
    + [Users](#users-epic)     
4. [Design](#design)
5. [Technologies](#technologies)
6. [Features](#features)
    + [Product Display & Cart](#product-display--cart)
        + [All Products](#all-products)
        + [Product Search](#product-search)
        + [Add to Cart](#add-to-cart)
        + [View Cart](#view-cart)
    + [Account Registration & User Profile](#account-registration--user-profile)
        + [Registration](#registration)
        + [User Profiles](#user-profiles)
        + [Order History](#order-history)
        + [Reviews](#reviews)
    + [Checkout & Stripe](#checkout--stripe)
        + [Checkout](#checkout)
        + [Order Summary](#order-summary)
        + [Stripe Integration](#stripe-integration)
        + [Confirmation](#confirmation)
    + [Product Management](#product-management)
        + [Add Product](#add-product)
        + [Edit Product](#edit-product)
        + [Remove Product](#remove-product)
        + [Update Inventory](#update-inventory)
        + [Sales Report](#sales-report)
8. [Deployment](#deployment)
9. [Testing](#testing)
   + [Validation](#validation)
   + [Manual Testing](#manual-testing)
   + [Responsive UI Testing](#responsive-ui-testing)
   + [Browser Compatibility](#browser-compatibility)
   + [User Story Testing](#user-story-testing)
11. [Credits](#credits)


![](/responsive_ui.png)

## Demo
A live demo to the website can be found [here](https://the-cosy-narwhal-0266caf0f910.herokuapp.com)

## Database ERD

### Product Model
### Order Model
### Profile Model

## User Stories

### Product Epic
### Users Epic

## Design

## Technologies
**HTML** - To create a basic site skeleton and add the content. The site consists of HTML template partials loaded within the **base.html** template.

<details>
<summary>base.html is shown here</summary>
    
    {% load static %}

      <!doctype html>
      <html lang="en">
      
      <head>
          {% block core_meta %}
          <!-- Required meta tags -->
          <meta http-equiv="X-UA-Compatible" content="ie=edge">
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          {% endblock %}
      
          {% block extra_meta %}
          {% endblock %}
      
          {% block core_css %}
          <!-- Bootstrap CSS -->
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css"
              integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
          <!-- Googlefonts Import-->
          <link rel="preconnect" href="https://fonts.googleapis.com">
          <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
          <link
              href="https://fonts.googleapis.com/css2?family=Bad+Script&family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap"
              rel="stylesheet">
          <!-- Core Custom CSS -->
          <link href="{% static 'css/base.css' %}" rel="stylesheet">
          {% endblock %}
      
          {% block extra_css %}
          {% endblock %}
      
          {% block core_js %}
          <!-- Bootstrap JS -->
          <script src="https://code.jquery.com/jquery-3.7.1.js"
              integrity="sha256-eKhayi8LEQwp4NKxN+CfCh+3qOVUtJn3QNZ0TciWLP4=" crossorigin="anonymous"></script>
          <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"
              integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN"
              crossorigin="anonymous"></script>
          <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js"
              integrity="sha384-+sLIOodYLS7CIrQpBjl+C7nPvqq+FbNUBDunl/OZv93DB7Ln/533i8e/mZXLi/P+"
              crossorigin="anonymous"></script>
          <!-- FontAwesome Kit -->
          <script src="https://kit.fontawesome.com/9ea763a632.js" crossorigin="anonymous"></script>
          <!-- Stripe JS -->
          <script src="https://js.stripe.com/v3/"></script>
          {% endblock %}
      
          {% block extra_js %}
          {% endblock %}
      
          <title>The Cosy Narwhal - Handmade Crochet</title>
      </head>
      
      <body>
          <header class="container-fluid fixed-top">
              <div id="topnav" class="row bg-grad p-2 d-none d-lg-flex align-items-center">
                  <div
                      class="col-12 col-lg-4 d-flex align-items-center justify-content-center justify-content-lg-start py-lg-0">
                      <a href="{% url 'home' %}" class="nav-link main-logo-link">
                          <h2 class="logo-font text-black m-0">The Cosy Narwhal</h2>
                      </a>
                  </div>
      
                  <div class="col-12 col-lg-4 d-flex align-items-center py-1 py-lg-0">
                      <form method="GET" action="{% url 'products' %}" class="w-100">
                          <div class="input-group">
                              <input class="form-control border border-black rounded" 
                                  type="text" name="q"
                                  placeholder="Search our site"
                                  value="{{ search_term|default:'' }}">
                              <div class="input-group-append">
                                  <button class="btn btn-black border border-black rounded" type="submit">
                                      <span class="icon"><i class="fas fa-search"></i></span>
                                  </button>
                              </div>
                          </div>
                      </form>
                  </div>
      
                  <div
                      class="col-12 col-lg-4 d-flex align-items-center justify-content-center justify-content-lg-end py-1 py-lg-0">
                      <ul class="list-inline list-unstyled m-0 d-flex align-items-center">
                          <li class="list-inline-item dropdown mx-2">
                              <a class="text-black nav-link" href="{% url 'products' %}">
                                  <div class="text-center">
                                      <div><i class="fa-solid fa-store"></i></div>
                                      <p class="my-0">Products</p>
                                  </div>
                              </a>
                          </li>
                          <li class="list-inline-item dropdown mx-2">
                              <a class="text-black nav-link" href="#" id="user-options" data-toggle="dropdown"
                                  aria-haspopup="true" aria-expanded="false">
                                  <div class="text-center">
                                      <div><i class="fas fa-user fa-lg"></i></div>
                                      <p class="my-0">My Account</p>
                                  </div>
                              </a>
                              <div class="dropdown-menu border-0" aria-labelledby="user-options">
                                  {% if request.user.is_authenticated %}
                                  {% if request.user.is_superuser %}
                                  <a href="{% url 'product_management' %}" class="dropdown-item">Product Management</a>
                                  {% endif %}
                                  <a href="{% url 'profile' %}" class="dropdown-item">My Profile</a>
                                  <a href="{% url 'account_logout' %}" class="dropdown-item">Logout</a>
                                  {% else %}
                                  <a href="{% url 'account_signup' %}" class="dropdown-item">Register</a>
                                  <a href="{% url 'account_login' %}" class="dropdown-item">Login</a>
                                  {% endif %}
                              </div>
                          </li>
                          <li class="list-inline-item mx-2">
                              <a class="nav-link" href="{% url 'view_bag' %}">
                                  <div class="text-center">
                                      <div><i class="fa-solid fa-cart-shopping"></i></div>
                                      <p class="my-0">My Cart</p>
                                      <p class="my-0">
                                          {% if grand_total %}
                                          £{{ grand_total|floatformat:2 }}
                                          {% else %}
                                          {% endif %}
                                      </p>
                                  </div>
                              </a>
                          </li>
                      </ul>
                  </div>
              </div>
              <div class="row p-2 d-lg-none d-md bg-grad">
                  <nav class="navbar navbar-expand-lg navbar-light w-100">
                      {% include 'includes/mobile_top_header.html' %}
                  </nav>
              </div>
          </header>
          <div class="container">
          {% block content %}
          {% endblock %}
          </div>
          <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
          {% if messages %}
          <div class="message-container">
              {% for message in messages %}
              {% with message.level as level %}
              {% if level == 40 %}
              {% include 'includes/toasts/toast_error.html' %}
              {% elif level == 30 %}
              {% include 'includes/toasts/toast_warning.html' %}
              {% elif level == 25 %}
              {% include 'includes/toasts/toast_success.html' %}
              {% else %}
              {% include 'includes/toasts/toast_info.html' %}
              {% endif %}
              {% endwith %}
              {% endfor %}
          </div>
          {% endif %}
          <script type="text/javascript">
              $('.toast').toast('show');
          </script>
          {% block postloadjs %}
          {% endblock %}
      </body>
      <footer class="footer bg-grad-rev w-100 d-lg-flex fixed-bottom">
          {% include 'includes/footer.html' %}
      </footer>
      </html>
</details>

**CSS** - To create a controlled and consistent display for each element and to give a great user experience. Using js, I applied a class based responsive design to the site.

**Javascript** - 

**Django** - This was the meat of the project, enabling full user controlled CRUD functionality. Implementing a CustomUser model as well as creating custom templates for much of the Django AllAuth library to allow for greater access and customisation across the sites features. 

**Balsamiq** - To create a wireframe, [here](mtg-forum-assets/mtg_forum.pdf) (pdf format)

**Bootstrap** - To ensure responsive design and usability across all devices, I use a combination of Bootstrap classes and custom css.

## Features

### All Products
### Product Search
### Add to Cart
### View Cart
### Account Registration & User Profile
### Registration
### User Profiles
### Order History
### Reviews
### Checkout & Stripe
### Checkout
### Order Summary
### Stripe Integration
### Confirmation
### Product Management
### Add Product
### Edit Product
### Remove Product
### Update Inventory
### Sales Report

# Deployment 
1. Log in to Heroku if you already have an account with them. If not, create an account.
2. Once signed in, click on the "Create New App" button located above your dashboard. Give your app a unique name, choose the region you're in (United States/Europe) and click "Create app".
3. Before deploying, you need to go to the Settings tab. Once there, scroll down and click on Reveal Config Vars to open this section.
4. In this section, enter all of your environment variables that are present in your env.py file. Fields like DATABASE_URL, SECRET_KEY, CLOUDINARY_URL (if using Cloudinary), EMAIL_HOST_USER and EMAIL_HOST_PASSWORD if you are planning on sending emails to users (like having a Reset Password functionality).
5. After that, make sure to go to the Resources tab and make sure Heroku didn't automatically set up a database for you. If that happens, simply remove the PostgreSQL database.
6. Now, go to the Deploy tab. Once there, in the Deployment Method section, click GitHub and if needed, authorize GitHub to access your Heroku account. Click Connect to GitHub.
7. Once connected, look up your GitHub repository by entering the name of it under Search for a repository to connect to and click Search. After you've found your repo, click Connect.
8. I used manual deployment throughout this project, so once I had done a GitHub push, I navigated here and clicked Deploy Branch. If you enabled automatic deploys, every time you push changes to GitHub, the app will be automatically deployed every time, just like you would with a webpage deployed on GitHub Pages.
8. The app can take a couple of minutes until it's deployed. Once it's done, you'll see the message Your app was successfully deployed and a "Open App" button will be displayed at the top of the screen, where you can see your deployed app.

# Testing

## Validation

**HTML** <br>
[W3C HTML validator](https://validator.w3.org) seemed to really struggle with the Django generated content so I instead validated the raw HTML after Django rendering, which showed no errors

<details>
   <summary>HTML Pass</summary>
   
![](./mtg-forum-assets/pass_html.png)
</details>

**CSS** <br>
[W3C CSS Validator](https://jigsaw.w3.org/css-validator/) showed no errors.

<details>
   <summary>CSS Pass</summary>
   
![](./mtg-forum-assets/pass_css.png)
</details>

**JS** <br>
[BeautifyTools JS Validator](https://beautifytools.com/javascript-validator.php) was used to validate all my js scripts and each returned no errors. I've included one screenshot, but I ran every script through the validator.

<details>
   <summary>JS Pass</summary>
   
![](./mtg-forum-assets/js_pass.png)
</details>

**Python** <br>
[Pep8 CI](https://pep8ci.herokuapp.com) was used to validate all *.py files and with the exception of a couple of trailing whitespaces and incorrect spacing, which I then fixed, everything came back clear.

**Lighthouse** <br>
DevTools Lighthouse Scores. The big problem with the Best Practices score was the third party cookies, most of which were the cloudinary images, and I'm not sure how to make this any better.

<details>
   <summary>Lighthouse</summary>
   
![](./mtg-forum-assets/lighthouse_scores.png)
</details>

## Manual Testing

### Manual Testing

All these features were manually tested by me and several others, these are the results of those tests.

| Feature | Expectation | Action | Result |
| ---------- | ---------- | ------------ | ----------- |

## Responsive UI Testing


## Browser Compatibility
I tested the site on several popular browsers to ensure functionality and usablity on each. Here are the results of those tests.

| Browser | Issues | Functionality |
| ---------- | ---------- | ------------ |
| Google Chrome | None | Good |
| Apple Safari | None | Good |
| Opera GX | None | Good |
| Mozilla Firefox | None | Good |
| Microsoft Edge | None | Good |

## User Story Testing
Below follows a breakdown of each of the user stories and the results of the implementation and testing of each.

| User Story | Acceptance criteria | Criteria Met? | Tested | Notes |
| ---------- | ---------- | ---------- | ---------- | ---------- |

## Major Bugs & Errors

# Credits
I would like to thank my mentor, Medale Oluwafemi and my tutor Tom Cowen for their continued insights and support during this project.

MASSIVE thank you to my best friends Rew and Emma for their continued support and belief in me as I've progressed as well as their help testing functionality and features and their valuable feedback, I love you both.

Thanks go to the Frome MTG club who have also helped me with testing and troubleshooting. 

I would also like to credit ChatGPT for helping me with specific debugging and formatting issues I faced when building this project, as well as helping me to refactor redundant code.



The Cosy Narwhal - Basic Introduction

Easy and clean, responsive design
Social account links
Interactive reviews, score based on average
e-commerce, purchase, checkout and delivery
Events calendar
user can register login and view an order history
allow guest checkout
confirmation of order email
limit purchases to UK only
maximum searchable field results
product code
delivery based on weight, as set by Royal Mail

item
 - Name
 - Product code - Individualised for colored variants
 - Picture
 - Description
 - Care Details
 - Price
 - Size S/M/L
 - Quantity Available
 - OOS Notification

user
 - Name
 - Email - Unique
 - Phone Number
 - Full Address

bag
 - Current Items in Bag
 - Subtotal of Items
 - Delivery Charge
 - Grand Total of Order

superuser
 - Add New Products
 - Delete Existing Products
 - Edit Existing Products
 - Update Stock
 - View Current Inventory

Example Item
 - Name: Crochet Turtle Plushie
 - Product Code: TCN0001
 - Picture: tcn0001.png
 - Description: Soft, squishy, and handmade with plush blanket yarn, this adorable turtle is perfect for cuddles, gifting, or adding a cosy touch to any space. Each one is unique and full of charm.
 - Care Details: Made with 100% polyester yarn and hypoallergenic soft toy filling. Machine Washable at 30 degrees. Colours may run or fade. Not suitable for children under 3yo due to smaller parts.
 - Colours: N/A
 - Price: £12
 - Size: M


