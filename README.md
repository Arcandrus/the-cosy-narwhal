# The Cosy Narwhal - Handmade Crochet Toys
This project was a collaboration with my friend, Emma, who makes crochet toys and accessories, to create an e-commerce platform for her products.

# Code Institute Project Milestone 4 - Django Full Stack E-Commerce Development

## Table of Contents

1. [Live Demo](#demo)
2. [Database](#database)
   + [Product Model](#product-model)
   + [Order Model](#order-model)
   + [Profile Model](#profile-model)
3. [User Stories](#user-stories)
    + [Customer User Stories](#customer-user-stories)
    + [Admin User Stories](#admin-user-stories)
    + [General User Stories](#general-user-stories)
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
    + [FAQ & Contact](#faq--contact)
8. [Deployment](#deployment)
9. [Testing](#testing)
   + [Validation](#validation)
   + [Manual Testing](#manual-testing)
   + [Responsive UI Testing](#responsive-ui-testing)
   + [Browser Compatibility](#browser-compatibility)
   + [User Story Testing](#user-story-testing)
11. [Credits](#credits)


![](./the-cosy-narwhal-assets/responsive_ui.png)

## Demo
A live demo to the website can be found [here](https://the-cosy-narwhal-0266caf0f910.herokuapp.com)

## Database

<details>
   <summary>ERD Diagram</summary>
   
![](./the-cosy-narwhal-assets/erd.png)
</details>

## Product Model

The `Product` model represents an individual handmade crochet toy. It defines all the core attributes necessary to manage product listings, variants, pricing, inventory, and image data.

### **Field Breakdown**

| Field | Type | Description |
|-------|------|-------------|
| `code` | `CharField` | Optional internal or SKU code for the product. |
| `name` | `CharField` | The name/title of the product. Required. |
| `description` | `TextField` | A detailed description of the product. |
| `size` | `IntegerField` (choices) | Indicates the product's size, using predefined options: `Small (0)`, `Medium (1)`, and `Large (2)`. Defaults to `Small`. |
| `has_colors` | `BooleanField` | Flags whether the product comes in multiple colors. |
| `color` | `ForeignKey` → `Color` | Optionally links a product to a default or featured color. Can be null/blank. |
| `available_colors` | `ManyToManyField` → `Color` | Links a product to all colors it's available in. |
| `price` | `DecimalField` | The retail price of the product. Max 6 digits with 2 decimal places. |
| `rating` | `DecimalField` | The product's average customer rating (e.g. 4.5). Nullable and defaults to 0. |
| `image` | `ImageField` | Allows uploading an image file via Django. Stored in the `media/` folder using S3. |
| `image_url` | `URLField` | Stores the full URL to the product image. Automatically updated from the `image` field if present. |
| `inventory` | `IntegerField` | Tracks how many units are in stock. Defaults to 0. Cannot be blank. |

### **Custom `save` Method**

The `save()` method is overridden to keep the `image_url` field synchronized with the `image` field. When an image is uploaded:

1. Django saves the image file.
2. If the `image_url` doesn't match the uploaded image's `.url`, it's updated.
3. A second save is triggered with `update_fields=['image_url']` to persist the change.

This ensures consistent linking between uploaded images and their web-accessible URLs.

### **String Representation**

The `__str__` method returns the product’s name, which makes the model more readable in admin panels, shell, and debugging output.

### **Design Notes**

- The `size` field uses `choices`, making it easy to render dropdowns in forms and translate values in templates.
- The use of both `color` (single default color) and `available_colors` (multiple options) allows flexibility in how color variants are handled on product pages.
- Image support includes both uploaded files (`image`) and external URLs (`image_url`), making it compatible with S3, CDN-hosted images, or local storage.


<details>
<summary>Product Model shown here</summary>
   
      class Product(models.Model):
       SIZE = (
           (0,'Small'),
           (1, 'Medium'),
           (2, 'Large')
           )
       code = models.CharField(max_length=254, null=True, blank=True)
       name = models.CharField(max_length=254)
       description = models.TextField()
       size = models.IntegerField(choices=SIZE, null=False, blank=False, default=0)
       has_colors = models.BooleanField(default=False, null=True, blank=True)
   
       color = models.ForeignKey(
           'Color',
           null=True,
           blank=True,
           on_delete=models.SET_NULL,
           related_name='products_by_color'
       )
   
       available_colors = models.ManyToManyField(
           'Color',
           blank=True,
           related_name='products_available_colors'
       )
       
       price = models.DecimalField(max_digits=6, decimal_places=2)
       rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default=0)
       image = models.ImageField(upload_to='media', null=True, blank=True)
       image_url = models.URLField(max_length=1024, null=True, blank=True)
       inventory = models.IntegerField(null=True, blank=False, default=0)
   
       def save(self, *args, **kwargs):
               super().save(*args, **kwargs)
               if self.image:
                   # Update image_url with the full URL to the S3 image
                   if self.image_url != self.image.url:
                       self.image_url = self.image.url
                       # Save again to update image_url field
                       super().save(update_fields=['image_url'])
   
       def __str__(self):
           return self.name
</details>

## Order Model

The `Order` model represents a single customer purchase transaction. It stores all relevant user data, item details, pricing, and shipping information.

### **Field Breakdown**

| Field | Type | Description |
|-------|------|-------------|
| `order_number` | `CharField` | A unique, non-editable identifier for the order. Automatically generated using a UUID. |
| `user` | `ForeignKey` → `AUTH_USER_MODEL` | Links the order to a registered user (optional). Allows guest checkout by making it nullable. |
| `email` | `EmailField` | Email address associated with the order. Used for receipts and contact. Defaults to `'Unknown'`. |
| `items` | `JSONField` | Stores all purchased product data (product IDs, names, quantities, prices) in structured JSON format. |
| `total_price` | `DecimalField` | The total price of the order. Validated to be 0 or greater. |
| `created_at` | `DateTimeField` | Timestamp when the order was created. Automatically set on creation. |
| `updated_at` | `DateTimeField` | Timestamp when the order was last updated. Automatically refreshed on save. |

### **Delivery Information Fields**

| Field | Type | Description |
|-------|------|-------------|
| `full_name` | `CharField` | Full name of the recipient. |
| `street_address1` | `CharField` | Primary street address for delivery. |
| `street_address2` | `CharField` | Secondary address line (optional). |
| `town_or_city` | `CharField` | The town or city of the shipping address. |
| `county` | `CharField` | County or region (optional). |
| `postcode` | `CharField` | Postal code for delivery. |
| `country` | `CharField` | Country of the shipping address. |

Most fields have default values to prevent validation errors during anonymous or incomplete orders.

### **Custom `save()` Method**

The `save()` method is overridden to ensure each order is assigned a unique `order_number` before it’s saved:

1. If `order_number` is not already set,
2. A UUID is generated using the `_generate_order_number()` method,
3. The order is then saved normally.

This guarantees that each order is uniquely identifiable, even for guest checkouts.

### **Private `_generate_order_number()` Method**

`def _generate_order_number(self):
    return uuid.uuid4().hex.upper()`
    
This helper method returns a UUID-based string in uppercase hexadecimal format to uniquely identify the order.

### **String Representation**

The `__str__()` method returns the `order_number`, which helps with readable logs and admin display.

## **Design Notes**

- Uses `JSONField` for `items` to flexibly store varying order structures without requiring a separate `OrderItem` model.
- Supports both registered and guest users (`user` is nullable).
- Automatically tracks creation and update times for auditing and admin use.
- Can be extended later to include order status, payment confirmation, shipping tracking, etc.

<details>
<summary>Order Model shown here</summary>

      class Order(models.Model):
          order_number = models.CharField(max_length=32, unique=True, editable=False)
          user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
          email = models.EmailField(max_length=254, default='Unknown')
          items = models.JSONField()  # or Postgres JSONField if needed
          total_price = models.DecimalField(
              max_digits=10,
              decimal_places=2,
              validators=[MinValueValidator(0)]
          )
          created_at = models.DateTimeField(auto_now_add=True)
          updated_at = models.DateTimeField(auto_now=True)

          # Delivery information fields
          full_name = models.CharField(max_length=100, default='Unknown')
          street_address1 = models.CharField(max_length=80, default='Unknown')
          street_address2 = models.CharField(max_length=80, blank=True)
          town_or_city = models.CharField(max_length=40, default='Unknown')
          county = models.CharField(max_length=80, blank=True)
          postcode = models.CharField(max_length=20, default='Unknown')
          country = models.CharField(max_length=40, default='Unknown')
         
          def save(self, *args, **kwargs):
              if not self.order_number:
                  self.order_number = self._generate_order_number()
              super().save(*args, **kwargs)
         
          def _generate_order_number(self):
              return uuid.uuid4().hex.upper()
         
          def __str__(self):
              return self.order_number
</details>

## Profile Model

The `Profile` model is used to store additional user information related to billing or shipping addresses. It extends the default user model with structured address fields, allowing for quicker checkouts and a better user experience.

### **Field Breakdown**

| Field | Type | Description |
|-------|------|-------------|
| `user` | `OneToOneField` → `AUTH_USER_MODEL` | Links one profile to one user account. Ensures a unique profile per user. If the user is deleted, the profile is also removed (`on_delete=CASCADE`). |
| `full_name` | `CharField` | The user's full name for identification and address purposes. |
| `street_address1` | `CharField` | The primary street address. Required. |
| `street_address2` | `CharField` | Secondary address line (optional). Useful for apartment or suite numbers. |
| `town_or_city` | `CharField` | City or town portion of the user's address. |
| `county` | `CharField` | County or region information. |
| `postcode` | `CharField` | Postal or ZIP code. |
| `country` | `CharField` | Country of residence. Could be upgraded to a country-select field in the future. |

### **String Representation**

The `__str__()` method returns the associated user's `username`, making it easy to identify profiles in the Django admin or logs.

### **Design Notes**

- Used for pre-filling checkout forms and maintaining shipping info between sessions.
- Ensures personal address data is kept separate from the core `User` model.
- The one-to-one relationship enforces a strict 1:1 connection between users and profiles.
- Could be extended to store phone numbers, preferences, or default payment methods.

<details>
<summary>Profile Model shown here</summary>

      class Profile(models.Model):
          user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
          full_name = models.CharField(max_length=150)
          street_address1 = models.CharField(max_length=255)
          street_address2 = models.CharField(max_length=255, blank=True, null=True)
          town_or_city = models.CharField(max_length=100)
          county = models.CharField(max_length=100)
          postcode = models.CharField(max_length=20)
          country = models.CharField(max_length=100)
      
          def __str__(self):
              return self.user.username
</details>

## User Stories
I decided to break the User Stories into three Epics, based on customer needs, admin needs and general functionality of the website. Each of these is explained and explored, along with acceptance criteria and using the Given/When/Then/And structure.
## Customer User Stories

### Browse Products
**User Story**  
_As a guest user, I want to browse all available crochet toys, so I can see what's available without creating an account._

**Acceptance Criteria**
- **Given** I’m on the homepage or product listing page  
- **When** I load the page  
- **Then** I see a grid or list of all available crochet toys with images and titles

### View Product Details
**User Story**  
_As a guest user, I want to view product details including size, color, and images, so I can make informed purchase decisions._

**Acceptance Criteria**
- **Given** I click on a product  
- **When** the product detail page loads  
- **Then** I see the name, description, price, size options, color options, and product image(s)

### Guest Checkout
**User Story**  
_As a guest user, I want to add items to my cart and checkout without creating an account, so I can shop quickly and easily._

**Acceptance Criteria**
- **Given** I have added at least one item to my cart  
- **When** I go to checkout  
- **Then** I am not required to sign up or log in  
- **And** I can proceed directly to payment

### Stripe Payment
**User Story**  
_As a customer, I want to pay securely using Stripe, so I can trust the payment process._

**Acceptance Criteria**
- **Given** I’m on the checkout page  
- **When** I submit my payment information  
- **Then** Stripe securely processes the payment  
- **And** I receive a success or failure message

### Order Confirmation
**User Story**  
_As a customer, I want to receive confirmation of my order, so I know it was successfully placed._

**Acceptance Criteria**
- **Given** I’ve completed a purchase  
- **When** the payment is confirmed  
- **Then** I see an order confirmation page  
- **And** I receive a confirmation email

### Product Reviews
**User Story**  
_As a customer, I want to leave a review on products I’ve purchased, so I can share my experience with others._

**Acceptance Criteria**
- **Given** I have completed an order  
- **When** I navigate to the product page  
- **Then** I can submit a star rating and comment  
- **And** the review is displayed publicly once submitted

### Contact Form for Custom Orders
**User Story**  
_As a potential customer, I want to use a contact form to ask about custom crochet orders, so I can request personalized products._

**Acceptance Criteria**
- **Given** I’m on the contact page  
- **When** I fill in the form with my name, email, and message  
- **And** I click submit  
- **Then** I receive a success message  
- **And** my message is sent to the admin’s email or dashboard

## Admin User Stories

### Add Products
**User Story**  
_As an admin, I want to add new crochet toys to the store, so I can keep my catalog up to date._

**Acceptance Criteria**
- **Given** I am logged in as an admin  
- **When** I access the product dashboard and click “Add Product”  
- **Then** I can enter product name, description, size, color, price, image, and inventory  
- **And** the new product appears on the store page

### Edit Products
**User Story**  
_As an admin, I want to edit product information, so I can fix errors or make updates._

**Acceptance Criteria**
- **Given** I am logged in as an admin  
- **When** I access the product list and “Edit” a product  
- **Then** I can modify the product's fields  
- **And** changes are reflected on the frontend

### Remove Products
**User Story**  
_As an admin, I want to remove discontinued products, so customers only see available items._

**Acceptance Criteria**
- **Given** I am logged in as an admin  
- **When** I access the product list and “Delete” a product  
- **Then** the product is no longer visible in the store

### Update Inventory
**User Story**  
_As an admin, I want to update inventory levels, so I can track stock accurately._

**Acceptance Criteria**
- **Given** I am logged in as an admin  
- **When** I change a product’s inventory count  
- **Then** the new quantity is saved  
- **And** the stock level affects whether it is shown as “in stock” or “sold out”

### View Sales Reports
**User Story**  
_As an admin, I want to view sales reports, so I can monitor revenue and product performance._

**Acceptance Criteria**
- **Given** I am logged in as an admin  
- **When** I access the dashboard's reporting section  
- **Then** I see metrics like total sales, number of orders, and top-selling products

## General User Stories

### Responsive Design
**User Story**  
_As a user, I want the website to be responsive on mobile and desktop, so I can browse and shop comfortably from any device._

**Acceptance Criteria**
- **Given** I visit the site on different screen sizes  
- **When** I interact with the UI  
- **Then** the layout adjusts appropriately  
- **And** all functionality remains usable

### Fast Navigation
**User Story**  
_As a user, I want the platform to load quickly and be easy to navigate, so I can enjoy a smooth shopping experience._

**Acceptance Criteria**
- **Given** I move between pages  
- **When** I click on navigation links  
- **Then** the pages load in under 3 seconds  
- **And** the structure is consistent and intuitive

### Reliable Contact Form
**User Story**  
_As a user, I want the contact form to be accessible and reliable, so I can reach out to the seller without issues._

**Acceptance Criteria**
- **Given** I fill in the contact form with valid data  
- **When** I submit it  
- **Then** the message is sent successfully  
- **And** I see a clear confirmation message

## Design

Taking into account Strategy, Scope, Structure, Skeleton and Surface, together with User Stories and desired outcomes, this is what I considered while building this project.

Given this was a collaborative project, the colour scheme was set by Emma's branding choices, as she already had a logo and colour selection available as well as a main font. Unfortunately, the font she uses in her branding is a Canva exclusive font and as such, we worked together to find one available on Google Fonts that match it closely for consistency.

(cosy marwhal logo here)
(color scheme here)

I chose a fixed top navigation style as it is both consistent accross multiple screen types and is intuative to use and navigate. This also allows for easy and maximal display for products and information as there is nothing "inside" the screen where this infomation would be presented.

(navbar here)

A wireframe for the initial design concepts can be found in the [technologies](#technologies) section.

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

**CSS** - To create a controlled and consistent display for each element and to give a great user experience.

**Javascript** - Several small scripts are implemented on pages that require them such as change listeners to redirect to different colours on the product page and Stripe integration.

**Django** - This was the meat of the project, enabling full Admin user controlled CRUD functionality for the products in the database. I used customised AllAuth templates to enable greater customisation of AllAuth forms.

**Balsamiq** - To create a wireframe, [here]() (pdf format)

**Bootstrap** - To ensure responsive design and usability across all devices, I use a combination of Bootstrap classes and custom css.

## Features
Most of the features I implemented were the direct responses to the User Stories listed above, as such, here follows an explanation of them in greater detail.

### Product Display & Cart
#### All Products
Displays the complete catalog of crochet toys with images, titles, and key details so users can browse available items easily.

#### Product Search
Allows users to search products by keywords, filtering results to quickly find specific crochet toys.

#### Add to Cart
Enables users to add selected products to their shopping cart for purchase.

#### View Cart
Displays the contents of the user’s cart, showing product details, quantities, and total price before checkout.

### Account Registration & User Profile
#### Registration
Provides a form for users to create a new account by entering necessary details such as email and password.

#### User Profiles
Allows registered users to view and update their personal information.

#### Order History
Shows users a history of their past purchases with details of each order.

#### Reviews
Lets users submit ratings and comments on products they have purchased, sharing their experience with others.

### Checkout & Stripe
#### Checkout
Guides users through the process of entering shipping and payment details to complete a purchase.

#### Order Summary
Displays a final review of cart contents, shipping info, and total cost before submitting payment.

#### Stripe Integration
Processes payments securely via Stripe, ensuring customer payment data is protected.

#### Confirmation
Provides an order confirmation page and sends a confirmation email once payment is successful.

### Product Management
#### Add Product
Enables admins to add new crochet toys by entering product details like name, description, price, size, color, images, and inventory.

#### Edit Product
Allows admins to update existing product information and reflect changes on the storefront.

#### Remove Product
Lets admins delete discontinued products to keep the catalog current.

#### Update Inventory
Allows admins to adjust stock levels, which control product availability and display status.

#### Sales Report
Provides admins with detailed metrics such as total sales, total value of sales and top-selling products to monitor business performance within a given time period.

### FAQ & Contact
Provides a list of FAQs and a Contact form to allow users to contact admin.

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
[W3C HTML validator](https://validator.w3.org) seemed to really struggle with the Django generated content so I instead validated the raw HTML after Django rendering, which showed only one error consistently. The scrrenshot beolw shows the error and this occurs because we have both the standard navbar and the mobile version of the navbar loaded at all times, ready for the switch if the screen width threshold is broken. As such, the validator sees two duplicate ids and panics but this can be safely ignored as only one of the menus is active at a time depending on screen width. No other errors detected.

<details>
   <summary>HTML Error Sumamry</summary>
   
![](./the-cosy-narwhal-assets/html_pass.png)
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

| **Feature** | **Expectation** | **Action** | **Result** |
| - | - | - | - |
| All Products | All available products are displayed on the product page. | Navigate to product listing page. | ✅ |
| Product Search | Users can search for products by keyword. | Enter keyword in search bar and view filtered results. | ✅ |
| Add to Cart | Users can add products to their cart without issues. | Click “Add to Cart” on a product page. | ✅ |
| View Cart | Users can view cart contents accurately. | Open cart page to review added products and quantities. | ✅ |
| Registration | New users can create an account. | Fill registration form and submit. | ✅ |
| User Profiles | Registered users can view and edit profile data. | Access profile page and update information. | ✅ |
| Order History | Users can view past orders in their profile. | Navigate to order history section and review orders. | ✅ |
| Reviews | Users can submit and see product reviews. | Submit a review on a purchased product and verify display. | ✅ |
| Checkout | Checkout form captures all necessary info correctly. | Fill checkout details and proceed to payment. | ✅ |
| Order Summary | Order summary displays correct order details before payment. | Review order summary page. | ✅ |
| Stripe Integration | Payment is processed securely via Stripe. | Submit payment and confirm success message. | ✅ |
| Confirmation | Users receive order confirmation page and email. | Complete payment and check for confirmation page/email. | ✅ |
| Add Product | Admins can add new products with full details. | Use dashboard to add a new product. | ✅ |
| Edit Product | Admins can update product information and see changes live. | Modify existing product details and save. | ✅ |
| Remove Product | Admins can delete products and they are removed from the store. | Delete product from dashboard and check storefront. | ✅ |
| Update Inventory | Stock levels update correctly and affect availability. | Change inventory count and verify stock status. | ✅ |
| Sales Report | Admins can view accurate sales data and metrics. | Access reports dashboard and review sales figures. | ✅ |

## Responsive UI Testing


## Browser Compatibility
I tested the site on several popular browsers to ensure functionality and usablity on each. Here are the results of those tests.

| Browser | Issues | Functionality |
| - | - | - |
| Google Chrome | None | Good |
| Apple Safari | None | Good |
| Opera GX | None | Good |
| Mozilla Firefox | None | Good |
| Microsoft Edge | None | Good |

## User Story Testing
Below follows a breakdown of each of the user stories and the results of the implementation and testing of each.

| **User Story** | **Acceptance Criteria** | **Criteria Met?** | **Tested** | **Notes** |
| - | - | - | - | - |
| Browse Products | View a list/grid of all available crochet toys with images and titles on the homepage or product listing page. | ✅ | ✅ | |
| View Product Details | View name, description, price, size, color options, and images on the product detail page. | ✅ | ✅ | |
| Guest Checkout | Add items to cart and checkout without account creation; proceed directly to payment. | ✅ | ✅ | |
| User Checkout | Add items to cart and checkout; delivery information is populated automatically from profile. | ✅ | ✅ | |
| Stripe Payment | Submit payment securely through Stripe and receive success/failure message. | ✅ | ✅ | |
| Order Confirmation | After payment, display confirmation page and send confirmation email. | ✅ | ✅ | |
| Product Reviews | After purchase, leave a star rating and comment on product pages, which displays publicly. | ✅ | ✅ | Product reveiws are currently set to a single reveiw per product, per user |
| Contact Form for Custom Orders | Submit name, email, and message via contact form; receive success message; message sent to admin. | ✅ | ✅ | |
| Add Products (Admin) | Logged-in admin can add product name, description, size, color, price, image, and inventory. Product appears in store. | ✅ | ✅ | |
| Edit Products (Admin) | Logged-in admin can edit product fields and see updates on the frontend. | ✅ | ✅ | |
| Remove Products (Admin) | Logged-in admin can delete products; removed items are no longer visible. | ✅ | ✅ | |
| Update Inventory (Admin) | Admin can change inventory count, which updates product availability (in stock/sold out). | ✅ | ✅ | |
| View Sales Reports (Admin) | Admin can view dashboard metrics such as total sales, orders, and top-selling products. | ✅ | ✅ | |
| Responsive Design | Site adjusts layout and maintains full functionality on various screen sizes. | ✅ | ✅ | |
| Fast Navigation | Pages load in under 3 seconds; site structure is intuitive and consistent. | ✅ | ✅ | |
| Reliable Contact Form | Valid contact form submissions are processed successfully, with clear confirmation. | ✅ | ✅ | |

## Major Bugs & Errors
The only big problem I came up against during development was when I deployed to Heroku. I thought my views and login were broken because my products page showed no information at all and I could not log in. After some testing and debugging it became apparent that the PostGres database was empty and as we were now in production environment, we were no longer reading from the development database. After creating a new superuser and a fixture to instantiate the products in the new database, everything worked as expected.

There was a minor bug when I invited Tom to test the site. When he signed up the site generated a 500 Server Error, but the registration was successful. This happened because I forgot to update Herokus Config Vars with the Email app password after switching to true email sending. After adding this variable, everything worked as intended.

# Credits
I would like to thank my mentor, Medale Oluwafemi and my tutor Tom Cowen for their continued insights and support during this project.

MASSIVE thank you to my best friends Rew and Emma for their continued support and belief in me as I've progressed as well as their help testing functionality and features and their valuable feedback, I love you both.

Thanks go to the Yates Family who have also helped me with testing and troubleshooting. 

I would also like to credit ChatGPT for helping me with specific debugging and formatting issues I faced when building this project, as well as helping me to refactor redundant code.
