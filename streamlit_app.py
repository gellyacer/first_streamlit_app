import streamlit
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas 
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
    def get_fruityvice_data(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized
     #streamlit.dataframe(fruityvice_normalized)

except URLError as e:
    streamlit.error()
  
# streamlit.write('The user entered ', fruit_choice)

# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# streamlit.text(fruityvice_response) #just writes the data to the screen

# take the json version of the response and normalize it
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it in the screen as a table
# streamlit.dataframe(fruityvice_normalized)

# streamlit.stop()
# Display the table on the page.

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
#my_data_rows = my_cur.fetchall()
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")

streamlit.header("The fruit load list contains:")
#Snowflake-Related Actions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from_load_list")
         return my_cur.fetchall()

#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
       my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
       my_data_rows = get_fruit_load_list()
       streamlit.dataframe(my_data_rows)
      


# streamlit.dataframe(my_data_rows)
# streamlit.dataframe(fruits_to_show)

