#!/usr/bin/python3
from settings.loadenv import handleEnv


self_url = handleEnv('SELF_URL')

class HTMLTemp:
    def otp(code, username):
        return f'''<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Unikrib OTP Verification</title>
            </head>
            <body style="background-color: #f6f6f6; font-family: Arial, sans-serif;">
                <div
                style="
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                "
                >
                <!-- Header -->
                <div
                    style="
                    background-color: #fc6c85;
                    color: #ffffff;
                    font-size: 28px;
                    font-weight: bold;
                    text-align: center;
                    padding: 40px;
                    "
                >
                    Unikrib OTP Verification
                </div>
            
                <!-- Body -->
                <div style="padding: 40px;">
                    <p
                    style="
                        font-size: 18px;
                        line-height: 1.5;
                        margin-bottom: 20px;
                        text-align: center;
                    "
                    >
                    Hello {username},
                    </p>
                    <p> Thank you for signing up to Unikrib,</br>
                    Here is your OTP to verify your Unikrib account:
                    </p>
                    <div
                    style="
                        background-color: #000000;
                        color: #ffffff;
                        font-size: 32px;
                        font-weight: bold;
                        text-align: center;
                        padding: 20px;
                        margin-bottom: 20px;
                        border-radius: 8px;
                    "
                    >
                    {code}
                    </div>
                    <p
                    style="
                        font-size: 16px;
                        line-height: 1.5;
                        margin-bottom: 20px;
                        text-align: center;
                    "
                    >
                    This OTP will expire in 30 minutes. If you did not request this OTP,
                    please ignore this email.
                    </p>
                </div>
            
                <!-- Footer -->
                <div
                    style="
                    background-color: #fc6c85;
                    color: #ffffff;
                    font-size: 14px;
                    text-align: center;
                    padding: 20px;
                    "
                >
                    © Unikrib 2023. All Rights Reserved.
                </div>
                </div>
            </body>
            </html>'''

    def welcome(username):
        return f'''<!DOCTYPE html>
            <html>
                <head>
                    <title>Welcome to Unikrib!</title>
                    <meta charset="utf-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1" />
                </head>
                <body>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    border="0"
                    align="center"
                    width="600"
                    style="max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; border-collapse: collapse; background-color: #f5f5f5;"
                    >
                <tr>
                    <td
                    style="padding: 20px; background-color: #ffffff; border-radius: 10px;"
                    >
                    <div
                        style="
                        background-color: #fc6c85;
                        color: #ffffff;
                        font-size: 32px;
                        font-weight: bold;
                        text-align: center;
                        padding: 20px;
                        margin-bottom: 20px;
                        border-radius: 8px;
                        "
                    >
                        Welcome to Unikrib
                    </div>
                    <p style="font-size: 18px; line-height: 1.5;">
                        Hi {username},<br />
                        We're thrilled to have you join us here at Unikrib! You're now part
                        of a global community of people advertising their products or services.
                        Enjoy our world of endless possibilities!
                    </p>
                    <p style="font-size: 18px; line-height: 1.5;">
                        To get started, just log in to your account and start exploring! If
                        you have any questions or feedback, feel free to reach out to our
                        support team at Unikrib@gmail.com.
                    </p>
                    <p style="font-size: 18px; line-height: 1.5;">
                        Thanks for choosing Unikrib, and happy shopping!
                    </p>
                    </td>
                </tr>
                <tr>
                    <td
                    style="text-align: center; padding: 20px; background-color: #ffffff; border-radius: 10px;"
                    >
                    <p style="font-size: 16px;">
                        If you didn't create an account with Unikrib, please disregard
                        this email.
                    </p>
                    </td>
                </tr>
                </table>
                </body>
            </html>'''

    def resetpassword(otp, username):
        return f'''<!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>Unikrib OTP Verification</title>
                </head>
                <body style="background-color: #f6f6f6; font-family: Arial, sans-serif;">
                    <div
                        style="
                            max-width: 600px;
                            margin: 0 auto;
                            background-color: #ffffff;
                            border-radius: 8px;
                            overflow: hidden;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                        "
                    >
                    <!-- Header -->
                    <div
                        style="
                        font-size: 28px;
                        font-weight: bold;
                        padding: 40px;
                        "
                    >
                    Reset Password
                    </div>
                
                    <!-- Body -->
                    <div style="padding: 40px;">
                        <p
                        style="
                            font-size: 18px;
                            line-height: 1.5;
                            margin-bottom: 20px;
                            text-align: center;
                        "
                        >
                        Hello there {username},
                        </p>
                        <p
                        style="
                            font-size: 16px;
                            line-height: 1.5;
                            margin-bottom: 20px;
                        "
                        >
                        You recently requested to reset your password for your Unikrib account. Use the following OTP to reset your password:
                        </p>
                        <div
                        style="
                        background-color: #000000;
                        color: #ffffff;
                        font-size: 32px;
                        font-weight: bold;
                        text-align: center;
                        padding: 20px;
                        margin-bottom: 20px;
                        border-radius: 8px;
                        "
                        >
                        {otp}
                        </div>
                        <p
                        style="
                            font-size: 16px;
                            line-height: 1.5;
                            margin-bottom: 20px;
                            text-align: center;
                        "
                        >
                        This OTP will expire in 30 minutes. If you did not request this OTP,
                        please ignore this email.
                        </p>
                    </div>
                
                    <!-- Footer -->
                    <div
                        style="
                        background-color: #fc6c85;
                        color: #ffffff;
                        font-size: 14px;
                        text-align: center;
                        padding: 20px;
                        "
                    >
                        © Unikrib 2023. All Rights Reserved.
                    </div>
                    </div>
                </body>
            </html>'''
  
    def verifyLink(code, username, user_id):
        return f'''<!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>Unikrib Verification Link</title>
                </head>
                <body style="background-color: #f6f6f6; font-family: Arial, sans-serif;">
                    <h1> Hey {username}!</h1></br>
                    <p>Please verify your email address.

                    Use the following link to confirm your email address:</br></br>
                    <div
                        style="
                        background-color: #000000;
                        color: #ffffff;
                        font-size: 32px;
                        font-weight: bold;
                        text-align: center;
                        padding: 20px;
                        margin-bottom: 20px;
                        border-radius: 8px;
                        ">
                        <a href="{self_url}/user/{user_id}/verify-email?code={code}">Verify Email</a>
                    </div>
                    <p>The link will expire in 30 minutes.</p>
                    
                    </br></br>If you did not sign up for unikrib, please ignore this email. 
                    
                    </br></br>This is an automated message. Please do NOT reply to this email.
                    
                    </br>Best Wishes<p>
                </body>
            </html>'''

    def newReport(topic, reporter, reported, description):
        return f'''<!DOCTYPE html>
            <html>
                <head>
                    <title>Welcome to Unikrib!</title>
                    <meta charset="utf-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1" />
                </head>
                <body>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    border="0"
                    align="left"
                    width="600"
                    style="max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; border-collapse: collapse; background-color: #f5f5f5;"
                    >
                <tr>
                    <td
                    style="text-align: left; padding: 20px; background-color: #ffffff; border-radius: 10px;"
                    >
                    <div
                        style="
                        background-color: #fc6c85;
                        color: #ffffff;
                        font-size: 32px;
                        font-weight: bold;
                        text-align: center;
                        padding: 20px;
                        margin-bottom: 20px;
                        border-radius: 8px;
                        "
                    >
                        New Report notification
                    </div>
                    <p style="font-size: 18px; line-height: 1.5;">
                        A new report has been made:</br>
                        -----------------------</br>
                        Reported: {reported},</br>
                        Reporter: {reporter},</br>
                        Topic: {topic},</br>
                        Description: {description}.</br>
                        -----------------------</br>
                        <br>
                        Please look into it.
                    </td>
                </tr>
                </table>
                </body>
            </html>'''

    def notifyAgent(first_name):
        return f'''<!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>Apartment inspection request</title>
                </head>
                <body style="background-color: #f6f6f6; font-family: Arial, sans-serif;">
                    <h1> Hey {first_name}!</h1></br>
                    <p>Someone has requested inspection on your posted apartment.

                    Please use the following link to accept or deny request:</br></br>
                    <div
                        style="
                        background-color: #000000;
                        color: #ffffff;
                        font-size: 32px;
                        font-weight: bold;
                        text-align: center;
                        padding: 20px;
                        margin-bottom: 20px;
                        border-radius: 8px;
                        ">
                        <a href="https://unikribafrica.com/static/notification-page.html">Go to unikrib</a>
                    </div>
                    
                    </br></br>If you did not post any apartment on unikrib, please ignore this email. 
                    
                    </br></br>This is an automated message. Please do NOT reply to this email.
                    
                    </br>Best Wishes<p>
                </body>
            </html>'''

    def requestAccepted(first_name, itemId):
        return f'''<!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>Apartment inspection request accepted</title>
                </head>
                <body style="background-color: #f6f6f6; font-family: Arial, sans-serif;">
                    <h1> Hey {first_name}!</h1></br>
                    <p>Your request for inspection on an apartment has been accepted.

                    Come contact the agent to physically check out the apartment</br></br>
                    <div
                        style="
                        background-color: #000000;
                        color: #ffffff;
                        font-size: 32px;
                        font-weight: bold;
                        text-align: center;
                        padding: 20px;
                        margin-bottom: 20px;
                        border-radius: 8px;
                        ">
                        <a href="https://unikribafrica.com/static/Apartment-info-page.html?id=''' + itemId + '''">Go to unikrib</a>
                    </div>
                    
                    </br></br>If you did not request any apartment on unikrib, please ignore this email. 
                    
                    </br></br>This is an automated message. Please do NOT reply to this email.
                    
                    </br>Best Wishes<p>
                </body>
            </html>'''

    def requestDenied(first_name):
        return f'''<!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>Apartment inspection request denied</title>
                </head>
                <body style="background-color: #f6f6f6; font-family: Arial, sans-serif;">
                    <h1> Hello {first_name}!</h1></br>
                    <p>Your request for inspection on an apartment has been denied.</p>

                    Don't worry, this doesn't have to be the end of your search.
                    Come check out more recent apartments at 
                    <a href="https://unikribafrica.com/static/Apartment-page.html">Unikrib apartments</a>
                    </br></br>
                    
                    </br></br>If you did not request any apartment on unikrib, please ignore this email. 
                    
                    </br></br>This is an automated message. Please do NOT reply to this email.
                    
                    </br>Best Wishes<p>
                </body>
            </html>'''

    def newReview(first_name):
        return f'''<!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>Apartment inspection request denied</title>
                </head>
                <body style="background-color: #f6f6f6; font-family: Arial, sans-serif;">
                    <h1> Hello {first_name}!</h1></br>
                    <p>A new review has been left for you.</p>

                    Please visit your profile page to view all your reviews 
                    <a href="https://unikribafrica.com">Go to unikrib</a>
                    </br></br>
                    
                    </br></br>This is an automated message. Please do NOT reply to this email.
                    
                    </br>Best Wishes<p>
                </body>
            </html>'''
    
    def user_verification(*args, **kwargs):
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        face_image = kwargs.get('face_image')
        id_image = kwargs.get('id_image')
        user_id = kwargs.get('user_id')

        return f'''<!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8"/>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                    <title>User verification</title>
                </head>
                <body style="background-color:#f6f6f6; font-family: Arial, sans-serif;">
                    <h1> Hello admins, </h1>
                    <p> A new user is requesting for verification, His/her details are as follows:>

                    <br>
                    <p>first_name: {first_name},</p>
                    <p>last_name: {last_name},</p>
                    <p>face_image: {face_image},</p>
                    <p>id_image: {id_image},</p>
                    <p>user_id: {user_id}.</p>

                    <br>
                    <hr>
                    <br>

                    <p><a href='{self_url}/verify_user/{user_id}/accept'>
                    We have verify this user's info and he can be verified ✅</a></p>
                    <br>
                    <p><a href='{self_url}/verify_user/{user_id}/deny'>
                    This user is not clear to be verified ❌</a></p>
                    <br>

                    <p>Please treat as urgent!.</p>
                </body>
            </html>'''
