# Item Catalog

The Item Catalog project consists of developing an application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system.

Tables used in this project saved under " itemCatalog.db " 
    
    User        - Contains information about a user.

    Categories  - Contain information about a particular category and user who     created this category. 
    
    CategoryItem- Contains information about a particular item, associated category and the user who created this item.
### User
| id | username | email | hash_password |
|:--:|---------:|:-----:|:-------------:|

### Categories
| id | user_id | name |
|:--:|--------:|:-----:|
    A relation with User. 

### CategoryItem
| id | name | description | price | user_id | category_id |
|----|------|-------------|-------|---------|-------------|
    A relation with User and Categories.

Features successfully implemented:
    
    1. API Endpoint. (http://localhost:5000/catalog.json)
![image](https://user-images.githubusercontent.com/13224901/35765575-bd2d331c-08ec-11e8-8fcf-61926c31d512.png)

    2. CRUD: READ. (http://localhost:5000/catalog.json)
![image](https://user-images.githubusercontent.com/13224901/35765666-cd1f24a4-08ee-11e8-914a-a3d86fdb5eb1.png)

![image](https://user-images.githubusercontent.com/13224901/35765698-8195026e-08ef-11e8-997a-2286e21f1e35.png)

    3. CRUD: CREATE (http://localhost:5000/catalog/new)
![image](https://user-images.githubusercontent.com/13224901/35765760-a6745b42-08f0-11e8-87ef-39ea19e2b28e.png)

    4. CRUD: UPDATE (http://localhost:5000/catalog/ID/edit)
![image](https://user-images.githubusercontent.com/13224901/35768117-22759586-091d-11e8-810d-7ff879f843b4.png)

    5. CRUD: DELETE (http://localhost:5000/catalog/ID/delete)
![image](https://user-images.githubusercontent.com/13224901/35768132-47561e3e-091d-11e8-8246-eff5dc72e9ea.png)

    6. Authorization and Authentication (http://localhost:5000/login)
![image](https://user-images.githubusercontent.com/13224901/35765738-3bd51f56-08f0-11e8-905d-6af59657c90f.png)

![image](https://user-images.githubusercontent.com/13224901/35765739-3f4a872a-08f0-11e8-8ba2-ccf35e09d9c8.png)

![image](https://user-images.githubusercontent.com/13224901/35765731-2420a9a2-08f0-11e8-8ec7-0c9e68b5b033.png)
    
## Requirements

This project uses Linux-based virtual machine and OAuth of 2 popularly used platforms (facebook and google).

1. VirtualBox (https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
2. Vagrant (https://www.vagrantup.com/downloads.html)
3. itemCatalog.db
4. Configuration file from google oauth. (NOT INCLUDED IN THIS DIRECTORY)
5. Configuration file from facebook developers. (NOT INCLUDED IN THIS DIRECTORY)

## Setting up the environment

1. Download the VM configuration(https://github.com/udacity/fullstack-nanodegree-vm)
2. Once the configuration is up navigate to vagrant folder, and start the virtual machine using:
    > vagrant up (This will cause Vagrant to download the Linux operating system and install it.)
    > vagrant ssh (To log in to your newly installed Linux VM)

3. Clone this directory inside vagrant. CD into this directory.
4. Run addDB python script to populate the itemCatalog.db with some dummy data.
    > python addDB.py
    > On completion "added items", all the requirements are set. 
    
## Running the python file

After succesfully setting the virtual environment, database, open the terminal, navigate to the 'catalog' folder.

```
$ python views.py
```
Upon running the above command the server will be running on localhost:5000. Go to your web browser and test the website. One of the dummy credentials (localhost:5000/login)
    ```
    username: peter@example.com |
    password: Pan
    ```