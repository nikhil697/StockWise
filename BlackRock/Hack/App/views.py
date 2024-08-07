from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,request
from .models import *
from django.core.mail import send_mail
import mysql
from django.db import connection,IntegrityError,transaction
from mysql.connector import Error
import subprocess
from django.shortcuts import redirect
import yfinance as yf
from django.http import JsonResponse
import matplotlib.pyplot as plt
import pandas as pd
import io
import urllib, base64
from datetime import datetime


user1='admin'
Password='nikhil2002'
host='blackrock.c3m8wyo4c5hq.ap-south-1.rds.amazonaws.com'
database='blackrock'


import yfinance as yf

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

import json
from transformers import GPTJForCausalLM, GPT2Tokenizer
import requests

conne = mysql.connector.connect(user=user1, password=Password, host=host, database=database)

def login_page(request):
    return render(request, 'App/loginpage.html')

def register(request):
    conne = mysql.connector.connect(user=user1, password=Password, host=host, database=database)
    if request.method == "POST":
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        phone_number = request.POST.get('phone-number')
        email_address = request.POST.get('email-address')
        password = request.POST.get('password')
        
        try:
            Regis = credent(first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    email_address=email_address,
                    password=Password)
            Regis.full_clean()
            Regis.save()            
            print("Account saved successfully")

            subject = 'Account Created'
            message = f'Hello {first_name} {last_name},\n\nYour account has been successfully created. You can now login to your Account using your credentials.'
            from_email = 'nchadha_be21@thapar.edu'
            recipient_list = [email_address]
            send_mail(subject, message, from_email, recipient_list)

            success_message = "Account Registered successfully"
            return render(request, 'App/success_not.html', {'message': success_message})
        except IntegrityError:
            error_msg = "Email is already registered"
        except Exception as e:
            error_msg = "An error occurred: {}".format(str(e))
        
        return render(request, 'App/success_not.html', {'message': error_msg})
        
    else:
        return render(request, 'App/loginpage.html')
    
# def homepage(request):
#     conne = mysql.connector.connect(user=user1, password=Password, host=host, database=database)

#     if request.method== "POST":
#         Email=request.POST.get("uname")
#         password=request.POST.get("psw")

#         try:
#             conne
#             cursor = conne.cursor()
#             query = f"SELECT * FROM credentials WHERE email_address = '{Email}' AND password = '{password}'"
#             cursor.execute(query)
#             user = cursor.fetchone()
            
#             if user:
#                     first_name_query = f"SELECT first_name FROM credentials WHERE email_address='{Email}'"
#                     last_name_query = f"SELECT last_name FROM credentials WHERE email_address='{Email}'"

#                     conne
#                     cursor = conne.cursor()

#                     cursor.execute(first_name_query)
#                     first_name_result = cursor.fetchone()
#                     first_name = first_name_result[0] if first_name_result else None

#                     cursor.execute(last_name_query)
#                     last_name_result = cursor.fetchone()
#                     last_name = last_name_result[0] if last_name_result else None

#                     conne.close()
                    

#                     return render(request, 'App/homepage.html', {'first_name': first_name, 'last_name': last_name})
#             else:
#                 conne.close()
#                 error_message = 'Invalid login credentials. Please try again.'
#                 return render(request, 'App/success_not.html', {'message': error_message})
        
#         except Error as e:
#             # Handle database connection or query errors
#             error_message = 'An error occurred while accessing the database: {}'.format(str(e))
#             return render(request, 'App/success_not.html', {'message': error_message})
        
#     else:
#         # If request method is GET, show the login page
#         return render(request, 'App/loginpage.html')

def homepage(request):
    conne = mysql.connector.connect(user=user1, password=Password, host=host, database=database)

    if request.method == "POST":
        Email = request.POST.get("uname")
        password = request.POST.get("psw")

        try:
            conne
            cursor = conne.cursor()
            query = f"SELECT * FROM credentials WHERE email_address = '{Email}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()

            if user:
                # Store Email in the session
                request.session['email'] = Email
                
                first_name_query = f"SELECT first_name FROM credentials WHERE email_address='{Email}'"
                last_name_query = f"SELECT last_name FROM credentials WHERE email_address='{Email}'"

                cursor.execute(first_name_query)
                first_name_result = cursor.fetchone()
                first_name = first_name_result[0] if first_name_result else None

                cursor.execute(last_name_query)
                last_name_result = cursor.fetchone()
                last_name = last_name_result[0] if last_name_result else None

                conne.close()

                return render(request, 'App/homepage.html', {'first_name': first_name, 'last_name': last_name})
            else:
                conne.close()
                error_message = 'Invalid login credentials. Please try again.'
                return render(request, 'App/success_not.html', {'message': error_message})

        except Error as e:
            error_message = 'An error occurred while accessing the database: {}'.format(str(e))
            return render(request, 'App/success_not.html', {'message': error_message})

    else:
        return render(request, 'App/loginpage.html')


def resetpass(request):
    conne = mysql.connector.connect(user=user1, password=Password, host=host, database=database)

    if request.method == 'POST':
        email_address = request.POST.get('email')
        prevpass = request.POST.get('prevpass')
        newpass = request.POST.get('newpass')
        conne
        cursor = conne.cursor()
        query = f"UPDATE credentials SET password = '{newpass}' WHERE email_address = '{email_address}' AND password = '{prevpass}'"
        cursor.execute(query)
        if cursor.rowcount > 0:
            # Password was successfully updated in the database
            conne.commit()
            conne.close()
            message = 'Password Reset Successful'
            return render(request, 'App/success_not.html', {'message': message})
        else:
            # Password could not be updated in the database
            conne.rollback()
            conne.close()
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'App/success_not.html', {'message': error_message})
    else:
        # if request method is GET, show the reset password page
        return render(request, 'App/resetpass.html')
def resetsuccess(request):
    return render(request, 'App/resetsuccess.html')

def module(request):
    conne = mysql.connector.connect(user=user1, password=Password, host=host, database=database)
    cursor = conne.cursor(dictionary=True)

    # Retrieve Email from the session
    email = request.session.get('email')

    # Print statement to check the session value for email
    print("Session email:", email)

    if email:
        try:
            query = "SELECT first_name, last_name FROM credentials WHERE email_address = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            
            # Print statement to check the fetched user
            print("Fetched user:", user)
            
            if user:
                context = {
                    'first_name': user['first_name'],
                    'last_name': user['last_name']
                }
            else:
                context = {
                    'error': 'User not found'
                }
        except mysql.connector.Error as err:
            print("Error:", err)
            context = {
                'error': f"Database error: {err}"
            }
        finally:
            cursor.close()
            conne.close()
    else:
        context = {
            'error': 'User not logged in'
        }

    return render(request, 'App/modulepage.html', context)

def contactus(request):
    conne = mysql.connector.connect(user=user1, password=Password, host=host, database=database)
    cursor = conne.cursor(dictionary=True)

    # Retrieve Email from the session
    email = request.session.get('email')

    # Print statement to check the session value for email
    print("Session email:", email)

    if email:
        try:
            query = "SELECT first_name, last_name FROM credentials WHERE email_address = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            
            # Print statement to check the fetched user
            print("Fetched user:", user)
            
            if user:
                context = {
                    'first_name': user['first_name'],
                    'last_name': user['last_name']
                }
            else:
                context = {
                    'error': 'User not found'
                }
        except mysql.connector.Error as err:
            print("Error:", err)
            context = {
                'error': f"Database error: {err}"
            }
        finally:
            cursor.close()
            conne.close()
    else:
        context = {
            'error': 'User not logged in'
        }
    return render(request,'App/contactpage.html')

def homepage1(request):
    conne = mysql.connector.connect(user=user1, password=Password, host=host, database=database)
    cursor = conne.cursor(dictionary=True)

    # Retrieve Email from the session
    email = request.session.get('email')

    # Print statement to check the session value for email
    print("Session email:", email)

    if email:
        try:
            query = "SELECT first_name, last_name FROM credentials WHERE email_address = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            
            # Print statement to check the fetched user
            print("Fetched user:", user)
            
            if user:
                context = {
                    'first_name': user['first_name'],
                    'last_name': user['last_name']
                }
            else:
                context = {
                    'error': 'User not found'
                }
        except mysql.connector.Error as err:
            print("Error:", err)
            context = {
                'error': f"Database error: {err}"
            }
        finally:
            cursor.close()
            conne.close()
    else:
        context = {
            'error': 'User not logged in'
        }
    return render(request,'App/homepage.html')



# def viewvalues(request):
#     context = {}

#     if request.method == 'POST':
#         ticker_symbol = request.POST.get('ticker_symbol', 'AAPL')
        
#         # Fetch the company's stock data
#         company = yf.Ticker(ticker_symbol)

#         # Get the company's financials
#         financials = company.financials
#         balance_sheet = company.balance_sheet
#         cashflow = company.cashflow
#         earnings = company.earnings

#         # Get key statistics
#         pe_ratio = company.info.get('trailingPE', 'N/A')
#         beta = company.info.get('beta', 'N/A')
#         market_cap = company.info.get('marketCap', 'N/A')
#         currentPrice = company.info.get('currentPrice', 'N/A')
#         previousClose = company.info.get('previousClose', 'N/A')
#         open = company.info.get('open', 'N/A')
#         dayHigh = company.info.get('dayHigh', 'N/A')
#         dayLow = company.info.get('dayLow', 'N/A')

#         # Check if DataFrames are empty
#         financials_empty = financials is None or financials.empty
#         balance_sheet_empty = balance_sheet is None or balance_sheet.empty
#         cashflow_empty = cashflow is None or cashflow.empty
#         earnings_empty = earnings is None or earnings.empty

#         # Add the data to the context
#         context = {
#             'pe_ratio': pe_ratio,
#             'beta': beta,
#             'market_cap': market_cap,
#             'currentPrice': currentPrice,
#             'previousClose': previousClose,
#             'open' : open,
#             'dayHigh' : dayHigh,
#             'dayLow' : dayLow,
#             'financials': financials.to_html() if not financials_empty else None,
#             'balance_sheet': balance_sheet.to_html() if not balance_sheet_empty else None,
#             'cashflow': cashflow.to_html() if not cashflow_empty else None,
#             'earnings': earnings.to_html() if not earnings_empty else None,
#             'ticker_symbol': ticker_symbol,
#         }

        

#     return render(request, 'App/viewvalues.html', context)

def generate_chart(ticker_symbol):
    # Fetch historical data
    company = yf.Ticker(ticker_symbol)
    hist = company.history(period="1d", interval="1m")
    
    # Generate the plot
    plt.figure(figsize=(10, 5))
    plt.plot(hist.index, hist['Close'], label='Price', color='blue')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(f'Stock Price for {ticker_symbol}')
    plt.legend()
    plt.grid(True)
    
    # Save plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Encode the image to base64
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    
    return image_base64

# def viewvalues(request):
#     context = {}

#     if request.method == 'POST':
#         ticker_symbol = request.POST.get('ticker_symbol', 'AAPL')
        
#         # Fetch the company's stock data
#         company = yf.Ticker(ticker_symbol)

#         # Get the company's financials
#         financials = company.financials
#         balance_sheet = company.balance_sheet
#         cashflow = company.cashflow
#         earnings = company.earnings

#         # Get key statistics
#         pe_ratio = company.info.get('trailingPE', 'N/A')
#         beta = company.info.get('beta', 'N/A')
#         market_cap = company.info.get('marketCap', 'N/A')
#         currentPrice = company.info.get('currentPrice', 'N/A')
#         previousClose = company.info.get('previousClose', 'N/A')
#         open = company.info.get('open', 'N/A')
#         dayHigh = company.info.get('dayHigh', 'N/A')
#         ebitda = company.info.get('ebitda', 'N/A')
#         dayLow = company.info.get('dayLow', 'N/A')
#         volume = company.info.get('volume', 'N/A')
#         bookvalue=company.info.get('priceToBook','N/A')
#         dividendYield=company.info.get('dividendYield','N/A')
#         current_date = datetime.now().strftime("%d %b - close price")

#         if currentPrice != 'N/A' and previousClose != 'N/A':
#             percent = ((currentPrice - previousClose) / previousClose) * 100
#         else:
#             percent = 'N/A'


#         # Generate the chart
#         chart_image = generate_chart(ticker_symbol)

#         # Check if DataFrames are empty
#         financials_empty = financials is None or financials.empty
#         balance_sheet_empty = balance_sheet is None or balance_sheet.empty
#         cashflow_empty = cashflow is None or cashflow.empty
#         earnings_empty = earnings is None or earnings.empty

#         # Add the data to the context
#         context = {
#             'pe_ratio': pe_ratio,
#             'beta': beta,
#             'market_cap': market_cap,
#             'currentPrice': currentPrice,
#             'previousClose': previousClose,
#             'open': open,
#             'dayHigh': dayHigh,
#             'dayLow': dayLow,
#             'ebitda':ebitda/10000000,
#             'volume':volume,
#             'percent':percent,
#             'dividendYield':dividendYield*100,
#             'bookvalue':bookvalue,
#             'market_cap_cr': market_cap/10000000,
#             'current_date':current_date,
#             'financials': financials.to_html() if not financials_empty else None,
#             'balance_sheet': balance_sheet.to_html() if not balance_sheet_empty else None,
#             'cashflow': cashflow.to_html() if not cashflow_empty else None,
#             'earnings': earnings.to_html() if not earnings_empty else None,
#             'ticker_symbol': ticker_symbol,
#             'chart_image': f"data:image/png;base64,{chart_image}",
#         }

#     return render(request, 'App/index1.html', context)

from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
import yfinance as yf



    
    
# openai.api_key = 'sk-proj-nwHW8ggzQOxOvrs2rGSlT3BlbkFJfzT4m3jRS2jmlKXm7ptn'
# def viewvalues(request):
#     context = {}

#     if request.method == 'POST':
#         ticker_symbol = request.POST.get('ticker_symbol', 'AAPL')
        
#         # Fetch the company's stock data
#         company = yf.Ticker(ticker_symbol)

#         # Get the company's financials
#         financials = company.financials
#         balance_sheet = company.balance_sheet
#         cashflow = company.cashflow
#         earnings = company.earnings

#         # Get key statistics
#         pe_ratio = company.info.get('trailingPE', 'N/A')
#         beta = company.info.get('beta', 'N/A')
#         market_cap = company.info.get('marketCap', 'N/A')
#         currentPrice = company.info.get('currentPrice', 'N/A')
#         previousClose = company.info.get('previousClose', 'N/A')
#         open = company.info.get('open', 'N/A')
#         dayHigh = company.info.get('dayHigh', 'N/A')
#         dayLow = company.info.get('dayLow', 'N/A')
#         ebitda = company.info.get('ebitda', 'N/A')
#         volume = company.info.get('volume', 'N/A')
#         bookvalue = company.info.get('priceToBook', 'N/A')
#         dividendYield = company.info.get('dividendYield', 'N/A')
#         current_date = datetime.now().strftime("%d %b - close price")

#         if currentPrice != 'N/A' and previousClose != 'N/A':
#             percent = ((currentPrice - previousClose) / previousClose) * 100
#         else:
#             percent = 'N/A'

#         # Generate the chart
#         chart_image = generate_chart(ticker_symbol)

#         # Check if DataFrames are empty
#         financials_empty = financials is None or financials.empty
#         balance_sheet_empty = balance_sheet is None or balance_sheet.empty
#         cashflow_empty = cashflow is None or cashflow.empty
#         earnings_empty = earnings is None or earnings.empty

#         # Prepare the prompt for the LLM
#         prompt = f"Provide an in-depth analysis of the stock {company.info['longName']} ({ticker_symbol}). Include pros and cons based on the following data:\n\n"
#         prompt += f"Current Price: {currentPrice}\n"
#         prompt += f"Market Cap: {market_cap}\n"
#         prompt += f"PE Ratio: {pe_ratio}\n"
#         prompt += f"Beta: {beta}\n"
#         prompt += f"Total Revenue: {company.info.get('totalRevenue', 'N/A')}\n"
#         prompt += f"Net Income: {company.info.get('netIncomeToCommon', 'N/A')}\n"
#         prompt += f"Dividend Yield: {dividendYield}\n"

#         # Call the OpenAI API
#         response = openai.ChatCompletion.create(
#             engine="gpt-3.5-turbo",
#             prompt=prompt,
#             max_tokens=500
#         )
#         # tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-j-6B')
#         # model = GPTJForCausalLM.from_pretrained('EleutherAI/gpt-j-6B')

#         # input_text = prompt
#         # inputs = tokenizer(input_text, return_tensors='pt')
#         # outputs = model.generate(**inputs)
#         # analysis=tokenizer.decode(outputs[0], skip_special_tokens=True)

#         analysis = response.choices[0].text.strip()

#         # Add the data to the context
#         context = {
#             'pe_ratio': pe_ratio,
#             'beta': beta,
#             'market_cap': market_cap,
#             'currentPrice': currentPrice,
#             'previousClose': previousClose,
#             'open': open,
#             'dayHigh': dayHigh,
#             'dayLow': dayLow,
#             'ebitda': ebitda / 10000000 if ebitda != 'N/A' else 'N/A',
#             'volume': volume,
#             'percent': percent,
#             'dividendYield': dividendYield * 100 if dividendYield != 'N/A' else 'N/A',
#             'bookvalue': bookvalue,
#             'market_cap_cr': market_cap / 10000000 if market_cap != 'N/A' else 'N/A',
#             'current_date': current_date,
#             'financials': financials.to_html() if not financials_empty else None,
#             'balance_sheet': balance_sheet.to_html() if not balance_sheet_empty else None,
#             'cashflow': cashflow.to_html() if not cashflow_empty else None,
#             'earnings': earnings.to_html() if not earnings_empty else None,
#             'ticker_symbol': ticker_symbol,
#             'chart_image': f"data:image/png;base64,{chart_image}",
#             'analysis': analysis,
#         }

#     return render(request, 'App/index1.html', context)

@csrf_exempt
def viewvalues(request):
    conne = mysql.connector.connect(user=user1, password=Password, host=host, database=database)
    cursor = conne.cursor(dictionary=True)

    # Retrieve Email from the session
    email = request.session.get('email')

    # Print statement to check the session value for email
    print("Session email:", email)

    if email:
        try:
            query = "SELECT first_name, last_name FROM credentials WHERE email_address = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            
            # Print statement to check the fetched user
            print("Fetched user:", user)
            
            if user:
                context = {
                    'first_name': user['first_name'],
                    'last_name': user['last_name']
                }
            else:
                context = {
                    'error': 'User not found'
                }
        except mysql.connector.Error as err:
            print("Error:", err)
            context = {
                'error': f"Database error: {err}"
            }
        finally:
            cursor.close()
            conne.close()
    else:
        context = {
            'error': 'User not logged in'
        }
    context = {}

    if request.method == 'POST':
        ticker_symbol = request.POST.get('ticker_symbol', 'AAPL')
        request.session['ticker_symbol'] = ticker_symbol
        
        # Fetch the company's stock data
        company = yf.Ticker(ticker_symbol)

        # Get the company's financials
        financials = company.financials
        balance_sheet = company.balance_sheet
        cashflow = company.cashflow
        # earnings = company.earnings

        # Get key statistics
        pe_ratio = company.info.get('trailingPE', 'N/A')
        beta = company.info.get('beta', 'N/A')
        market_cap = company.info.get('marketCap', 'N/A')
        currentPrice = company.info.get('currentPrice', 'N/A')
        previousClose = company.info.get('previousClose', 'N/A')
        open_price = company.info.get('open', 'N/A')
        dayHigh = company.info.get('dayHigh', 'N/A')
        dayLow = company.info.get('dayLow', 'N/A')
        ebitda = company.info.get('ebitda', 'N/A')
        volume = company.info.get('volume', 'N/A')
        bookvalue = company.info.get('priceToBook', 'N/A')
        dividendYield = company.info.get('dividendYield', 'N/A')
        current_date = datetime.now().strftime("%d %b - close price")

        if currentPrice != 'N/A' and previousClose != 'N/A':
            percent = ((currentPrice - previousClose) / previousClose) * 100
        else:
            percent = 'N/A'

        # Generate the chart
        # chart_image = generate_chart(ticker_symbol)
        chart_image = None
        if ticker_symbol:
            chart_image = generate_chart(ticker_symbol)

        # Check if DataFrames are empty
        financials_empty = financials.empty if financials is not None else True
        balance_sheet_empty = balance_sheet.empty if balance_sheet is not None else True
        cashflow_empty = cashflow.empty if cashflow is not None else True
        # earnings_empty = earnings.empty if earnings is not None else True

        # Prepare the prompt for the Gemini API
        prompt = f"Provide an in-depth analysis of the stock {company.info.get('longName', 'N/A')} ({ticker_symbol}). Include pros and cons based on the following data:\n\n"
        prompt += f"Current Price: {currentPrice}\n"
        prompt += f"Market Cap: {market_cap}\n"
        prompt += f"PE Ratio: {pe_ratio}\n"
        prompt += f"Beta: {beta}\n"
        prompt += f"Total Revenue: {company.info.get('totalRevenue', 'N/A')}\n"
        prompt += f"Net Income: {company.info.get('netIncomeToCommon', 'N/A')}\n"
        prompt += f"Dividend Yield: {dividendYield}\n"

        # Define the Gemini API key and endpoint
        # API_KEY = "AIzaSyDuu2hb3BjBYuPAAfSmBRQADGAceCPCKQY"
        # url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

        # payload = {
        #     "contents": [
        #         {
        #             "role": "user",
        #             "parts": [{"text": prompt}]
        #         }
        #     ]
        # }

        # headers = {
        #     'Content-Type': 'application/json',
        # }

        # try:
        #     # Call the Gemini API
        #     response = requests.post(url, headers=headers, json=payload)
        #     response.raise_for_status()
        #     data = response.json()
        #     analysis = data['contents'][0]['parts'][0]['text']

        # except requests.exceptions.RequestException as e:
        #     analysis = f'An error occurred: {str(e)}'
        # except KeyError:
        #     analysis = 'Error: Unable to retrieve analysis from the response.'

        # Add the data to the context
        context = {
            'pe_ratio': pe_ratio,
            'beta': beta,
            'market_cap': market_cap,
            'currentPrice': currentPrice,
            'previousClose': previousClose,
            'open': open_price,
            'dayHigh': dayHigh,
            'dayLow': dayLow,
            'ebitda': ebitda / 10000000 if ebitda != 'N/A' else 'N/A',
            'volume': volume,
            'percent': percent,
            'dividendYield': dividendYield * 100 if dividendYield != 'N/A' else 'N/A',
            'bookvalue': bookvalue,
            'market_cap_cr': market_cap / 10000000 if market_cap != 'N/A' else 'N/A',
            'current_date': current_date,
            'financials': financials.to_html() if not financials_empty else None,
            'balance_sheet': balance_sheet.to_html() if not balance_sheet_empty else None,
            'cashflow': cashflow.to_html() if not cashflow_empty else None,
            # 'earnings': earnings.to_html() if not earnings_empty else None,
            'ticker_symbol': ticker_symbol,
            'chart_image': f"data:image/png;base64,{chart_image}",
            # 'analysis': analysis,
        }

    return render(request, 'App/index1.html', context)

def mockstock(request):
    context = {}
    email = request.session.get('email')
    
    if not email:
        context['error'] = 'User not logged in'
        return render(request, 'App/mockstock.html', context)

    try:
        conne = mysql.connector.connect(user=user1, password=Password, host=host, database=database)
        cursor = conne.cursor(dictionary=True)

        # Fetch user details
        query = "SELECT first_name, last_name, phone_number FROM credentials WHERE email_address = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if not user:
            context['error'] = 'User not found'
            return render(request, 'App/mockstock.html', context)

        context['first_name'] = user['first_name']
        context['last_name'] = user['last_name']
        phone_number = user['phone_number']

        # Fetch portfolio items
        query = """
            SELECT stock_name, bought_price, quantity, current_price
            FROM portfolio
            WHERE phone_number = %s
        """
        cursor.execute(query, (phone_number,))
        context['portfolio_items'] = cursor.fetchall()

        # Handle stock purchase
        if request.method == 'POST':
            stock_symbol = request.POST.get('stock_symbol')
            quantity = int(request.POST.get('quantity'))

            stock = yf.Ticker(stock_symbol)
            current_price = stock.info['regularMarketPrice']

            # Insert new stock purchase into portfolio
            query = """
                INSERT INTO portfolio (phone_number, stock_name, bought_price, quantity, current_price)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                quantity = quantity + %s,
                current_price = %s
            """
            cursor.execute(query, (phone_number, stock_symbol, current_price, quantity, current_price, quantity, current_price))
            conne.commit()

            return redirect('mockstock')

    except mysql.connector.Error as err:
        context['error'] = f"Database error: {err}"
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conne' in locals():
            conne.close()

    return render(request, 'App/mockstock.html', context)

def get_stock_price(request):
    symbol = request.GET.get('symbol')
    try:
        stock = yf.Ticker(symbol)
        price = stock.info['regularMarketPrice']
        return JsonResponse({'price': price})
    except:
        return JsonResponse({'error': 'Unable to fetch stock price'}, status=400)
    
def streamlit_view(request):
    # Redirect the user to the Streamlit app
    ticker_symbol = request.session.get('ticker_symbol', 'AAPL')
    if ticker_symbol:
        subprocess.Popen(['streamlit', 'run', '/Hack/App/stock.py', '--', ticker_symbol])
    return render(request,'App/waiting.html')


# def flask_proxy(request):
#     try:
#         # Start the Flask app
#         process = subprocess.Popen(['python', 'flask_app/app.py'])

#         # Wait for Flask app to start
#         # time.sleep(5)  # Adjust the sleep time as needed

#         # Make a request to the Flask app
#         response = requests.get('http://127.0.0.1:5000/')

#         return HttpResponse(response.content)

#     except Exception as e:
#         return HttpResponse(f"An error occurred: {str(e)}", status=500)

def flask_proxy(request):
    return redirect('http://127.0.0.1:5002/')
    





