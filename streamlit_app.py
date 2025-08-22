# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())


st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)


name = st.text_input('Name On Smoothie:')
st.write('The name on your smoothie will be:', name)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose Upto 5 Ingredients:'
    , my_dataframe
    ,max_selections=5
)


if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name+"""')"""

    submit_button = st.button('Submit Order')
    if submit_button:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!, '+name+'!', icon="✅")
