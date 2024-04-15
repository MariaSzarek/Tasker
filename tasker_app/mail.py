import smtplib


MY_EMAIL = "twojtasker@gmail.com"
PASSWORD = "etdarxvcmosjfarc"

quote = "Witaj w Taskerze"
print(quote)
with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(MY_EMAIL, PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs="kkeraz@gmail.com",
        msg = f"Subject: Witaj w Taskerze\n\n{quote}"
    )




