
import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="TraceMate",
    page_icon="🧠",
    layout="centered",
)

st.title("🧠 TraceMate")
st.caption("Your Java DSA learning assistant")

st.markdown(
    "Learn data structures and algorithms through explanations, "
    "hints, and code analysis."
)

# Learning mode selection
mode_options = {
    "Explain a concept": "explain",
    "Progressive hints": "hint",
    "Analyze Java code": "analyze",
    "Generate edge cases": "edge_cases",
}

selected_mode = st.selectbox(
    "Choose your learning mode",
    options=list(mode_options.keys()),
)

mode = mode_options[selected_mode]

# Question input
question = st.text_area(
    "Your question",
    placeholder="Example: Explain how binary search works in Java.",
    height=100,
)

# Show Java code input only when required
code = ""

if mode in ["analyze", "edge_cases"]:
    code = st.text_area(
        "Your Java code",
        placeholder="Paste your Java code here...",
        height=220,
    )

# Hint level selection
hint_level = 1

if mode == "hint":
    hint_level = st.slider(
        "Hint level",
        min_value=1,
        max_value=5,
        value=1,
        help="Level 1 gives a subtle hint. Level 5 gives a more direct hint.",
    )

# Submit
if st.button("Ask TraceMate", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")

    elif mode in ["analyze", "edge_cases"] and not code.strip():
        st.warning("Please provide your Java code.")

    else:
        payload = {
            "question": question,
            "mode": mode,
            "code": code,
            "hint_level": hint_level,
        }

        with st.spinner("TraceMate is thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json=payload,
                    timeout=120,
                )

                response.raise_for_status()
                result = response.json()

                st.divider()
                st.subheader("TraceMate's response")
                st.markdown(result["answer"])

                st.divider()
                st.subheader("Knowledge sources")

                if result["sources"]:
                    for source in result["sources"]:
                        st.write(f"- `{source}`")
                else:
                    st.write("No relevant sources retrieved.")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to the backend. "
                    "Make sure FastAPI is running."
                )

            except requests.exceptions.Timeout:
                st.error("The request timed out. Please try again.")

            except requests.exceptions.HTTPError:
                st.error(f"API error: {response.text}")

            except Exception as error:
                st.error(f"Unexpected error: {error}")
