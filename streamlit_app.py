import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from io import StringIO

"""
# Poc!
"""


def upload_file():
    uploaded_file = st.file_uploader("Envoyer votre facture du comptoir")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)


upload_file()

"**Les prix negocies avec le client**"

prix_ref = pd.read_csv("./prix_negocie.csv")
st.dataframe(prix_ref)

"**Les prix achetes au comptoir**"

prix_comptoir = pd.read_csv('./prix_comptoir.csv')
st.dataframe(prix_comptoir)

# AgGrid(prix_comptoir, editable=True)

"**Differences de prix**"

list_produit_comptoir = prix_comptoir["Produit"].tolist()
list_produit_ref = prix_ref["Produit"].tolist()

selection = list(set(list_produit_comptoir) & set(list_produit_ref))

prix_comptoir_filtered = prix_comptoir[prix_comptoir['Produit'].isin(selection)]
prix_ref_filtered = prix_ref[prix_ref['Produit'].isin(selection)]

d = []
for i in selection:
    prix_reference = prix_ref_filtered.set_index("Produit").loc[i][0]
    prix_comptoir = prix_comptoir_filtered.set_index("Produit").loc[i][0]
    if prix_reference != prix_comptoir:
        d.append({'produit': i, "negocie": prix_reference, "comptoir": prix_comptoir})

st.dataframe(pd.DataFrame(d))
