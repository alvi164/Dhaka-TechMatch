import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load Environment & Initialize OpenAI Client
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Fallback mechanism if env file isn't found
if not api_key:
    st.warning("⚠️ OPENAI_API_KEY not found in .env file. Please enter it below to run the app:")
    api_key = st.text_input("Enter OpenAI API Key:", type="password")

client = OpenAI(api_key=api_key) if api_key else None

# 2. App Configuration & Branding
st.set_page_config(page_title="LastCall Eats", page_icon="🥡", layout="wide")

st.title("🥡 LastCall Eats")
st.caption("AI-Powered Urban Surplus Food Marketplace — Reducing waste, feeding students.")
st.markdown("---")

# Initialize session state to store restaurant listings dynamically without a DB
if "listings" not in st.session_state:
    st.session_state.listings = [
        {
            "restaurant": "Campus Taqueria",
            "item": "Premium Burrito Batch (Surplus)",
            "description": "Freshly prepared artisanal burritos containing grilled proteins, black beans, and house-made salsa.",
            "original_price": 12.00,
            "discount_price": 3.60,
            "tags": ["Halal", "Dairy-Free"],
            "status": "Available"
        }
    ]

# 3. Create Navigation Tabs
tab1, tab2 = st.tabs(["🏪 Restaurant Portal", "🎓 Student Marketplace"])

# --- TAB 1: RESTAURANT PORTAL ---
with tab1:
    st.header("Manage End-of-Day Food Surplus")
    st.write("Type a rough note about what your kitchen has left over. Our AI will automatically format a beautiful, discounted listing.")
    
    restaurant_name = st.text_input("Restaurant Name", value="Diner 71")
    raw_input = st.text_area(
        "What is left over in the kitchen? (Be rough, e.g., 'got 5 bowls chicken rice left over closing at 10')",
        placeholder="e.g., 4 boxes of vegetarian pasta packs, need to clear in 45 mins"
    )
    
    base_price = st.number_input("Original Retail Price ($)", min_value=1.0, value=10.0, step=0.5)

    if st.button("✨ Generate AI Listing via OpenAI"):
        if not client:
            st.error("Please supply a valid OpenAI API Key first.")
        elif not raw_input:
            st.warning("Please type a quick kitchen description first.")
        else:
            with st.spinner("AI is analyzing ingredients and structuring menu profile..."):
                try:
                    # System instructions to drive the transformation logic
                    prompt = f"""
                    You are a backend menu parser for LastCall Eats. 
                    Take this raw, chaotic kitchen description: "{raw_input}"
                    
                    Generate a clean JSON payload exactly matching this structure:
                    {{
                        "item_title": "Attractive short item name",
                        "description": "Appetizing 1-sentence food description highlighting value and freshness",
                        "tags": ["Tag1", "Tag2"] (Choose relevant tags like Vegetarian, Vegan, Gluten-Free, Halal, Spicy, or Comfort Food)
                    }}
                    Provide ONLY raw JSON. No markdown wrappers, no backticks.
                    """
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini", # Highly cost-effective and fast model
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7
                    )
                    
                    import json
                    result = json.loads(response.choices[0].message.content.strip())
                    
                    # Calculate strict 70% discount math
                    discounted_value = round(base_price * 0.30, 2)
                    
                    # Store generated object in state
                    new_listing = {
                        "restaurant": restaurant_name,
                        "item": result["item_title"],
                        "description": result["description"],
                        "original_price": base_price,
                        "discount_price": discounted_value,
                        "tags": result["tags"],
                        "status": "Available"
                    }
                    st.session_state.listings.append(new_listing)
                    st.success("🎉 Listing processed successfully and pushed live to the marketplace!")
                    
                except Exception as e:
                    st.error(f"Error parsing AI generation: {e}")

# --- TAB 2: STUDENT MARKETPLACE ---
with tab2:
    st.header("Available LastCall Deals Near Campus")
    st.write("Grab premium meals at a **70% flat discount** before kitchens close down.")
    
    if not st.session_state.listings:
        st.info("No active surplus deals running right now. Check back closer to restaurant closing windows!")
    else:
        for idx, listing in enumerate(st.session_state.listings):
            # Create interactive card component structure
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{listing['item']} 🏷️ 70% OFF")
                    st.caption(f"Offered by: **{listing['restaurant']}**")
                    st.write(listing['description'])
                    
                    # Render styling tags
                    tags_html = " ".join([f"`{t}`" for t in listing['tags']])
                    st.markdown(f"**Dietary Details:** {tags_html}")
                    
                with col2:
                    st.markdown(f"~~Original: ${listing['original_price']:.2f}~~")
                    st.markdown(f"### 🔥 ${listing['discount_price']:.2f}")
                    
                    if listing['status'] == "Available":
                        if st.button(f"Reserve Box", key=f"btn_{idx}"):
                            listing['status'] = "Claimed 🎉"
                            st.rerun()
                    else:
                        st.button(f"Claimed ✅", disabled=True, key=f"btn_{idx}")
