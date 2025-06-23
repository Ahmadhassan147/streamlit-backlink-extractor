import streamlit as st
import requests
from bs4 import BeautifulSoup

# Define the function to extract backlink words
def extract_backlink_words_from_elementor_content(blog_url):

    backlink_words = []
    try:

        st.info(f"Attempting to fetch content from: {blog_url}...")
        
        response = requests.get(blog_url, timeout=10) # Added timeout for robustness
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        html_content = response.text
        # st.success("Successfully fetched HTML content.")

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all containers with the specific Elementor class
        content_containers = soup.find_all(class_='elementor-widget-theme-post-content')

        if not content_containers:
            st.warning("No element with class 'elementor-widget-theme-post-content' found on the page.")
            return []
        else:
            pass

        # Iterate through containers and find links
        for i, container in enumerate(content_containers):
            if len(content_containers) > 1:
                st.write(f"--- Processing Container {i+1} ---")
            
            for link in container.find_all('a', href=True):
                anchor_text = link.get_text(strip=True)
                if anchor_text:  # Only add if anchor text is not empty
                    backlink_words.append(anchor_text)

    except requests.exceptions.Timeout:
        st.error("Error: The request timed out. The server took too long to respond.")
        st.error("Please check the URL or your internet connection speed.")
    except requests.exceptions.ConnectionError:
        st.error("Error: Could not connect to the URL. Please check your internet connection.")
    except requests.exceptions.HTTPError as e:
        st.error(f"Error fetching the URL: HTTP {e.response.status_code} - {e.response.reason}")
        st.error("This usually means the URL is invalid or the server is not responding correctly.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred during the request: {e}")
        st.error("Please check the URL or your internet connection.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.error("This might be due to an issue with parsing the page content or an invalid URL structure.")

    return backlink_words

# --- Streamlit App Interface ---

st.set_page_config(
    page_title="Elementor Backlink Extractor",
    page_icon="🔗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🔗 Elementor Backlink Word Extractor")
st.markdown("Enter the URL of an Elementor-based blog post to extract the anchor texts of its internal/external links.")

# Input for the blog URL
blog_link = st.text_input("Enter the URL of the blog post:", placeholder="e.g., https://example.com/blog-post")

# Button to trigger the extraction
if st.button("Extract Backlink Words"):
    if blog_link:
        # Show a spinner while processing
        with st.spinner("Extracting backlinks... This might take a moment."):
            words = extract_backlink_words_from_elementor_content(blog_link)

        st.markdown("---") # Separator

        if words:
            st.success("SUCCESS: Backlinks Found!")
            st.metric(label="Total Backlinks Found", value=len(words))
            st.subheader("List of Backlink Texts:")
            # Use st.markdown with an unordered list for better presentation
            for i, word in enumerate(words):
                st.markdown(f"- **{word}**") # Bold the words for emphasis
            st.markdown("---")
            st.success("Extraction Complete.")
        else:
            st.error("STATUS: No Backlinks Found or an Error Occurred.")
            st.info("Please review the messages above for details.")
            st.info("Ensure the URL is correct and the blog post uses the 'elementor-widget-theme-post-content' class for its main content.")
            st.markdown("---")
    else:
        st.warning("Please enter a URL to proceed.")

# Footer
st.markdown("---") # Separator
st.markdown("Made by **Ahmad Hassan** from Strouse House.")
