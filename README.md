# SOAP-API-PUBLIC-FETCH

## Project Overview

This project demonstrates SOAP web service integration using Python, Zeep, and Flask. The application connects to the public DataAccess Number Conversion service, validates user input, and converts numeric values into their written English equivalents.

**WSDL:** https://www.dataaccess.com/webservicesserver/NumberConversion.wso?WSDL

## Features

- Public SOAP web service consumption
- Conversion of SOAP XML responses into Python data
- GET and POST endpoints using Flask
- Input validation for integers between 1 and 1,000,000
- Custom validation and SOAP fault messages

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

## API Endpoints

**GET:** `/convert?number=123`

**POST:** `/convert`

Example JSON body:

```json
{
  "number": 500
}
```

## Reflection

This assignment helped me better understand how SOAP web services can be integrated into Python applications and accessed through Flask. I started by selecting a public WSDL and using the Zeep library to create a SOAP client. From there, I added input validation to ensure that users could only submit whole numbers within a specified range. I also created GET and POST endpoints so the application could accept different types of requests.

One aspect that surprised me was how Zeep could automatically interpret the WSDL and convert XML responses into Python objects. Before this assignment, I expected that I would need to manually parse the XML response. As I developed the application, I also realized the importance of handling errors rather than assuming every request would succeed.

This assignment strengthened my understanding of service integration, data validation, and exception handling. I would like to learn more about how SOAP services are secured and how their performance compares with REST APIs in larger applications.
