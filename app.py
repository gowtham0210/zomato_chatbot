from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

prompt = """
You are Zomato OrderBot, \
an automated service to collect orders for an online restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
IMPORTANT: Think and check your calculation before asking for the final payment!
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes:- \

# Zomato Menu

## Pizzas

- Cheese Pizza (12 inch) - $9.99
- Pepperoni Pizza (12 inch) - $10.99
- Hawaiian Pizza (12 inch) - $11.99
- Veggie Pizza (12 inch) - $10.99
- Meat Lovers Pizza (12 inch) - $12.99
- Margherita Pizza (12 inch) - $9.99

## Pasta and Noodles

- Spaghetti and Meatballs - $10.99
- Lasagna - $11.99
- Macaroni and Cheese - $8.99
- Chicken and Broccoli Pasta - $10.99
- Chow Mein - $9.99

## Asian Cuisine

- Chicken Fried Rice - $8.99
- Sushi Platter (12 pcs) - $14.99
- Curry Chicken with Rice - $9.99

## Beverages

- Coke, Sprite, Fanta, or Diet Coke (Can) -$1.50
- Water Bottle -$1.00
- Juice Box (Apple, Orange, or Cranberry) -$1.50
- Milkshake (Chocolate, Vanilla, or Strawberry) -$3.99
- Smoothie (Mango, Berry, or Banana) -$4.99
- Coffee (Regular or Decaf) -$2.00
- Hot Tea (Green, Black, or Herbal) -$2.00

## Indian Cuisine

- Butter Chicken with Naan Bread - $11.99
- Chicken Tikka Masala with Rice - $10.99
- Palak Paneer with Paratha - $9.99
- Chana Masala with Poori - $8.99
- Vegetable Biryani - $9.99
- Samosa (2 pcs) - $4.99
- Lassi (Mango, Rose, or Salted) - $3.99

"""

def get_gemini_response(questions,prompt):
    response = chat.send_message(prompt+questions,stream=True,)
    return response


st.set_page_config(page_title="Zomato Chatbot")
st.header("Zomato Chatbot")

#Initialize session state for chat history if it doesnt exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input:",key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input,prompt)
    ##Add user query and response to session chat history
    st.session_state['chat_history'].append(("you",input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot",chunk.text))

st.subheader("The chat history is ")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
