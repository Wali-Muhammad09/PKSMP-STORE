import streamlit as st
import random
import yagmail
import uuid

# Initialize a unique UUID for the entire session
if 'user_uuid' not in st.session_state:
    st.session_state.user_uuid = str(uuid.uuid4())

# Assign to a variable for easy use
user_id = st.session_state.user_uuid

# Optional: display it for debugging
st.write("Your session UUID:", user_id)


SENDER_EMAIL = "pksmprankmanager@gmail.com"
SENDER_PASSWORD = "wpoz fdpf nuko aczp"
OWNER_EMAIL = "pksmpminecraft@gmail.com"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="PKSMP Store",
    page_icon="🔥",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #00ffcc;
}

.subtitle {
    text-align: center;
    color: #cccccc;
    margin-bottom: 30px;
}

.rank-card {
    background: #111;
    padding: 22px;
    border-radius: 18px;
    margin-top: 25px;
}

.rank-name {
    font-size: 28px;
    font-weight: bold;
}

.price {
    font-size: 22px;
    margin-top: 10px;
}

.perks {
    margin-top: 10px;
    color: #ddd;
    line-height: 1.6;
}

/* PRO - Pink */
.pro {
    box-shadow: 0 0 12px rgba(255,105,180,0.7),
                0 0 30px rgba(255,105,180,0.4);
    color: hotpink;
}

/* VIP - Light Yellow */
.vip {
    box-shadow: 0 0 12px rgba(255,255,150,0.7),
                0 0 30px rgba(255,255,150,0.4);
    color: #fff7a0;
}

/* Deadliest - Blue */
.deadliest {
    box-shadow: 0 0 12px rgba(0,150,255,0.7),
                0 0 30px rgba(0,150,255,0.4);
    color: #6fb8ff;
}

/* GOD - Gold */
.god {
    box-shadow: 0 0 12px rgba(255,200,0,0.8),
                0 0 30px rgba(255,200,0,0.5);
    color: gold;
}

/* HERO - Lime */
.hero {
    box-shadow: 0 0 12px rgba(0,255,100,0.7),
                0 0 30px rgba(0,255,100,0.4);
    color: #66ff99;
}

/* DEVIL - Dark Red */
.devil {
    box-shadow: 0 0 12px rgba(180,0,0,0.8),
                0 0 30px rgba(180,0,0,0.5);
    color: #ff4c4c;
}
.payment-note {
    font-size: 13px;
    color: #aaaaaa;
    margin-top: 8px;
    text-align: left;
    font-style: italic;
}

</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
class Rank:
    def __init__(self, name, price, perks):
        self.name = name
        self.price = price
        self.perks = perks

ranks = [
    Rank("PRO", "Rs.200",
         "Iron Armor Kit (24h)\n"
         "1 Golden Apple\n"
         "Food\n"
         "/kit PRO"),

    Rank("VIP", "Rs.350",
         "Iron Armor Kit (Unbreaking 1, Protection 1)\n"
         "6 Golden Apples\n"
         "Food\n"
         "/kit VIP"),

    Rank("Deadliest", "Rs.650",
         "Diamond Armor Kit (24h)\n"
         "8 Golden Apples\n"
         "Food\n"
         "/echest\n"
         "/kit Deadliest"),

    Rank("God", "Rs.850",
         "Diamond Armor Kit (Unbreaking 1, Protection 2)\n"
         "16 Golden Apples\n"
         "/echest\n"
         "/craft\n"
         "/kit God"),

    Rank("Hero", "Rs.1000",
         "Diamond Armor Kit (Unbreaking 2, Protection 2) every 24h\n"
         "20 Golden Apples\n"
         "Food\n"
         "/echest\n"
         "/craft\n"
         "/anvil\n"
         "/kit Hero"),

    Rank("Devil", "Rs.1300",
         "Diamond Armor Kit (Unbreaking 3, Protection 3) every 24h\n"
         "32 Golden Apples\n"
         "Food\n"
         "/echest\n"
         "/craft\n"
         "/anvil\n"
         "Access to /fix (This fixes the durability of all the items in your inventory)\n"
         "Permission to /nick\n"
         "/kit Devil")
]

# ---------------- HEADER ----------------
st.markdown('<div class="title">🔥 PKSMP STORE 🔥</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Choose a Rank and view its perks</div>', unsafe_allow_html=True)

# ---------------- SELECT ----------------
choice = st.selectbox("Select a Rank", [r.name for r in ranks])
#
# ---------------- DISPLAY CARD ----------------
for r in ranks:
    if r.name == choice:
        glow_class = choice.lower()

        st.markdown(f"""
        <div class="rank-card {glow_class}">
            <div class="rank-name">{r.name}</div>
            <div class="price">💰 {r.price}</div>
            <div class="perks">
                ⭐ Perks:<br>
                {"<br>".join(r.perks.splitlines())}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Buy Now"):
            st.session_state.show_form = True

        if "show_form" not in st.session_state:
            st.session_state.show_form = False

        # ---------------- PURCHASE FORM ----------------
        if st.session_state.show_form:

            st.markdown("### 📝 Purchase Information")

            discord = st.text_input("Discord Username")
            gmail = st.text_input("Gmail Address")

            # Initialize session state for verification
            if "verified_email" not in st.session_state:
                st.session_state.verified_email = False
            if "verification_code" not in st.session_state:
                st.session_state.verification_code = None

            # Step 1: Send verification code
            if not st.session_state.verified_email and gmail:
                if st.button("Send Verification Code"):
                    st.session_state.verification_code = str(random.randint(100000, 999999))
                    try:
                        yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)
                        yag.send(
                            gmail,
                            "PKSMP Store - Email Verification",
                            f"Your verification code is: {st.session_state.verification_code}"
                        )
                        st.success("✅ Verification code sent to your email!")
                    except:
                        st.error("❌ Failed to send verification code. Check your email.")

            # Step 2: Verify the code
            if st.session_state.verification_code and not st.session_state.verified_email:
                code_input = st.text_input("Enter Verification Code")
                if st.button("Verify Email"):
                    if code_input == st.session_state.verification_code:
                        st.session_state.verified_email = True
                        st.success("✅ Email verified!")
                    else:
                        st.error("❌ Incorrect code. Try again.")

            # Step 3: Only allow purchase submission if verified
            if st.session_state.verified_email:
                description = st.text_area("Description (Optional)", key=f"{user_id}_description")
                if st.button("Submit Purchase Request"):
                    if discord and gmail:
                        try:
                            yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)

                            # Email to Buyer
                            buyer_subject = "PKSMP Store - Purchase Instructions"
                            buyer_body = f"""
            Hello!

            Thanks for your interest in purchasing the {choice} rank.

            Please create a ticket in our Discord server:
            http://dsc.gg/pksmp

            Our staff will assist you further.

            PKSMP Store Team
            """
                            yag.send(gmail, buyer_subject, buyer_body)

                            # Email to Owner
                            owner_subject = "New PKSMP Purchase Request"
                            owner_body = f"""
            New Purchase Request:

            Rank: {choice}
            Discord: {discord}
            Gmail: {gmail}
            Description: {description}
            """
                            yag.send(OWNER_EMAIL, owner_subject, owner_body)

                            st.success("✅ Request submitted! Check your email.")
                            st.session_state.show_form = False
                            st.session_state.verified_email = False
                            st.session_state.verification_code = None

                        except:
                            st.error("❌ Email sending failed. Check credentials.")
                    else:
                        st.error("❌ Discord Username and Gmail are required.")

