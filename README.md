

![Logo](https://github.com/MostafaMotahari/Sila-Website/blob/master/images/website_poster.png)



# Sila Website

What's Sila? An introduction to Sila Group.


Sila is a large football tournament collection that provides many possibilities for football guess tournaments.

Every match needs an information database so that the members of the league can easily access the information related to the tournament, including the scoreboard and upcoming matches.

This website fulfills the high demand in Sila complex.

Sila website is an site for your football information league
## Run Locally

First clone this repo:

```bash
    git clone https://github.com/MostafaMotahari/Sila-Website.git
```

Go to repo directory, make a virtual environment and then install the dependencies:
```bash
    cd Sila-Website
    pip install -r requirements
```

In production, use below command to collect all static files:
```bash
    python manage.py collectstatic
```

Now you can easily start the webserver and see the result in https://localhost:8000
```bash
    python manage.py runserver
```
## Documentation

[Documentation](https://linktodocumentation)


## TODO

- Dockerize project


## License

[MIT](https://choosealicense.com/licenses/mit/)

