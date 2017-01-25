=============
Specification
=============

---------
Objective
---------

Use/supply/stock products in common.

Account
=======

An account owns, supplies, requests and uses products.

- ownes : created products.
- supplies : supplied products.
- requests : requested products. Solved with the object Request.
- uses : used products. Solved with the object Using.

Location
========

Product location.

- longitude : location longitude.
- lattitude : location lattitude.
- datetime : location time.
- address : location address.

Product
=======

- name : product name
- description : (optional) product description.
- categories : product categories.
- owners : at least one account which has created the product and can destroy it.
- suppliers : 0 or more account which can supply the product and change its properties.
- using : 0 or more Using.
- users : dynamic property which returns current user accounts.
- stock : (optional) current stock.
- conditions : (optional) request conditions.
- requests : product requests.
- states : product states.
- locations : product locations.

Stock
=====

Product which stocks products.

- products : contained products.
- capacities : product capacities.

Condition
=========

Base object for specifying using conditions.

- products : products to request.
- vevent : date time while the condition occurs.
- check(request) : validate input request.

Request
=======

Base object for requesting products.

- products : requested products.
- accounts : requesting accounts.
- vevent : object period use.

State
=====

Product state.

- detail : state details.
- medias : state media.
- datetime : creation time.

Media
=====

State media.

- media : file media.

Using
=====

Used by accounts for using products.

- accounts : accounts using the product.
- products : products in use.
- request : (optional) origin request.
- datetime : creation time.

Category
========

Product category.

- name : unique category name.
- parent : parent category (for example, a car type is a sub category of a car).
- children : children category.

Capacity
========

Product stock capacity.

- categories : at least one category.
- used : number of stocked products of self categories.
- total : total capacity of a stock for self categories.
