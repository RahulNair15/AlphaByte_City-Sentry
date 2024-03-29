
# CitySentry
## Requirements:

You can find the list of requirements in [requirements.txt](). Main requirements are listed below:


Python >= v3.9
Django >= v3.0


## Directory Structure

- CitySentry is main project containing settings and urls
- 3  modules -> Saferoute, violation guard, waste segregration
- each module has its independent path constisting of views, urls, templates
- static -> Contains all css, js and json files
- templates -> Template files for HTML

<b>Note:</b> Before running the project make sure you have created directories namely <strong>models, uploaded_images</strong> in the project root and that you have proper permissions to access them.

# Running application locally on your machine

### Prerequisite
1. All requirements must be satisfied which are present in requirements.txt
2. Model training for 3rd module which is our waste segregation module for segregating waste into class types and eventually helps in waste management

#### Step 1 : Clone the repo and Navigate to Django Application

`git clone `

#### Step 2: Create virtualenv (optional)

python -m venv venv

#### Step 3: Activate virtualenv (optional)

venv\Scripts\activate

#### Step 4: Install requirements

pip install -r requirements.txt

#### Step 5: Copy and install dependencies properly

Copy the code in correct sequence and in correct format. One must correctly understand the dependencies and eventally solve errors if arises accordingly.

#### step 6: For 1st module (saferoute)

1. cd respective_folder
2. python manage.py makemigrations 
3. python manage.py migrate
4. python manage.py runserver (will start at port 8000)

#### step 7: For 2nd module (violation guard)

1. cd respective_folder
2. python manage.py makemigrations 
3. python manage.py migrate
4. python manage.py runserver 8081 (will start at port 8081)

#### step 8: For 3rd module (waste segregation)

 uvicorn app:app --reload --port 8082 (will start at port 8082)

#### step 9: All module are connected

Simply follow above steps and you are ready to go as there is proper routing between those 3 modules

#### step 10: Admin 

change respective url to end with /admin
