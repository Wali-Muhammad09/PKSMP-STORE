import streamlit as st
import random
import yagmail
import uuid

# ---------------- CONFIG ----------------
SENDER_EMAIL = "pksmprankmanager@gmail.com"
SENDER_PASSWORD = "wpoz fdpf nuko aczp"
OWNER_EMAIL = "pksmpminecraft@gmail.com"

st.set_page_config(page_title="PKSMP Store", page_icon="🔥")

# ---------------- SESSION ----------------
if "user_uuid" not in st.session_state:
    st.session_state.user_uuid = str(uuid.uuid4())

# ---------------- CSS ----------------
st.markdown("""
<style>

body{
background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}

.title{
text-align:center;
font-size:48px;
color:#00ffcc;
font-weight:bold;
}

.subtitle{
text-align:center;
color:#ccc;
}

/* CARDS */
.rank-card,.crate-card{
background:#111;
padding:22px;
border-radius:18px;
margin-top:25px;
}

.rank-name,.crate-name{
font-size:28px;
font-weight:bold;
}

.price,.crate-price{
font-size:22px;
margin-top:10px;
}

.perks{
color:#ddd;
line-height:1.6;
}

/* RANK GLOWS */
.pro{box-shadow:0 0 12px hotpink;color:hotpink;}
.vip{box-shadow:0 0 12px #fff7a0;color:#fff7a0;}
.deadliest{box-shadow:0 0 12px #6fb8ff;color:#6fb8ff;}
.god{box-shadow:0 0 12px gold;color:gold;}
.hero{box-shadow:0 0 12px #66ff99;color:#66ff99;}
.devil{box-shadow:0 0 12px #ff4c4c;color:#ff4c4c;}

/* CRATE GLOWS */
.common{box-shadow:0 0 12px #ddd;color:#ddd;}
.rare{box-shadow:0 0 12px #6fdcff;color:#6fdcff;}
.epic{box-shadow:0 0 12px #d28cff;color:#d28cff;}
.legendary{box-shadow:0 0 12px gold;color:gold;}
.mythic{box-shadow:0 0 12px #ff7ac8;color:#ff7ac8;}

</style>
""", unsafe_allow_html=True)

# ---------------- CLASSES ----------------
class Rank:
    def __init__(self,name,price,perks):
        self.name=name
        self.price=price
        self.perks=perks

class Crate:
    def __init__(self,name,price):
        self.name=name
        self.price=price

# ---------------- DATA ----------------
ranks = [
    Rank("PRO", "1 USDT",
         "Iron Armor Kit (24h)\n"
         "1 Golden Apple\n"
         "Food\n"
         "/kit PRO"),

    Rank("VIP", "2 USDT",
         "Iron Armor Kit (Unbreaking 1, Protection 1)\n"
         "6 Golden Apples\n"
         "Food\n"
         "/kit VIP"),

    Rank("Deadliest", "3 USDT",
         "Diamond Armor Kit (24h)\n"
         "8 Golden Apples\n"
         "Food\n"
         "/echest\n"
         "/kit Deadliest"),

    Rank("God", "4 USDT",
         "Diamond Armor Kit (Unbreaking 1, Protection 2)\n"
         "16 Golden Apples\n"
         "/echest\n"
         "/craft\n"
         "/kit God"),

    Rank("Hero", "5 USDT",
         "Diamond Armor Kit (Unbreaking 2, Protection 2) every 24h\n"
         "20 Golden Apples\n"
         "Food\n"
         "/echest\n"
         "/craft\n"
         "/anvil\n"
         "/kit Hero"),

    Rank("Devil", "6 USDT",
         "Diamond Armor Kit (Unbreaking 3, Protection 3) every 24h\n"
         "32 Golden Apples\n"
         "Food\n"
         "/echest\n"
         "/craft\n"
         "/anvil\n"
         "Access to /fix\n"
         "Permission to /nick\n"
         "/kit Devil")
]


crates=[
Crate("Common","0.5 USDT"),
Crate("Rare","1 USDT"),
Crate("Epic","2 USDT"),
Crate("Legendary","3 USDT"),
Crate("Mythic","4 USDT")
]

# ---------------- HEADER ----------------
st.markdown("<div class='title'>🔥 PKSMP STORE 🔥</div>",unsafe_allow_html=True)
store=st.selectbox("Choose Category",["Ranks","Crate Keys"])

# ---------------- EMAIL PURCHASE SYSTEM ----------------
def purchase(item):

    if "show_form" not in st.session_state:
        st.session_state.show_form=False

    if st.button("Buy Now"):
        st.session_state.show_form=True

    if st.session_state.show_form:

        st.markdown("### 📝 Purchase Info")

        discord=st.text_input("Discord Username")
        gmail=st.text_input("Gmail Address")

        if "verified" not in st.session_state:
            st.session_state.verified=False
        if "code" not in st.session_state:
            st.session_state.code=None

        if not st.session_state.verified and gmail:
            if st.button("Send Verification Code"):
                try:
                    st.session_state.code=str(random.randint(100000,999999))
                    yag=yagmail.SMTP(SENDER_EMAIL,SENDER_PASSWORD)
                    yag.send(gmail,"PKSMP Verification",
                    f"Your code is: {st.session_state.code}")
                    st.success("Code sent!")
                except :
                    st.error("Verification could not be sent. Please re-check your email")
            if st.session_state.code and not st.session_state.verified:
                entered=st.text_input("Enter Code")
                if st.button("Verify"):
                    if entered==st.session_state.code:
                        st.session_state.verified=True
                        st.success("Verified!")
                    else:
                        st.error("Wrong code")

            if st.session_state.verified:
                desc=st.text_area("Description (Optional)")
                if st.button("Submit Purchase"):
                    yag=yagmail.SMTP(SENDER_EMAIL,SENDER_PASSWORD)

                    yag.send(gmail,"PKSMP Purchase",
                    f"You ordered: {item}\nJoin discord: http://dsc.gg/pksmp")

                    yag.send(OWNER_EMAIL,"New Order",
                    f"Item: {item}\nDiscord:{discord}\nEmail:{gmail}\nDesc:{desc}")

                    st.success("Request sent!")
                    st.session_state.show_form=False
                    st.session_state.verified=False
                    st.session_state.code=None

# ---------------- RANK STORE ----------------
if store=="Ranks":

    choice=st.selectbox("Select Rank",[r.name for r in ranks])

    for r in ranks:
        if r.name==choice:
            st.markdown(f"""
            <div class="rank-card {choice.lower()}">
            <div class="rank-name">{r.name}</div>
            <div class="price">{r.price}</div>
            <div class="perks">{"<br>".join(r.perks.splitlines())}</div>
            </div>
            """,unsafe_allow_html=True)

            purchase(choice)

# ---------------- CRATE STORE ----------------
if store=="Crate Keys":

    crate_choice=st.selectbox("Select Crate",[c.name for c in crates])

    for c in crates:
        if c.name==crate_choice:
            st.markdown(f"""
            <div class="crate-card {c.name.lower()}">
            <div class="crate-name">{c.name} Crate Key</div>
            <div class="crate-price">{c.price}</div>
            </div>
            """,unsafe_allow_html=True)

            purchase(c.name+" Crate Key")
