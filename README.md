# the-cosy-narwhal
Code Institute Project Milestone 4 - Django Full Stack E-Commerce Development


## Table of Contents

1. [Live Demo](#demo)
2. [Database ERD](#database-erd)
   + [Product Model](#product-model)
   + [Order Model](#order-model)
   + [Profile Model](#profile-model)
3. [User Stories](#user-stories)
   + [Epics](#epics)
        + [Product Epic](#product-epic)
        + [Users Epic](#users-epic)     
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

# Database ERD

# User Stories

## Design

## Technologies
**HTML** - To create a basic site skeleton and add the content. The site consists of HTML template partials loaded within the **base.html** template.

<details>
<summary>base.html is shown here</summary>
    
    {% load static %}
    {% url 'posts' as posts_url %}
    {% url 'account_login' as login_url %}
    {% url 'account_signup' as signup_url %}
    {% url 'account_logout' as logout_url %}
    
    <!DOCTYPE html>
    <html lang="en-US">
    
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="keywords" content="">
        <meta name="author" content="">
    
        <!-- FontAwesome Import -->
        <script src="https://kit.fontawesome.com/9ea763a632.js" crossorigin="anonymous"></script>
        <!-- Bootstrap CSS Import -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-4Q6Gf2aSP4eDXB8Miphtr37CMZZQ5oXLH2yaXMJ2w8e2ZtHTl7GptT4jmndRuHDT" crossorigin="anonymous">
        <!-- jQuery (required by Summernote) -->
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <!-- Bootstrap JS (required by Summernote) -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <!-- Summernote CSS & JS -->
        <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.20/dist/summernote.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/summernote@0.8.20/dist/summernote.min.js"></script>
        <!-- Custom CSS -->
        <link rel="stylesheet" href="{% static 'css/style.css' %}">
        <title>MTG Forum</title>
    </head>
    
    <body class="">
        <header>
            <img class="icon" alt="Brand Icon" src="{% static 'image/card.png' %}">
            <h1>MTG FORUM</h1>
                <div class="header-spacer"></div>
                <button id="menu-toggle" class="right hamburger" aria-label="Toggle sidebar">
                    &#9776;
                </button>
        </header>
    
        <div class="page-wrapper d-flex"> <!-- Flex container -->
    
            <aside class="sidebar">
                {% if user.is_authenticated %}
                <div class="profile_container">
                    <div class="profile_picture">
                        <img src="{{ user.profile_picture.url }}" alt="Profile Picture">
                    </div>
                    <div class="profile_details">
                        <p><strong>{{ user }}</strong></p>
                        <p><strong><i class="fa-solid fa-pencil"></i> Posts:</strong> {{ user.post_count }}</p>
                        <p><strong><i class="fa-solid fa-comment"></i> Comments:</strong> {{ user.comment_count }}</p>
                        <p><strong><i class="fa-solid fa-circle-check"></i> Status:</strong> {{ user.user_status }}</p>
                    </div>
                </div>
                {% endif %}
                <div class="search-wrapper">
                    <form method="GET" action="{% url 'search_results' %}">
                        <input type="text" name="q" placeholder="Search posts..." required>
                        <button class="btn search-btn btn-primary" type="submit" aria-label="Search">
                            <i class="fas fa-magnifying-glass"></i>
                        </button>
                    </form>
                </div>
    
                <nav class="sidebar-nav" aria-label="Sidebar navigation">
                    <ul>
                        {% if user.is_authenticated %}
                        <li><a href="{% url 'create_post' %}"><i class="fa-solid fa-plus"></i> New Post</a></li>
                        <li><a href="{% url 'account_logout' %}"><i class="fa-solid fa-right-from-bracket"></i> Logout</a>
                        </li>
                        {% else %}
                        <li><a href="{% url 'account_signup' %}"><i class="fa-solid fa-user-plus"></i> Register</a></li>
                        <li><a href="{% url 'account_login' %}"><i class="fa-solid fa-right-to-bracket"></i> Login</a></li>
                        {% endif %}
    
                        <li>
                            <hr>
                        </li>
    
                        <li><a href="{% url 'post_list' %}"><i class="fa-solid fa-house"></i> Home</a></li>
                        <li><a href="{% url 'category_list' %}"><i class="fa-solid fa-list"></i> Categories</a></li>
                        <li><a href="{% url 'favourite_posts' %}"><i class="fa-solid fa-star"></i> Favourites</a></li>
                        <li><a href="{% url 'popular_posts' %}"><i class="fa-solid fa-fire"></i> Popular</a></li>
    
                        <li>
                            <hr>
                        </li>
    
                        {% if user.is_authenticated %}
                        <li><a href="{% url 'profile' username=request.user.username %}"><i class="fa-solid fa-user"></i>
                                Profile</a></li>
                        <li><a href="{% url 'user_settings' %}"><i class="fa-solid fa-gear"></i> Settings</a></li>
                        {% else %}
                        <li><a href="{% url 'account_login' %}"><i class="fa-solid fa-user"></i> Profile</a></li>
                        {% endif %}
                    </ul>
                </nav>
            </aside>
            <div id="sidebar-overlay"></div>
    
            <main class="content flex-grow-1 p-3">
                {% if messages %}
                <ul class="messages">
                    {% for message in messages %}
                    <li{% if message.tags %} class="{{ message.tags }}" {% endif %}>
                        {{ message }}
                        </li>
                        {% endfor %}
                </ul>
                {% endif %}
    
                {% block content %}
                <!-- Content Goes here -->
                {% endblock content %}
            </main>
    
        </div>
    
        <footer>
            <p>Copyright Eric Harper 2025</p>
        </footer>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script src="{% static 'js/like.js' %}"></script>
        <script src="{% static 'js/comments.js' %}"></script>
        <script src="{% static 'js/post_edit.js' %}"></script>
        <script src="{% static 'js/messages.js' %}"></script>
        <script src="{% static 'js/favourite.js' %}"></script>
        <script src="{% static 'js/screen_check.js' %}"></script>
    
        <!-- Hamburger -->
        <script>
            const toggleBtn = document.getElementById('menu-toggle');
            const sidebar = document.querySelector('.sidebar');
            const overlay = document.getElementById('sidebar-overlay');
    
            function toggleSidebar() {
                const isOpen = sidebar.classList.toggle('open');
                overlay.classList.toggle('active', isOpen);
            }
    
            toggleBtn.addEventListener('click', toggleSidebar);
    
            // Dismiss sidebar when clicking the overlay
            overlay.addEventListener('click', () => {
                sidebar.classList.remove('open');
                overlay.classList.remove('active');
            });
        </script>
    </body>
    
    </html>
</details>

**CSS** - To create a controlled and consistent display for each element and to give a great user experience. Using js, I applied a class based responsive design to the site.

**Javascript** - This is where most of the work for this project was done, as much of the system runs on Javascript
+ comments.js - Contains the functionality to post comments, post replies and edit/ delete both
+ favourite.js - Enables AJAX js for the favourite button, both processing the form and updating the button
+ like.js - Enables the like button functionality in a similar vein to the favourite button
+ messages.js - Controls the display of Django messages
+ post_edit.js - Enables the inline form to allow users to edit any of their own posts
+ screen_check.js - As part of responsive design, this js file checks for screen size changes as well as orientation changes

**Django** - This was the meat of the project, enabling full user controlled CRUD functionality. Implementing a CustomUser model as well as creating custom templates for much of the Django AllAuth library to allow for greater access and customisation across the sites features. 

**Balsamiq** - To create a wireframe, [here](mtg-forum-assets/mtg_forum.pdf) (pdf format)

**Bootstrap** - To ensure responsive design and usability across all devices, I use a combination of Bootstrap classes and custom css.

# Features
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


