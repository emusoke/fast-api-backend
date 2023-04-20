# Use Python 3.9 image
FROM python:3.9

# Code is the working directory in our container
WORKDIR /code

# Copy requirements folder to the code folder 
COPY ./requirements.txt /code/requirements.txt

#Copy the migrations script 
COPY ./migrations.py /code/migrations.py

# install required packages. Do not save the locally
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy app folder to code folder in the conatiner
COPY ./app /code/app
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/alembic.ini
COPY ./migrate.sh /code/migrate.sh



# Run the application
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# RUN python migrations.py
ENTRYPOINT ["./migrate.sh"]


