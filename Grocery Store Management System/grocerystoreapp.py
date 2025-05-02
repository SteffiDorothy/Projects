from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
import oracledb
import pandas as pd
import os

def connect_to_db():

    try:
        
        dsn = oracledb.makedsn('oracle.wpi.edu', 1521, sid = 'ORCL')
        db = oracledb.connect(user = 'zzhang18',
                               password = 'ZZHANG18',
                               dsn = dsn)
        return db
        
    except oracledb.DatabaseError as e:
        raise
    

def fetch_data(sql, params = None):
    '''
    Execute SQL statement to pull data and store in dataframe
    '''
    
    try:
        cursor = connect_to_db().cursor()
        cursor.execute(sql, params or [])
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] # Extract column names
        df = pd.DataFrame(data, columns=columns) # Create dataframe
        cursor.close() # Close connection

        return df

    except oracledb.DatabaseError as e:
        raise
        

def insert_data(sql, data):
    '''
    Documentation: https://python-oracledb.readthedocs.io/en/latest/user_guide/batch_statement.html
    '''

    try:
        con = connect_to_db()
        cursor = con.cursor()

        cursor.executemany(sql, data)

        con.commit()
        cursor.close()
               
    except oracledb.DatabaseError as e:
        raise
        

def update_data(sql, data):
    '''
    Documentation: https://python-oracledb.readthedocs.io/en/latest/user_guide/batch_statement.html

    '''
    try:

        con = connect_to_db()
        cursor = con.cursor()

        cursor.executemany(sql, data)

        con.commit()
        cursor.close()
               
    except oracledb.DatabaseError as e:
        raise
        

# Create instance
app = Flask(__name__)

# Secret key for session
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST']) # Route is the place to go (/ represents the base url or the homepage)
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Pull username and password from DB
        real_password = fetch_data('SELECT PASSWORD FROM ACCOUNT WHERE USERNAME = :1',[username])

        # Validate credentials
        if  password == real_password['PASSWORD'][0]:
            session['user'] = username
            return redirect(url_for('home')) 
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/home')
def home():

    return render_template('DailyPick.html')


@app.route('/profile', methods = ['GET','POST'])
def profile():
    try:

        # Get the user email from session
        username = session.get('user')

        # If user doesn't exist throw an error
        if not username:
            return "Unauthorized", 401  # Or redirect to login

        # SQL for grabbing user info
        account_sql = '''
            SELECT username, phone, paypref
            FROM ACCOUNT
            WHERE username = :1
        '''
        
        # Store information in DF
        df = fetch_data(account_sql, [(username)])

        # Collect user preferences
        if request.method == 'POST':

            diet = request.form.get('diet')
            brand = request.form.get('brand')
            budget = request.form.get('budget')

            # Check if user already exists in preferences table
            pref_sql = '''
            SELECT * FROM PREFERENCES WHERE USERNAME = :1
            '''

            # Store results in df
            pref_df = fetch_data(pref_sql, [(username)])

            # If empty use INSERT statement
            if pref_df.empty == True:
                insert_sql = '''
                INSERT INTO PREFERENCES (username, max_budget, dietaryrestric, prefbrands)
                VALUES (:1, :2, :3, :4)
                '''

                # Execute
                insert_data(insert_sql, [(username, budget, diet, brand)])

                # Flash success message
                flash("Preferences saved successfully!", "success")


            # Else use UPDATE statement
            else:
                update_sql = '''
                UPDATE PREFERENCES SET
                max_budget = :1, 
                dietaryrestric = :2, 
                prefbrands = :3
                WHERE USERNAME = :4
                '''

                # Execute
                update_data(update_sql, [(budget, diet, brand, username)])

                # Flash message
                flash("Preferences saved successfully!", "success")

        # Return template
        return render_template('Account.html',
                               username=df['USERNAME'].iloc[0],
                               phone=df['PHONE'].iloc[0],
                               credit_card= df['PAYPREF'].iloc[0])
    
    # Error handling
    except oracledb.DatabaseError as e:
        print(f"Database Error: {e}")
        return "Internal Server Error", 500


@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():

    # Collect new account details
    if request.method == 'POST':
        try:
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            phone = request.form['phone']
            paypref = request.form['paypref']

            # INSERT statement
            insert_sql = '''
            INSERT INTO ACCOUNT (createDate, phone, password, email, username, paypref)
            VALUES (CURRENT_DATE, :1, :2, :3, :4, :5)
            '''

            # Execute
            insert_data(insert_sql, [(phone, password, email, username, paypref)]) 

            # Return to login page
            return redirect(url_for('login'))  # Redirect to login

        # Error if incomplete form
        except KeyError as e:
            print(f"KeyError: Missing fields for {str(e)}")
            return "Missing data", 400

    # Render the template
    return render_template('CreateAccount.html')


@app.route('/shop', methods=['GET'])
def shop():

    # Connect to db
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COMMODITYID, NAME, PRICE, QUANTITY FROM COMMODITY_STORE")
    data = cursor.fetchall()

    # Get query from search bar
    search_query = request.args.get('search', '') 


    if search_query:
        filtered_data = [row for row in data if search_query.lower().strip() in row[1].lower()]
    else:
        filtered_data = data
    return render_template('Search.html', data=filtered_data)



@app.route('/go_to_shop')
def go_to_shop():
    # This route will redirect the user to the shop page
    return redirect(url_for('shop'))


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        product_id = request.form['commodityID']
        product_name = request.form['product_name']
        product_price = float(request.form['price'])
        product_quantity = int(request.form['quantity'])

        cart = session.get('cart', [])
        
        product_in_cart = False
        for item in cart:
            if item['commodityID'] == product_id:
                item['quantity'] += product_quantity
                product_in_cart = True
                break
        
        if not product_in_cart:
            cart.append({
                'commodityID': product_id,
                'name': product_name,
                'price': product_price,
                'quantity': product_quantity
            })

        session['cart'] = cart
        session.modified = True

        return redirect(url_for('cart'))

    except KeyError as e:
        print(f"KeyError: Missing form data for {str(e)}")
        return "Missing data", 400
    

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():

    # Product to remove
    product_name = request.form['product_name']
    
    # Get the cart from the session
    cart = session.get('cart', [])

    # Remove item from cart if it exists
    cart = [item for item in cart if item['name'] != product_name]

    # Save
    session['cart'] = cart
    session.modified = True

    # Refresh page
    return redirect(url_for('cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():

    # Clear the cart
    session['cart'] = []

    # Refresh page
    return redirect(url_for('cart'))

@app.route('/cart', methods=['GET'])
def cart():
    
    cart = session.get('cart', [])
    return render_template('Cart.html', cart=cart)


@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO contactus (name, email, message) VALUES (:1, :2, :3)",
            (name, email, message)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return render_template('thankyou.html')
    
    return render_template('contactus.html')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', [])
    conn=connect_to_db()
    cursor=conn.cursor()
    if request.method == 'POST':
        # Collect form data
        name = request.form['name']
        address = request.form['address']
        card = request.form['card']

        # Process each item in the cart: reduce quantity
        for item in cart:
            commodity_id = item['commodityID']  # Make sure this exists in your cart structure
            quantity_ordered = item['quantity']

            try:
                cursor.execute("""
                    UPDATE commodity_store
                    SET quantity = quantity - :qty
                    WHERE commodityID = :cid
                """, {'qty': quantity_ordered, 'cid': commodity_id})
            except Exception as e:
                print(f"Error updating quantity for {commodity_id}: {e}")

        conn.commit()  # Commit the update so the trigger fires
        cursor.close()

        # Clear the cart
        session['cart'] = []
        session.modified = True

        # Render thank you page
        return render_template('thankyou.html', name=name)

    return render_template('checkout.html', cart=cart)


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    products = []
    categories = []
    brands = []
    dietary_options = []

    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch distinct filter options
    cursor.execute("SELECT DISTINCT category FROM commodity_store")
    categories = [row[0] for row in cursor.fetchall() if row[0]]

    cursor.execute("SELECT DISTINCT brand FROM commodity_store")
    brands = [row[0] for row in cursor.fetchall() if row[0]]

    cursor.execute("SELECT DISTINCT dietaryrestric FROM commodity_store")
    dietary_options = [row[0] for row in cursor.fetchall() if row[0]]

    if request.method == 'POST':
        # Retrieve user preferences
        pref_category = request.form.get('category')
        pref_brand = request.form.get('brand')
        pref_dietary = request.form.get('dietary')

        print(f"Category: {pref_category}, Brand: {pref_brand}, Dietary: {pref_dietary}")

        # Build dynamic query
        base_query = "SELECT name, price FROM commodity_store WHERE 1=1"
        params = {}

        if pref_category:
            base_query += " AND LOWER(category) = :category"
            params['category'] = pref_category.lower()
        if pref_brand:
            base_query += " AND LOWER(brand) = :brand"
            params['brand'] = pref_brand.lower()
        if pref_dietary:
            base_query += " AND LOWER(dietaryrestric) = :dietary"
            params['dietary'] = pref_dietary.lower()

        print(f"SQL Query: {base_query}, Parameters: {params}")

        cursor.execute(base_query, params)
        products = [{'name': name, 'price': price} for name, price in cursor.fetchall()]

    cursor.close()
    conn.close()

    return render_template(
        'recommendations.html',
        products=products,
        categories=categories,
        brands=brands,
        dietary_options=dietary_options
    )

@app.route('/review/<commodityName>', methods=['GET'])
def write_review(commodityName):
    product_sql = "SELECT commodityID, name FROM commodity_store WHERE name = :1"
    try:
        product_df = fetch_data(product_sql, [commodityName])
        if not product_df.empty:
            commodityID = product_df['COMMODITYID'].iloc[0]
            product_name = product_df['NAME'].iloc[0]
        else:
            product_error = "Product not found."
            return render_template('review.html', product_error=product_error)

    except oracledb.Error as e:
        error, = e.args
        print(f"Database error fetching product: {error.message}")
        product_error = "Error fetching product details."
        return render_template('review.html', product_error=product_error)

    # Fetch reviews using commodityID as usual
    reviews_sql = """
        SELECT a.username, r.rating, r.review, r.reviewDate
        FROM Review r
        JOIN Account a ON r.custID = a.email
        WHERE r.commodityID = :1
    """
    reviews = []
    try:
        reviews_df = fetch_data(reviews_sql, [commodityID])
        print("Fetched reviews:", reviews_df)
        reviews = reviews_df.to_records(index=False).tolist() if not reviews_df.empty else []
    except oracledb.Error as e:
        error, = e.args
        print(f"Database error fetching reviews: {error.message}")
        flash("Error fetching existing reviews.", "error")

    return render_template('review.html',
                           product=(commodityID, product_name),
                           reviews=reviews,
                           product_error=None)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    print("Submit Review Endpoint Hit")

    commodityName = request.form.get('commodityName')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    custID = request.form.get('custID') or 'testuser@example.com'  # dummy user for now

    print(f"Received data: commodityName={commodityName}, rating={rating}, comment={comment}")

    if not (commodityName and rating and comment):
        print("Review details are incomplete!")
        flash("Please fill out all fields.", "error")
        return redirect(url_for('write_review', commodityName=commodityName))

    try:
        rating = float(rating)
        print(f"Converted rating: {rating}")
    except ValueError:
        print("Invalid rating value!")
        flash("Invalid rating value.", "error")
        return redirect(url_for('write_review', commodityName=commodityName))

    # Fetch commodityID for the given commodityName
    product_sql = "SELECT commodityID FROM commodity_store WHERE name = :1"
    try:
        product_df = fetch_data(product_sql, [commodityName])
        if product_df.empty:
            print("Product not found.")
            flash("Product not found.", "error")
            return redirect(url_for('write_review', commodityName=commodityName))
        commodityID = product_df['COMMODITYID'].iloc[0]
        print(f"Found commodityID: {commodityID}")
    except oracledb.Error as e:
        error, = e.args
        print(f"Database error fetching commodityID: {error.message}")
        flash("Error fetching product details.", "error")
        return redirect(url_for('write_review', commodityName=commodityName))

    # Get the next reviewID manually
    get_max_id_sql = "SELECT NVL(MAX(reviewID), 0) FROM Review"
    try:
        max_id_df = fetch_data(get_max_id_sql)
        new_reviewID = int(max_id_df.iloc[0, 0]) + 1
        print(f"New reviewID: {new_reviewID}")
    except oracledb.Error as e:
        error, = e.args
        print(f"Database error getting max reviewID: {error.message}")
        flash("Error generating review ID.", "error")
        return redirect(url_for('write_review', commodityName=commodityName))

    # Insert the review
    insert_review_sql = """
        INSERT INTO Review (reviewID, commodityID, custID, rating, review, reviewDate)
        VALUES (:1, :2, :3, :4, :5, SYSDATE)
    """
    try:
        insert_data(insert_review_sql, [(new_reviewID, commodityID, custID, rating, comment)])
        print("Review submitted successfully.")
        flash("Review submitted successfully!", "success")
    except oracledb.Error as e:
        error, = e.args
        print(f"Database error submitting review: {error.message}")
        flash("Error submitting review.", "error")

    return redirect(url_for('write_review', commodityName=commodityName))


if __name__ == '__main__':
    app.run(debug=True)

