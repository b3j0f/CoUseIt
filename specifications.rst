=============
Specification
=============

---------
Objective
---------

Manage common product location and date availability.

User
====

System user which plan to supply/use products.

- own/use/supply products.
- own/supply stocks.

Product
=======

System core concept which is stocked in stocks and used/supplied by users.

- contained in a stock.
- owned/supplied/used by users.

Stock
=====

Place whose stocks products.

- contain products.
- owned/supplied by users.
- contain capacities.

Capacity
========

Product stock capacity.

- related to an amount of products.
- related to categories of products.

Planning
========

Product use planning.

- related to products.
- related to date time period.
- contains conditions.

Condition
=========

Abstract condition which checks a product use planning.
