# Import python packages
import streamlit as st
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

from snowflake.snowpark.functions import col
cnx = st.connection("snowflake")
session = cnx.session()

smoothiesfroot_response = requests.get("https://www.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiesfroot_response.json(), use_container_width=True)

name_on_order = st.text_input("Name on Smoothie")

my_dataframe = session.table("smoothies.public.fruit_options").select("FRUIT_NAME")
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe, max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')

    if ingredients_string and time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
