

![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)



# Sila Website

What's Sila? An introduction to Sila Group.


Sila is a large football tournament collection that provides many possibilities for football guess tournaments.

Every match needs an information database so that the members of the league can easily access the information related to the tournament, including the scoreboard and upcoming matches.

This website fulfills the high demand in Sila complex.

Sila website is an site for your football information league
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`


## Deployment

To deploy this project, first clone this repo:

```bash
    git clone https://github.com/MostafaMotahari/Sila-Website.git
```

Go to repo directory, make an virtual enviroment and then install the requirements:
```bash
    cd Sila-Website
    pip install -r requirements
```

In production, use below command to collect all static files:
```bash
    python manage.py collectstatic
```

Now you can easily run the webserver and see the result in https://localhost:8000
```bash
    python manage.py runserver
```
