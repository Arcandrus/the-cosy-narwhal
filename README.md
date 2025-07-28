# the-cosy-narwhal
Code Institute Project Milestone 4 - Django Full Stack E-Commerce Development


## Table of Contents

1. [Live Demo](#demo)
2. [Database ERD](#database-erd)
   + [CustomUser Model](#customuser-model)
   + [Post Model](#post-model)
   + [Comment Model](#comment-model)
3. [User Stories](#user-stories)
   + [Epics](#epics)
        + [User Profile](#user-profile)
        + [Content Interaction](#content-interaction)     
4. [Design](#design)
5. [Technologies](#technologies)
6. [Features](#features)
    + [Account Registration & User Profile](#account-registration--user-profile)
        + [Registration](#registration)
        + [User Profiles](#user-profiles)
    + [Content Interaction](#content-interactions)
        + [New Posts](#new-posts)
        + [Comments](#comments)
        + [Nested Replies](#nested-replies)
    + [Post Filtering & Finding](#post-filtering--finding)
        + [Categories](#categories)
        + [Favourites](#favourites)
        + [Popular Posts](#popular-posts)
        + [Search](#search)
    + [Edit & Delete](#edit--delete)
8. [Deployment](#deployment)
9. [Testing](#testing)
   + [Validation](#validation)
   + [Manual Testing](#manual-testing)
   + [Responsive UI Testing](#responsive-ui-testing)
   + [Browser Compatibility](#browser-compatibility)
   + [User Story Testing](#user-story-testing)
11. [Credits](#credits)

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


