===================
 Calling the story
===================

The most simple valiant to execute story, is to call it as regular
method.

Example
=======

We will use this story definition to discuss details of its execution
further.

.. code:: python

    class CreateUser:

        @story
        @argument('name')
        @argument('email')
        @argument('age')
        def create(self):

            self.validate()
            self.persist()
            self.send_confirmation_email()

        # Steps.

        def validate(self):

            if self.ctx.

Result
======

Given this ``notify_user`` method

.. code:: python

    def notify_user(self):

        # ...
        create = Purchase(status='READY_FOR_SHIPMENT')
        return Result(create)

call of the story will looks like this

.. code:: python

    >>> CreateUser().create(user, product, shipment_details)
    Purchase(status='READY_FOR_SHIPMENT')
