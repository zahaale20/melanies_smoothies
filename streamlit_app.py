# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    f"""Choose the fruits you want in your custom Smoothie!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select("fruit_name")
#st dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on Smoothie", "")
st.write("The name on your Smoothie will be:", name_on_order)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    #st.write(ingredients_list)SMOOTHIES.PUBLIC.FRUIT_OPTIONS
    #st.text(ingredients_list)
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        my_insert_stmt = f"INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_filled) VALUES ('{ingredients_string}', '{name_on_order}', false)"
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, {}!'.format(name_on_order), icon="✅")
