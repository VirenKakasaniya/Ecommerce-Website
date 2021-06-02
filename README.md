<p align="center">
  <p align="center">
    <a href="#" target="_blank">
      <img src="https://github.com/VirenKakasaniya/Coursera_HTML/blob/main/logo.jpg" alt="Viren Kakasaniya" height="130">
    </a>
  </p>
</p>

---

# Django E-commerce

This is a  e-commerce website built with Django and Celery.

## Quick demo of Customer Functionality

![Customer Functionality Demo](https://github.com/VirenKakasaniya/Ecommerce-Website/blob/master/Quick%20Demo/Customer%20functionality.gif)

## Quick demo of Admin Functionality

![Admin Functionality Demo](https://github.com/VirenKakasaniya/Ecommerce-Website/blob/master/Quick%20Demo/Admin%20functionality.gif)



---

## Project Summary

The website displays products. User can signup and login. Users can add and remove products to/from their cart while also specifying the quantity of each item. They can then enter their address and choose Stripe to handle the payment. Also user/customer will get the order status through mail.
Admin can add new employee/admin and Add Product, see the placed order and it's status. Here I used Django, Celery distributed queue and RabbitMQ. 


---

## Running this project

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtualenv env
```

That will create a new folder `env` in your project directory. Next activate it with this command on mac/linux:

```
source env/bin/active
```

Then install the project dependencies with

```
pip install -r requirements.txt
```
You can run celery with this command (for windows)

```
celery -A Ecommerce_Website worker -l info --pool=solo
```

Now you can run the project with this command

```
python manage.py runserver
```

**Note** if you want run email/celery , you will need install RabbitMQ. and you need to enter your mail details in settings.py file.

---



<div align="center">

<i>Other places you can find me:</i><br>

<a href="https://www.linkedin.com/in/virenkakasaniya" target="_blank">Linkedin</a>


</div>
