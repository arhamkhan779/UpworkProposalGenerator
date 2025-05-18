import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

api_key = st.secrets["GEMINI_API_KEY"]

# Initialize model
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)

# Prompt Template
prompt = PromptTemplate(
    input_variables=["JobDescription", "ProfileDescription"],
    template="""
You are a helpful and professional AI assistant. Your task is to write **Upwork proposals** that are tailored, persuasive, and job-specific.

### Instructions:
- Do **not** include unnecessary phrases like “Here is the proposal,” “I can write a proposal,” or anything similar.
- Only return the **final proposal content**—structured and ready to be sent to a client.

### Strategy — Use AIDA Framework:
1. **Attention**: Address the client's key need in the first sentence.
2. **Interest**: Highlight your relevant skills, experience, or services.
3. **Desire**: Show how you will solve their problem and add value.
4. **Action**: End with a strong call to action.

### Writing Style:
- Professional yet human tone.
- Concise, formal, and clean format.

### Job Description:
{JobDescription}

### Profile Description:
{ProfileDescription}

Now, generate a compelling, customized Upwork proposal.
"""
)

# Set Page Config
st.set_page_config(page_title="💼 AI Proposal Writer", layout="wide")

# Header
st.markdown(
    """
    <div style='text-align: center; padding: 10px 0 30px 0;'>
        <h1 style='color:#2563EB;'>💼 AI Upwork Proposal Generator</h1>
        <p style='font-size:18px;'>Craft tailored, job-specific proposals using the AIDA framework ⚡</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Two-column layout
left_col, right_col = st.columns([1.2, 1])

# Left: Inputs
with left_col:
    st.markdown("### ✍️ Enter Your Details")
    job_description = st.text_area("📄 Job Description", height=220, placeholder="Paste the client's job description here...")
    st.markdown("___")  # Separator line
    profile_summary = st.text_area("👤 Profile Summary", height=180, placeholder="Paste your Upwork profile summary here...")
    generate = st.button("🚀 Generate Proposal")

# Right: Output
with right_col:
    st.markdown("### 📬 Proposal Output")
    if generate:
        if job_description.strip() == "" or profile_summary.strip() == "":
            st.warning("⚠️ Please fill in both the Job Description and Profile Summary.")
        else:
            with st.spinner("✍️ Writing your proposal..."):
                try:
                    formatted_prompt = prompt.format(
                        JobDescription=job_description,
                        ProfileDescription=profile_summary
                    )
                    response = model.invoke(formatted_prompt)
                    st.success("✅ Proposal generated successfully!")
                    st.markdown(
                        f"""
                        <div style='background-color: #ecfdf5; padding: 20px; border-radius: 10px; border: 1px solid #a7f3d0; margin-top: 10px;'>
                            <pre style='white-space: pre-wrap; font-size: 16px; color: #065f46;'>{response.content}</pre>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")
