# WhatsApp Chatbot Project

This project is a chatbot application designed to run on WhatsApp, leveraging the WhatsApp Business API. It's built using Python and Flask, and it can handle various tasks such as responding to user inquiries, managing inventory, scheduling events, and providing information on cleaning services.

## Features

- **Automated Responses**: Engage with users by answering their questions and providing information automatically.
- **Inventory Management**: Users can inquire about stock levels or update inventory through the chatbot.
- **Event Scheduling**: Schedule events or meetings directly through conversations with the chatbot.
- **Cleaning Service Inquiries**: Users can get information about cleaning services, schedule cleanings, or inquire about service details.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Flask
- ngrok (for local development and testing)
- A WhatsApp Business API account

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://yourrepository.com/yourproject.git
   cd yourproject


2. Set Up a Virtual Environment

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install Required Packages
    ```bash
    pip install -r requirements.txt
    Configure Your Application
    ```

```
Update config.py with your WhatsApp Business API credentials, including ACCESS_TOKEN, APP_ID, APP_SECRET, and PHONE_NUMBER_ID.
```


#### Running the Application

1. Start the Flask Application
    ```
    bash
    python3 main.py


2. Expose Your Local Server (Using ngrok)
    ```bash
    ngrok http 8000
    Note the forwarding URL provided by ngrok, which will be used to set up the webhook.
    ```

3. Configure the Webhook
    ```
    Go to your Facebook Developer Console and set the webhook URL to the ngrok forwarding URL followed by /webhook.```

#### Testing
Send a message to your WhatsApp Business number to interact with the chatbot and test its functionalities.

##### Deployment
For production deployment, consider using a cloud service provider like AWS, GCP, or Azure to host your application. Ensure that your production environment is secure and that you've configured your WhatsApp Business API webhook URL to your production server's address.

##### Built With
Python - The programming language used.
Flask - The web framework used.
ngrok - Used to expose local servers behind NATs and firewalls to the public internet over secure tunnels.


##### Versioning
We use SemVer for versioning. For the versions available, see the tags on this repository.



Acknowledgments


