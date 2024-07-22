from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

@login_required(login_url = '/auth/login')
def faturamento(request):
    if request.method == "GET":

        # Read sqlite query results into a pandas DataFrame
        con = sqlite3.connect("db.sqlite3")
        df = pd.read_sql_query("SELECT * from financeiro_financeiro", con)
        df["data_pagamento"] = pd.to_datetime(df["data_pagamento"])
        df.sort_values(by="data_pagamento")

        df["Month"] = df["data_pagamento"].apply(lambda x: str(x.year) + "-" + str(x.month))
        print(df["Month"])
        #print(df["data_pagamento"])

        month = st.sidebar.selectbox("Mês", df["Month"].unique())
        # Verify that result of SQL query is stored in the dataframe
        #print(df.head())
        con.close()

        return render(request, 'faturamento.html')
    elif request == "POST":
        pass