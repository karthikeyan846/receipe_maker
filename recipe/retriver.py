from qdrant_client import QdrantClient# qdrant client
from docling.chunking import HybridChunker# chunking
from docling.datamodel.base_models import InputFormat# doc converter
from docling.document_converter import DocumentConverter# doc converter
from llm import * # llm
import streamlit as st 
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class RecipeAssistant:
    def __init__(self):
        # Get configuration from environment variables
        self.url = os.getenv("QDRANT_URL")
        self.api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv("COLLECTION_NAME")
        
        # Initialize qdrant client
        self.client = QdrantClient(url=self.url, api_key=self.api_key)
        self.client.set_model("sentence-transformers/all-MiniLM-L6-v2")

    def retrieve(self, ingredients):
        # Create placeholders for status messages
        status = st.empty()
        status.info("🔍 Searching for recipes...")
        
        # Query the database
        points = self.client.query(
            collection_name=self.collection_name,
            query_text=f"available items: {ingredients}",
            limit=5,
        )

        status.info("📝 Analyzing ingredients...")
        
        # Combine all retrieved documents
        final_response = " "
        for point in points:
            final_response += point.document

        status.info("✨ Preparing your personalized recipe suggestions...")

        # Create prompt for the LLM
        prompt = f"""
        You are an expert recipe maker who helps users discover dishes based on their available ingredients.

        Context (Recipe Database):
        {final_response}

        Available Ingredients:
        {ingredients}

        Instructions:
        1. Analyze the provided ingredients and suggest dishes that can be made using them

        2. If no recipes match the available ingredients, clearly state that no matching recipes were found and suggest adding more ingredients to find suitable recipes. For example: "I couldn't find any dishes with your specified ingredients. Please try adding more ingredients to help me suggest some delicious recipes."
        
        3. For each suggested dish:
           - List the dish name
           - Provide detailed step-by-step recipe instructions
           - Include any relevant cooking tips or variations

        Output Format:
        Matching Dishes:
        - [Dish Name 1]
        - [Dish Name 2]
        ...

        Detailed Recipes:
        [Dish Name 1]:
        Step 1: ...
        Step 2: ...
        ...

        [Dish Name 2]:
        Step 1: ...
        Step 2: ...
        ...

        Please suggest as many suitable dishes as possible based on the available ingredients. If only one dish is possible, that's perfectly fine.
        """

        result = chat_completion(prompt, "openai/gpt-4o-mini")
        status.empty()
        return result

# Set page config
st.set_page_config(
    page_title="Recipe Assistant",
    page_icon="🥘",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
        color: black;
        caret-color: black;
    }
    .recipe-card {
        background-color: #ffffff;
        color: #000000;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .header-container {
        text-align: center;
        padding: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header-container">', unsafe_allow_html=True)
st.title("🥘 Recipe Assistant")
st.markdown("Your personal AI chef to help you discover recipes with available ingredients!")
st.markdown('</div>', unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    # Input section
    st.subheader("📝 Enter Your Ingredients")
    ingredients = st.text_input(
        "List your available ingredients (separated by commas)",
        placeholder="e.g., tomatoes, onions, potatoes, garlic"
    )
    
    if st.button("Find Recipes", type="primary"):
        if ingredients.strip():
            # Create RecipeAssistant instance
            assistant = RecipeAssistant()
            
            # Get recipe suggestions
            result = assistant.retrieve(ingredients)
            
            # Display results in a card
            st.markdown("---")
            st.subheader("🍳 Recipe Suggestions")
            with st.container():
                st.markdown(f"""
                <div class="recipe-card">
                    <h3>Recipes for: {ingredients}</h3>
                    {result}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Please enter some ingredients first!")

with col2:
    # Tips and information
    st.subheader("💡 Tips")
    st.markdown("""
    - List all available ingredients
    - Include spices and condiments
    - Be specific (e.g., "red onions" vs "onions")
    - Separate ingredients with commas
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ by Recipe Finder Team</p>", unsafe_allow_html=True)
