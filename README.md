# 364final

### **Description of App** ###
This application will allow users to register and login, save their favorite words through a word entry. This word information will be given to the Oxford Dictionary API and create different pages with words, definitions, and other word related information. Users can see their own words and definitions and word-related information, but not other people's. This information will be stored in the db, can also be updated and deleted by the user.

### **How to Use This App** ###
1. Either login with an existing account, or create an account. Otherwise, the only information you can view are words submitted by other users.
2. Once logged in, you can search an english word.
3. Once a word is searched, you can view its linguistic information, and definition(s) through the main menu. Your words will also be visible in the public/complete dictionary tab through the main menu.

### **Required Python Modules** ###
- requests
- api_info (a separate python file with API keys, urls, etc.)

### **Included Routes** ###
- /index -> base.html
- /all_words -> all_words.html
- /form -> form.html
- /your_definitions -> your_definitions.html
- /delete/<word_id> -> deletes a word and redirects to the your_words page
- /update/<word_id> -> update.html (if the form submits correctly, this - redirects to the your_words page)
- /your_words -> your_words.html
- /login -> login.html
- /register -> register.html

### **Documentation README Requirements**

- [X] Create a `README.md` file for your app that includes the full list of requirements from this page. The ones you have completed should be bolded or checked off. (You bold things in Markdown by using two asterisks, like this: `**This text would be bold** and this text would not be`)

- [X] The `README.md` file should use markdown formatting and be clear / easy to read.

- [X] The `README.md` file should include a 1-paragraph (brief OK) description of what your application does

- [X] The `README.md` file should include a detailed explanation of how a user can user the running application (e.g. log in and see what, be able to save what, enter what, search for what... Give us examples of data to enter if it's not obviously stated in the app UI!)

- [X] The `README.md` file should include a list of every module that must be installed with `pip` if it's something you installed that we didn't use in a class session. If there are none, you should note that there are no additional modules to install.

- [X] The `README.md` file should include a list of all of the routes that exist in the app and the names of the templates each one should render OR, if a route does not render a template, what it returns (e.g. `/form` -> `form.html`, like [the list we provided in the instructions for HW2](https://www.dropbox.com/s/3a83ykoz79tqn8r/Screenshot%202018-02-15%2013.27.52.png?dl=0) and like you had to on the midterm, or `/delete -> deletes a song and redirects to index page`, etc).

### **Code Requirements** ###
- [X] Ensure that your `SI364final.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up). **Your main file must be called** `SI364final.py`**, but of course you may include other files if you need.**

- [X] A user should be able to load `http://localhost:5000` and see the first page they ought to see on the application.

- [X] Include navigation in `base.html` with links (using `a href` tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )

- [X] Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.

- [X] Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).

- [X] Must have data associated with a user and at least 2 routes besides `logout` that can only be seen by logged-in users.

- [X] At least 3 model classes *besides* the `User` class.

- [X] At least one one:many relationship that works properly built between 2 models.

- [X] At least one many:many relationship that works properly built between 2 models.

- [X] Successfully save data to each table.

- [X] Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).

- [X] At least one query of data using an `.all()` method and send the results of that query to a template.

- [X] At least one query of data using a `.filter_by(...` and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).

- [X] At least one helper function that is *not* a `get_or_create` function should be defined and invoked in the application.

- [X] At least two `get_or_create` functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).

- [X] At least one error handler for a 404 error and a corresponding template.

- [X] At least one error handler for any other error (pick one -- 500? 403?) and a corresponding template.

- [X] Include at least 4 template `.html` files in addition to the error handling template files.

  - [X] At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.

- [X] At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that *does* accord with other involved sites' Terms of Service, etc).

  - [X] Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source *to the database* (in some way).

- [X] At least one WTForm that sends data with a `GET` request to a *new* page.

- [X] At least one WTForm that sends data with a `POST` request to the *same* page. (NOT counting the login or registration forms provided for you in class.)

- [X] At least one WTForm that sends data with a `POST` request to a *new* page. (NOT counting the login or registration forms provided for you in class.)

- [X] At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.

- [X] Include at least one way to *update* items saved in the database in the application (like in HW5).

- [X] Include at least one way to *delete* items saved in the database in the application (also like in HW5).

- [X] Include at least one use of `redirect`.

- [X] Include at least two uses of `url_for`. (HINT: Likely you'll need to use this several times, really.)

- [X] Have at least 5 view functions that are not included with the code we have provided. (But you may have more! *Make sure you include ALL view functions in the app in the documentation and navigation as instructed above.*)


## Additional Requirements for additional points -- an app with extra functionality!

**Note:** Maximum possible % is 102%.

- [ ] (100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.
- [X]  (100 points) Create, run, and commit at least one migration.
- [ ] (100 points) Include file upload in your application and save/use the results of the file. (We did not explicitly learn this in class, but there is information available about it both online and in the Grinberg book.)
- [ ]  (100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README. (Heroku deployment as we taught you is 100% free so this will not cost anything.)
- [ ]  (100 points) Implement user sign-in with OAuth (from any other service), and include that you need a *specific-service* account in the README, in the same section as the list of modules that must be installed.
