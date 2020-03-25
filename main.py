import email
import imaplib
import os
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome('./chromedriver')

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASS')
SERVER = 'imap.gmail.com'

# connect to the server and go to its inbox
mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)
# we choose the inbox but you can select others
mail.select('inbox')

# we'll search using the ALL criteria to retrieve
# every message inside the inbox
# it will return with its status and a list of ids
status, data = mail.search(None, 'FROM', '"Chris Bashford (Classroom)"')

print(data)

mail_ids = []

# split a chunk of email ids into individual ids
for block in data:
    mail_ids += block.split()

mail_content_list = []

# now for every id we'll fetch the email
# to extract its content
for i in mail_ids:
    # the fetch function fetch the email given its id
    # and format that you want the message to be
    status, data = mail.fetch(i, '(RFC822)')

    # the content data at the '(RFC822)' format comes on
    # a list with a tuple with header, content, and the closing
    # byte b')'
    for response_part in data:
        # so if its a tuple...
        if isinstance(response_part, tuple):
            # we go for the content at its second element
            # skipping the header at the first and the closing
            # at the third
            message = email.message_from_bytes(response_part[1])

            mail_from = message['from']
            mail_subject = message['subject']

            # then for the text we have a little more work to do
            # because it can be in plain text or multipart
            # if its not plain text we need to separate the message
            # from its annexes to get the text
            if message.is_multipart():
                mail_content = ''
                # on multipart we have the text message and
                # another things like annex, and html version
                # of the message, in that case we loop through
                # the email payload
                for part in message.get_payload():
                    # if the content type is text/plain
                    # we extract it
                    if part.get_content_type() == 'text/plain':
                        mail_content += part.get_payload()
            else:
                # if the message isn't multipart, just extract it
                mail_content = message.get_payload()

            # and then let's show its result
            msg = [mail_from, mail_subject, mail_content]
            mail_content_list.append(msg)

message_content = mail_content_list[-1][2]
url = re.search("https:\/\/classroom.google.com\/c\/\w+\/a\/\w+\/details", message_content).group()

driver.get(url)


field = driver.find_element_by_class_name('whsOnd')
field.send_keys(EMAIL)
field.send_keys(Keys.RETURN)

time.sleep(2)

field = driver.find_element_by_class_name('whsOnd')
field.send_keys(PASSWORD)
field.send_keys(Keys.RETURN)

# CSS class for attached files: uqZtlf x0HGk QRiHXd MymH0d maXJsd
# WaitForElement()??
time.sleep(10)
attch = driver.find_element_by_class_name('uqZtlf')
doc = attch.get_attribute('href')
driver.get(doc)
