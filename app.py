import streamlit as st
from sweetcrypt.core import GlycanCrypt
from PyPDF2 import PdfReader
from PIL import Image
import io

# ===============================
# 🍭 Streamlit UI
# ===============================
st.set_page_config(
    page_title="SweetCrypt Glycan Encryptor", 
    layout="centered",
    page_icon="🍬"
)
st.title("🍬 SweetCrypt - Glycan Encryption Tool")
st.markdown("""
    Encrypt your files or text using glycan-like secure symbolization.
    *Part of the 418 Hackathon hosted by Enigma under AEON 2025*
""")

# Session state initialization
st.session_state.setdefault("stage", "input")
st.session_state.setdefault("content", "")
st.session_state.setdefault("encrypted_data", None)
st.session_state.setdefault("crypto", None)

# -------------------------------
# Stage 1: Input Selection
# -------------------------------
if st.session_state.stage == "input":
    st.subheader("Choose input method")
    text_input = st.text_area("Paste text to encrypt", height=150)
    uploaded_file = st.file_uploader(
        "Or upload a file", 
        type=["txt", "pdf", "jpeg", "jpg", "png"],
        accept_multiple_files=False
    )

    if st.button("Encrypt"):
        if uploaded_file:
            try:
                if uploaded_file.type == "application/pdf":
                    reader = PdfReader(uploaded_file)
                    st.session_state.content = "\n".join(
                        page.extract_text() or "" 
                        for page in reader.pages
                    )
                elif uploaded_file.type.startswith("image/"):
                    image = Image.open(uploaded_file)
                    with io.BytesIO() as output:
                        image.save(output, format="PNG")
                        st.session_state.content = output.getvalue()
                else:  # Text files
                    st.session_state.content = uploaded_file.read().decode()
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
        elif text_input:
            st.session_state.content = text_input
        else:
            st.warning("Please provide text or a file!")
            st.stop()

        st.session_state.stage = "passphrase"
        st.experimental_rerun()

# -------------------------------
# Stage 2: Passphrase Entry
# -------------------------------
elif st.session_state.stage == "passphrase":
    st.info("🔐 Please type a passphrase to later retrieve and decrypt your data.")
    passphrase = st.text_input("Enter your passphrase", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit", disabled=not passphrase):
            crypto = GlycanCrypt(passphrase)
            encrypted = crypto.encrypt(st.session_state.content)
            st.session_state.encrypted_data = encrypted
            st.session_state.crypto = crypto
            st.session_state.stage = "result"
            st.experimental_rerun()
    with col2:
        if st.button("Back"):
            st.session_state.stage = "input"
            st.experimental_rerun()

# -------------------------------
# Stage 3: Results Display
# -------------------------------
elif st.session_state.stage == "result":
    st.subheader("🔒 Encrypted Output")
    encrypted = st.session_state.encrypted_data
    
    # Show first 5 glycan symbols
    st.code("\n".join(encrypted["symbols"][:5])
    st.caption(f"Generated {len(encrypted['symbols'])} glycan symbols")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Decrypt"):
            decrypted = st.session_state.crypto.decrypt(encrypted)
            st.subheader("🔓 Decrypted Content")
            if isinstance(decrypted, str):
                st.text_area("", value=decrypted, height=200)
            else:  # Binary data (e.g., images)
                st.image(io.BytesIO(decrypted))
    with col2:
        st.download_button(
            "Download Encrypted",
            data=str(encrypted),
            file_name="sweet_encrypted.scrypt",
            mime="text/plain"
        )
    with col3:
        if st.button("New Encryption"):
            st.session_state.stage = "input"
            st.experimental_rerun()

    # Technical details expander
    with st.expander("🔍 Technical Details"):
        st.json({
            "Algorithm": "AES-256-GCM",
            "Key Derivation": "scrypt (N=16384, r=8, p=1)",
            "Symbol Engine": "BLAKE2b + Base32",
            "IV": encrypted["iv"][:10] + "...",
            "Salt": encrypted["salt"][:10] + "..."
        })

# Footer
st.markdown("---")
st.caption("""
    🚀 Built for the 418 Hackathon (AEON 2025) | 
    [GitHub Repo](https://github.com/yourusername/sweetcrypt-glycan-encryptor)
""")
