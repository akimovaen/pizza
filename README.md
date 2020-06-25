# Project 3

Web Programming with Python and JavaScript

This application is a Django web application for handling a pizza restaurant’s online orders.

### Menu

The menu items in the application are the same as the menu items of ***Pinocchio's Pizza & Subs***. In the app, they are represented by the **Menu** and **Items** models. The main data of the menu items are in the **Items** model - name, traits (small, large or addition) and price. They are grouped into groups of items which names are defined by the **Menu** model.  
When users register or log into the app they get to the home page with the menu on it. Each group of items has its own image field. If a user clicks on it, it opens a list of all the dishes in that group. Each item that can be ordered has a plus sign to add the item to the *'shopping cart'*. If the selected dish is a pizza with a certain amount of topping or sub, the application will offer to select a certain amount of topping or sub additives, but not more than three.  

### Shopping cart

All the selected items are displayed in the user's *shopping cart*, where a user can see the total amount. The contents of the *shopping cart* is saved even if a user closes the window, or logs out and logs back in again.  A user can edit the content of the *shopping cart* by adding and deleting items.  
In the app, the contents of *shopping cart* are represented by the **ShopCart** model. Each item in the shopping list is saved in the database as one row together with the list of topping or additives to the item. The objects of the **ShopCart** model have the fields 'ordered' and 'order_number'. They are empty until a user clicks on the button for placing the order. After placing the order the fields 'ordered' and 'order_number' are filled in with the value "True" and the order data respectively. Then these objects will  be no longer displayed in the user's *shopping cart*.

### Orders

The data of placed orders are represented in the **Order** model. The objects of the **Order** model have the fields 'number' (set as the maximum value + 1), 'placing_time' (set when the order is placed), 'status' (by default set as 'Pending') and other. Ordered menu items are not represented in this model, they are in the **ShopCart** model, linking to the **Order** model via *ForeignKey* (field 'order_number').  
When a user places an order the app redirects him (or her) to the page where all placed user's orders are displayed. There a user can see the content, 'placing_time' and 'status' of all his (or her) orders.

### Django Admin

Using ***Django Admin*** site administrators have access to a page where they can view any orders that have already been placed. By choosing an order they can view its contents, manually change its status to 'Complete' and enter 'complete_time'. Administrators have another way to change the status of orders: 
- in the list of orders, select those orders which statuses they want to change,
- in the list of actions, select "Mark selected orders as complete",
- click "Go".  
The status will be changed and 'complete_time' will be set automatically.