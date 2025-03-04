# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Pending Orders")

cnx = st.connection("snowflake")
session = cnx.session()
pending_orders_df = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if pending_orders_df:
    editable_df = st.data_editor(pending_orders_df)
    submitted = st.button('Submit')
    
    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        
        try:
            og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.success("Order(s) Updated!", icon="✅")
        except:
            st.write("Something went wrong.")
else:
    st.success("There are no pending orders right now.", icon="✅")
