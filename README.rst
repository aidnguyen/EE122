EE122 Project Example Code
==========================

The code will establish connection to the pre-created Thing in your AWS IoT account and
publish some data to topics ``EE122/project`` and ``EE122/final-sol`` every 30 seconds.
Then, follow instructions to see data for only topic ``EE122/project`` posting in the
Post Test Server http://ptsv2.com/

Requirements
------------

Code are written in Python
First, run::

    pip install -r requirements.txt


Create a Policy for AWS IoT Certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is needed for AWS IoT Things to be able to publish/subscribe messages

Go to AWS Console, choose *AWS IoT Core*, then click *Secure* -> *Policies*

Then click *Create*. Give a name to policy. In *Add statements* section, fill ``iot:*`` to
*Action* and ``*`` to *Resource ARN*. Check *Allow* box. Then click *Create*.


Create a AWS IoT Thing
~~~~~~~~~~~~~~~~~~~~~~

Go to AWS Console, choose *AWS IoT Core*, then click *Manage Thing* -> Create a Single Thing

Give it a name, then click *Next* (other information is not necessary for this example)

Choose *One-click certificate creation*, then download all certificates file, including root CA
certificate of AWS IoT if you don't have it (STORE THOSE CERT FILES IN THE SAME DIRECTORY WITH
``publisher.py``). Click *ACTIVATE* first then click *Attach Policy*.

Choose the policy you just created above and click *Register Thing*.

Create A Lambda Function:
~~~~~~~~~~~~~~~~~~~~~~~~~
Log in to AWS Console, choose *Lambda*, then click *Create function*

Choose *Author from scratch* (which is default option), give the function a name, choose *Python 2.7* for *Runtime*.

In *Role*, choose *Create New Role from Template(s)*. Give it a name. Then in Policy Template, choose
both *AWS IoT Button permissions* and *Basic Edge Lambda permissions*

Upload code for Lambda Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Our lambda function will use ``requests`` library to send POST request to a POST Test Server.
This example already include the deployment packet for you to upload to the newly created
lambda function.

From *AWS Lambda* main page, click on the function you just created.
In *Code Entry Type*, choose *Upload a .zip file*, then upload provided ``lambda.zip`` and click *SAVE*.

You know should see this block of code show up in your lambda function

.. code-block:: python

    import requests


    def lambda_handler(event, context):

        url = "http://ptsv2.com/t/EE122-project/post" # MAKE SURE THIS LINK IS AVAILABLE
        response = requests.session().post(url, data=event, timeout=10)


.. note:: You need to CHECK for the existence of ``url`` for lambda function to work correctly.

Create A Rule
~~~~~~~~~~~~~

In *AWS IoT Core* main page, choose *Act* then click *Create*

Give it a name. In *Attribute*, fill in with ``*`` and in *Topic filter*, fill in ``EE122/project``.
Then you should see ``SELECT * FROM 'EE122/project'`` in *Rule query statement*.

Then in *Set one or more actions*, click *Add action*.
Choose *Invoke a Lambda function passing the message data* and click *Configure Action*

Then choose the function you just created above and clikc *Add Action*.

Finally, click *Create Rule*


Run Example Code
----------------

Run the following code with some replacement::

    python publish.py <thing_name> <host> <root-CA-pem> <certificate.crt> <private-key>

``thing_name``: the name of AWS IoT Thing you just created above

``host``: in the format *xxx...xxxx.iot.<region>.amazonaws.com*. If
you don't know this, go to AWS IoT -> Manage Thing -> click to the Thing you just created above -> Interact.
You should see your REST API endpoint their.

``root-CA-pem``: root CA certificate of AWS IoT. You should already download it during create a new AWS IoT Thing.
If you forget to download it, you can download a copy from this repository (``root-CA.pem``)

``certificate.crt``: You should already download it during create a new AWS IoT Thing.
Its name should have the format  *xx...xxx-certificate.pem.crt* (unless you change the name after downloaded)

``private-key``: You should already download it during create a new AWS IoT Thing.
Its name should have the format  *xx...xxx-private.pem.key* (unless you change the name after downloaded)

After running the command, go to http://ptsv2.com/t/EE122-project and you should see some DUMPS there.







