"""Wrapper class for open AI API bot which accesses information from airtable"""
from config import Config
from openai import OpenAI
from airtable_wrapper import Airtable
import tiktoken
from outlook_wraper import OutlookWraper
import datetime
from dateparser import parse
import requests
from functions import save_answers
from knowledge import site_data
import datetime


MEMORY_SIZE = 30 #number of previous messages to store


class AIBot:
    def __init__(self):
        self.memory = ''
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        self.invoices_airtable = Airtable(Config.INVOICE_AIRTABLE_TOKEN, 
                                          Config.INVOICE_AIRTABLE_BASE_ID, 
                                          Config.INVOICE_AIRTABLE_TABLE_ID, 
                                          Config.INVOICE_AIRTABLE_FIELDS)
        self.invoices = self.invoices_airtable.get_all_records()
        
        
        self.inventory_airtable = Airtable(Config.INVENTORY_AIRTABLE_TOKEN, 
                                           Config.INVENTORY_AIRTABLE_BASE_ID, 
                                           Config.INVENTORY_AIRTABLE_TABLE_ID, 
                                           Config.INVENTORY_AIRTABLE_FIELDS)
        self.inventory = self.inventory_airtable.get_all_records()
        
        self.outlook_wraper = OutlookWraper()
        
        
        #measure the number of tokens in memory to avoid exceeding context length
        self.encoder = tiktoken.get_encoding('cl100k_base')
        self.max_memory_tokens = 4000
        
    
    def list_to_string(self, lst):
        output = '['
        
        for el in lst:
            output += f'"{el}"'
            
            if el != lst[-1]:
                output += ", "
        
        output += ']'
        return output
        
            
    def add_memory(self, data, isUser):
        """
        Store last message in memory 

        Args:
            data (str): message
            isUser (bool): true if user sent the last message, false otherwise
        """
        if isUser:
            self.memory += f'USER: {data}'
        else:
            self.memory += f'BOT: {data}'
        
        #ensure that the number of tokens in memory never exceeds the maximum context length
        tokens = self.encoder.encode(self.memory)
        self.memory = self.encoder.decode(tokens[-self.max_memory_tokens:])
    
    
    def inventory_fn(self, message):
        """Function to handle queries related to inventory

        Args:
            message (string): The message sent by the user

        Returns:
            string: The response from the bot
        """
        
        completions = self.client.chat.completions.create(
            messages=[
                    {
                        'role': 'system', 
                        'content': f'''
                                        You are a helpful and smart internal assistant for a business called {Config.BUSINESS_NAME}
                                        Your goal is to help people in the business manage their stock or inventory.
                                        If the user requests any information about the existing invoices use information from the table
                                        below to answer: 
                                        ```{self.inventory}```
                                        Some of the fields in the table are in dutch, so you must translate them to english first. 
                                        You must only use information from the table to answer the query from the user. 
                                        
                                        If the user wants to do any changes to the stock / inventory, you must make the changes requested to the table, 
                                        and then you must output the lines in the table that changed. You must output 'CHANGE$' before the line that has changed, and you must only allow
                                        one change at a time. 
                                        Only output CHANGE if the if the user has provided enough information for the changes that they want to make, otherwise you must collect the name of the inventory
                                        item and the change requested before making the change and outputting the CHANGE command. 
                                        
                                        If the user wants to add an item to the inventory:
                                            - You must first collect the name, current stock and maximum stock of the item
                                            - Once this is collected output CREATE: [name], [current stock], [maximum stock]
                                        
                                        Conversation transcript:
                                        ```{self.memory}```
                                    '''    
                    }, 
                    {
                        'role': 'user', 
                        'content': message
                    }
            ], 
            model='gpt-3.5-turbo-0125', 
            temperature=0.3, 
            max_tokens=3000
        )
        
        response = completions.choices[0].message.content
        response = response.replace('```', '')
        
        #update the stock of a product
        if response.startswith('CHANGE'):
            data = response.split('$')[1].strip()

            #parse string into dict
            row_dict = dict([[el.split(':')[0].strip(), ''.join(el.split(':')[1:]).strip()] 
                              for el in data.split(';')[:-1]
                            ])

            #remove irrelevant fields (only should update the amount of stock or the product name)
            if self.inventory_airtable.update_record({'product': row_dict['product']}, {'huidige_stock': int(row_dict['huidige_stock'])}):
                return f'Ok, I just updated the entry for {row_dict["product"]}'
            else:
                return 'What you are trying to do is not possible. It is likely you entered the name of a product that does not exist.'
        
        elif response.startswith('CREATE'):
            data = response.split(':')[1]
            name, curr_stock, min_stock = data.split(',')
            
            try:
                curr_stock = int(curr_stock.replace(' ', ''))
                min_stock = int(min_stock.replace(' ', ''))
            except Exception as e:
                return 'I am sorry, but I am not able to service your request, please try again. Remember to enter a valid value for the current stock and the minimum stock.'
        
        
            if self.inventory_airtable.create_record({'product': name, 'huidige_stock': curr_stock, 'minimum_stock': min_stock}):
                return f'Ok, I just added an entry for a new product called {name}'
            else:
                return 'Unfortunately, there was an error processing your request. Please try again'
        else:
            return response
    
    
    def callendar_fn(self, message):
        """Function to handle queries related to the callendar

        Args:
            message (string): The message sent by the user

        Returns:
            string: The response from the bot
        """
        
        now = datetime.datetime.now()

        day = now.day
        month = now.month
        year = now.year
        time = now.strftime("%H:%M:%S")

        response = f"Today is {day}/{month}/{year} and the current time is {time}"
        completions = self.client.chat.completions.create(
            messages=[
                    {
                        'role': 'system', 
                        'content': f'''
                                        You are a helpful and smart internal assistant for a business called {Config.BUSINESS_NAME}
                                        Your goal is to help people in the business manage their calendar.
                                        
                                        The current date and time is {response}.
                                        
                                        If the user requests any information about the events in their callendar, use the information below to answer:
                                        ```{self.invoices}```
                                        Some of the fields in the table are in dutch, so you must translate them to english first. 
                                        You must only use information from the table to answer the query from the user. 
                                                                                
                                        If the user wants to add a recurring event to the callendar, such as a cleaning every week, then do the following:
                                            - Ask the user for the days of the week when they want to book their events, the time of the event, the duration of the event, the name of the event and how long the event should repeat for (in weeks)
                                            - For example: 'I want to add a recurring event called 'test' at 12pm every Monday and Tuesday which lasts 2 hours and repeats for 3 weeks
                                            - You must ensure that the user enters all of the required information and that it is valid and has a valid format. For example, the number of weeks that the event repeats for must be an integer
                                            - Once all the information is collected, output RECURRING: [days of week separated by ;], [start_time], [end_time], [name], [start_date], [end_date], [number of weeks that it repeats for]
                                            
                                              The day of the week must be one of: 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
                                              The start time and end time must have the form hh:mm:ss (assume the seconds and minutes are 0 if they are not mentioned)
                                              The date must have the format dd/mm/yyyy
                                              Assume that 1 month is equal to 4 weeks
                                                        
                                        If the user wants to add an event, or cleaning job to the calendar:
                                            - You must ask them for them for the name, the date of the event, the start time and the duration. You must insist that they enter the day and month instead of day of the week. 
                                            - Once the user enters the details, output EVENT: [name], [date], [time], [duration]
                                              The date must have the format dd/mm/yyyy and the time must have the format hh:mm, the duration must also have the format hh:mm
                                              If the year it is not mentioned, assume that it is 2024.         
                                                                              
                                        Only allow the user to add one event at a time
                                        Conversation transcript:
                                        ```{self.memory}```
                                    '''    
                    }, 
                    {
                        'role': 'user', 
                        'content': message
                    }
            ], 
            model='gpt-3.5-turbo-0125', 
            max_tokens=4000, 
            temperature=0.2
        )
        
        response = completions.choices[0].message.content
        
        if response.startswith('EVENT'):
            data = ':'.join(response.split(':')[1:]).strip()
            name, date, time, duration = data.split(',')
            
            start_date = datetime.datetime.strptime(date.strip() + " " + time, "%d/%m/%Y %H:%M")
            duration_hours, duration_minutes = int(duration.split(':')[0]), int(duration.split(':')[1])
            end_date = start_date + datetime.timedelta(hours=duration_hours, minutes=duration_minutes)
            
            status = self.outlook_wraper.create_event(name, start_date, end_date)
            
            if status:
                return f'Ok I just added a new event to your callendar on {start_date} for {name}'
            else:
                return 'There was an error adding the event to the calendar, please try again'
            
            
        elif response.startswith('RECURRING'):
            print(response)
            data = ':'.join(response.split(':')[1:]).strip()
            print(data)
            days_of_week, start_time, end_time, name, start_date, end_date, length_weeks = [item.strip() for item in data.split(',')]

            # Split days_of_week into a list of days
            days_of_week = [day.strip() for day in days_of_week.split(';')]

            # Format the start date and end date
            start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y").strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").strftime("%Y-%m-%d")

            status = self.outlook_wraper.create_recurring_event(name, days_of_week, start_time, end_time, start_date, end_date, str(int(length_weeks) * len(days_of_week)))

            if status:
                return f'Ok, I just added a recurring event every {" and ".join(days_of_week)}'
            else:
                return 'There was an error adding the event to the calendar, please try again'

        return response
    
    
    def invoices_fn(self, message):
        """Function to handle queries related to invoice management

        Args:
            message (string): The message sent by the user
            
        Returns:
            String: The response from the bot
        """
        
        completions = self.client.chat.completions.create(
            messages=[
                    {
                        'role': 'system', 
                        'content': f'''
                                        You are a helpful and smart internal assistant for a business called {Config.BUSINESS_NAME}
                                        Your goal is to help people in the business manage their invoices.
                                        If the user requests any information about the existing invoices use information from the table
                                        below to answer: 
                                        ```{self.invoices}```
                                        Some of the fields in the table are in dutch, so you must translate them to english first. 
                                        You must only use information from the table to answer the query from the user. 
                                        
                                        If the user wants to create a record / invoice, do the following:
                                            - Collect the name, email and phone number of the business that they want to create and once you have the information output
                                            CREATE: [business_name], [phone number], [email]. 
                                            - The email and phone number are not required fields, so if the user does not enter them give their values as "". 
                                            - You must have at least the business name before proceeding to create the invoice. 
                                            - If the user tries to create multiple invoices at the time tell them that you can only do one at a time and forget the information they entered. 
                                        
                                        If the user wants to delete a record / invoice, do the following:
                                            - If they have entered the name of the business that they want to create an invoice for in the message, output
                                            'DELETE, [business name]', nothing else. 
                                            - If they did not enter the name of the business ask them for the name of the business that they want to create an invoice for. 
                                            - If the user tries to delete multiple invoices at the time tell them that you can only do one at a time and forget the information they entered. 
                                        
                                        If the user wants to send an invoice, or mark an invoice as sent, do the following:
                                            - Ask for the name of the business that they want to change the invoice for.
                                            - Once the name of the business is entered output SEND: [business_name]
                                            
                                        You must only do one instruction at a time, if the user tries to do many instructions in one query you must warn them of this. 
                                        
                                        Conversation transcript:
                                        ```{self.memory}```
                                    '''    
                    }, 
                    {
                        'role': 'user', 
                        'content': message
                    }
            ], 
            model='gpt-3.5-turbo-0125', 
            max_tokens=4000
        )
        
        response = completions.choices[0].message.content
        
        #agent has issued CREATE command which indicates that the airtable integration should be used
        if response.startswith('CREATE'):
            data = response.split(':')[1]
            business_name, phone_number, email = data.split(',')
            output = {'Bedrijf': business_name}
            
            #only add optional fields if a value for them was provided
            if phone_number != '':
                output['Telefoonnummer'] = phone_number
            
            if email != '': 
                output['Email'] = email
                
            self.invoices_airtable.create_record(output)
            return f'Ok, I just created a new invoice for {business_name}. Is there anything else I can help you with?'
        
        #agent has issued DELETE command, which indicates that the airtable integration should be used
        elif response.startswith('DELETE'):
            business_name = response.split(',')[1]
            self.invoices_airtable.delete_record({'Bedrijf': business_name})
            
            return f'Ok, I just deleted an invoice for {business_name}. Do you need help with anything else?'

        #agent has issued send command
        elif response.startswith('SEND'):
            business_name = response.split(':')[1]
            
            if self.invoices_airtable.update_record({'Bedrijf': business_name.strip().title()}, {'Status Factuur': 'Factuur Versturen...'}):
                return f'Ok, I just updated the invoice status for {business_name}'

        else:
            return response
    
    
    def chit_chat_fn(self, message):
        """Function to handle normal human interaction workflow

        Args:
            message (string): The message sent by the user

        Returns:
            String: The response from the bot
        """

        #general chat abilities using memory from the conversation
        completions = self.client.chat.completions.create(
            messages=[
                    {
                        'role': 'system', 
                        'content': f'''
                                        You are a helpful and smart internal assistant for a business called {Config.BUSINESS_NAME}
                                        Your goal is to help the people in the business manage inventory and their schedules. 
                                        You should also talk to the users like a human and answer any general questions that they have. 
                                        If the user wants to end the conversation say goodbye in a formal manner.
                                        You must remember that you are capable of accessing the inventory and the invoices of the business. 
                                        
                                        Here is a transcript of the conversation with the user up to now:
                                        ```{self.memory}```
                                        Reply to the user's message appropriately, using the transcript to get the context.
                                    '''    
                    }, 
                    {
                        'role': 'user', 
                        'content': message
                    }
            ], 
            model='gpt-3.5-turbo-0125', 
            temperature=0.3
        )
        
        return completions.choices[0].message.content

    # def cleaning_services_fn(self, message):
    #     """Function to handle questions related to cleaning services
        
    #     Args:
    #         message (string): The message containing the answers from the user

    #     Returns:
    #         String: The response from the bot
    #     """
    #     completions = self.client.chat.completions.create(
    #         messages=[
    #             {
    #                 'role': 'system',
    #                 'content': f'''
    #                             You are a helpful and smart internal  assistant. Your task is to assist the boss by understanding their cleaning needs through a series of questions and capturing their responses for services such as one-time cleaning, regular cleaning, post-construction cleaning, window washing, carpet cleaning, and sofa cleaning. 
                                
    #                             Always ask the user for their name, email, address and phonenumber.
                                
    #                             For each service request, you will ask the following questions to gather the necessary details:
                                
    #                             One-Time Cleaning:
    #                             1. Which standard cleaning tasks do you require?
    #                             2. What is the total square footage (m²) of the space that needs to be cleaned?
    #                             3. Are there specific spots or details that need extra attention?
    #                             4. Are there specific cleaning products we should use, for instance, for a certain type of floor?
    #                             5. Do you also wish the windows to be washed?

    #                             Regular Cleaning:
    #                             1. Desired cleaning frequency
    #                             2. How often per week do you want cleaning to be done?
    #                             3. What is the total square footage (m²) of the space that needs to be cleaned?
    #                             4. What standard cleaning tasks do you expect from us?
    #                             5. Are there specific focus points or additional tasks you want to be executed?

    #                             Post-Construction Cleaning:
    #                             1. Which standard cleaning tasks do you require?
    #                             2. What is the current condition of the spaces?
    #                             3. Are there specific spots or details that need extra attention?
    #                             4. What is the total square footage (m²) of the space that needs to be cleaned?
    #                             5. Are there specific cleaning products we should use, for instance, for a certain type of floor?
    #                             6. Are there any traces of cement grout haze?

    #                             Window Washing:
    #                             1. What is the total square footage (m²) of the space that needs to be cleaned?
    #                             2. How many windows approximately need to be washed?
    #                             3. How dirty are the windows currently?
    #                             4. Are they mostly large or small windows?
    #                             5. Are there specific cleaning products we should use for the windows?

    #                             Carpet Cleaning:
    #                             1. What is the width of the carpet you want to be cleaned? (in meters)
    #                             2. What is the length of the carpet you want to be cleaned? (in meters)
    #                             3. If you wish to have multiple carpets cleaned, please specify the total number of carpets to be cleaned here.
    #                             4. If you have multiple carpets with different dimensions that need cleaning, please specify the dimensions of each carpet here.

    #                             Sofa Cleaning:
    #                             1. How many sofas do you want to be cleaned?
    #                             2. How many seating places do the sofa(s) you want to be cleaned have?
    #                             3. If you have multiple sofas with different seating arrangements to be cleaned, please specify the details of each sofa here.
    #                             4. Is it a corner sofa?

                                
    #                             Important:
    #                             After capturing all this information  make sure to save the user details, the type of cleaning service they need and the necessary details about their service.
    #                             Save the answers here {save_answers}.
                                
    #                             Here is a transcript of the conversation with the boss up to now:
    #                             ```{self.memory}```
    #                             Reply to the boss message appropriately, using the transcript to get the context and when saving the user's information.                                
    #                             '''
    #                 },
    #             {
    #                 'role': 'user', 
    #                 'content': message
    #             }
    #         ], 
    #         model='gpt-4-1106-preview', 
    #         temperature=0
    #     )

    #     response = completions.choices[0].message.content

    #     return response 
     
    def cleaning_services_fn(self, message):
        """Function to handle questions related to cleaning services

        Args:
            message (string): The message containing the answers from the user

        Returns:
            String: The response from the bot
        """
        completions = self.client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': f'''
                                You are a helpful and smart internal  assistant. Your task is to assist the boss by understanding their cleaning needs through a series of questions and capturing their responses for services such as one-time cleaning and sofa cleaning. 

                                Always ask the user for their name, email, address and phonenumber.

                                For each service request, you will ask the following questions to gather the necessary details:

                                One-Time Cleaning:
                                1. Which standard cleaning tasks do you require?
                                2. What is the total square footage (m²) of the space that needs to be cleaned?
                                3. Are there specific spots or details that need extra attention?
                                4. Are there specific cleaning products we should use, for instance, for a certain type of floor?
                                5. Do you also wish the windows to be washed?

                                Sofa Cleaning:
                                1. How many sofas do you want to be cleaned?
                                2. How many seating places do the sofa(s) you want to be cleaned have?
                                3. If you have multiple sofas with different seating arrangements to be cleaned, please specify the details of each sofa here.
                                4. Is it a corner sofa?

                                make  sure to ask user for their name, email, address and phonenumber one after the other.

                                Important:
                                If all this information is captured make sure to save the user details, the type of cleaning service they need and the necessary details about their service output
                                Make the output startwith 'SAVE'
                                SAVE: [name], [phone], [email], [street_name], [city], [service_type], [1 "this is the response from the type of cleaning"]...[5].

                                Here is a transcript of the conversation with the boss up to now:
                                ```{self.memory}```
                                '''
                },
                {
                    'role': 'user',
                    'content': message
                }
            ],
            model='gpt-3.5-turbo-0125',
            temperature=0
        )

        response = completions.choices[0].message.content

        if response.startswith('SAVE'):
            # Extract the parameters from the response
            params = response.split(': ')[1].split(', ')
            name, phone, email, street_name, city, service_type = params[:6]
            # Call the save_answers function with the extracted parameters
            save_answers(name, phone, email, street_name, city, service_type, *params[6:])
            return 'Your answers have been saved.'
        else:
            return response

    
        
    def classify_intent(self, message):
        """Function used to classify the user's intent based on the message, to decide the correct worflow

        Args:
            message (string): The message sent by the user

        Returns:
            string: The response from the bot
        """
        completions = self.client.chat.completions.create(
            messages=[
                {
                    'role': 'system', 
                    'content': f'''
                                As a dedicated assistant for {Config.BUSINESS_NAME}, you are here to assist with inventory management, calendar scheduling, and answer questions related to cleaning services.

                                Based on the user's input, categorize their request into one of the following:

                                1) cleaning services questions.
                                2) Inventory or stock management
                                3) Scheduling or calendar updates
                                4) Invoice queries or customer billing
                                5) Other inquiries which do not involve the ones above

                                Respond with the corresponding category number only.

                                Context:
                                {';'.join(self.memory)}
                                '''      
                }, 
                {
                    'role': 'user', 
                    'content': message
                }
            ], 
            model='gpt-4-1106-preview', 
            temperature=0
        )
        
        response = completions.choices[0].message.content
        
        #try to parse integer from response
        #if output is not valid, default with 5 (other)
        try:
            choice = int(response.replace(')', ''))
        except Exception as e:
            print(f'Classification output parsing error: {e}')
            choice = 5
            
        return choice
      

    def handle_message(self, message):
        """Function to generate the bot's response to a given message. 
           This function starts by adding the user's message to the memory, then calls the correct workflow function and
           finally stores the bot's response in memory

        Args:
            message (string): The message received by the user

        Returns:
            string: the response generated by the bot
        """
        #special command to clear memory
        if message == 'CLEAR MEMORY':
            self.memory = ''
            return 'OK, I just cleared my memory'
        
        self.add_memory(message, True) #add the new message from the user to memory
        
        #get the function to excute based on the intent
        intent_to_function = [self.cleaning_services_fn,
                              self.inventory_fn, 
                              self.callendar_fn, 
                              self.invoices_fn, 
                              self.chit_chat_fn,
                             ]        
        response = ''        
        intent = self.classify_intent(message)

        #get function to execute from the intent number, which gets mapped to a bot state
        fn = intent_to_function[intent - 1]
        response = fn(message)
        
        self.add_memory(response, False)
        
        return response
            
           
if __name__ == '__main__':
    bot = AIBot()
    
    while True:
        msg = input('User: ')
        print(f'BOT: {bot.handle_message(msg)}')