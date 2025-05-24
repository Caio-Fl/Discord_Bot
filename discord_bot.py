# Bibliotecas Python utilizadas (pode ser necessário fazer a instalação de algumas delas "pip install biblioteca")
import streamlit as st
import plotly.express as px
import requests
import time
import json
import random
from random import randrange
from datetime import datetime, timezone
import pandas as pd
import io

image = "https://github.com/Caio-Fl/Discord_Bot/blob/master/disc.png?raw=true"
st.image(image,use_container_width=True)

st.subheader("Wellcome to Discord Bot 🤖 App")
st.write("")

aviso = """
<p style='text-align: justify; font-size: 16px;'>
Important: This is a Discord Bot App that will Send a List of Messages to a List of Discord Channels of the Discord Servers that you configure. 
This Bot will send each message to each channel in a random time range [minimum,maximum] that you configure. 
Be careful not to choose a time range that is too short, as there is a high chance that you will be identified as a Bot 
(I recommend using an interval of at least 10 - 60 minutes, but it will depend on the discord, as some are more strict than others). 
Use a reasonably sized message list (at least 10 different messages) and change them every day that you activate it. 
I also recommend checking at least once a day. If you are blocked on the server, an error may occur during execution. 👉 [Verify how to use here](https://x.com/CaioFlemin2089/status/1916149598847959457)
</p>
"""
st.markdown(aviso, unsafe_allow_html=True)
st.write("")

profile_url = "https://x.com/CaioFlemin2089"

# Função para salvar configurações
def salvar_configuracoes():
    df = pd.DataFrame({
        "Request_URLs": ['\n'.join(Request_URLs)],
        "Servers_Name": ['\n'.join(Servers_Name)],
        "Phrases": ['\n'.join(Phrases)],
        "Authorization": [Authorization],
        "min_time": [min_time],
        "max_time": [max_time],
        "lower_time": [lower_time],
        "higher_time": [higher_time],
    })
    return df

# Função para carregar configurações
def carregar_configuracoes(df):
    Request_URLs = df["Request_URLs"].iloc[0].splitlines()
    Servers_Name = df["Servers_Name"].iloc[0].splitlines()
    Phrases = df["Phrases"].iloc[0].splitlines()
    Authorization = df["Authorization"].iloc[0]
    min_time = int(df["min_time"].iloc[0])
    max_time = int(df["max_time"].iloc[0])
    # lower_time e higher_time, tratamento para NaN
    lower_time = int(df["lower_time"].iloc[0]) if not pd.isna(df["lower_time"].iloc[0]) else 0
    higher_time = int(df["higher_time"].iloc[0]) if not pd.isna(df["higher_time"].iloc[0]) else 0
    return Request_URLs, Servers_Name, Phrases, Authorization, min_time, max_time, lower_time, higher_time


# Criar uma variável de controle de acesso
if 'access_granted' not in st.session_state:
    st.session_state.access_granted = False

if not st.session_state.access_granted:
    if st.button('Liberate App'):
        # Redirecionar o usuário para o seu perfil
        st.markdown(
            "<p style='font-size:18px;'>Contribute to more content like this, "
            "<a href='https://x.com/CaioFlemin2089' target='_blank'>Follow on 𝕏</a></p>",
            unsafe_allow_html=True
        )
        st.session_state.access_granted = True        
        time.sleep(5)
        st.rerun() 
    
    #st.rerun()

# Liberar o app se o botão foi clicado
if st.session_state.access_granted:
    st.success("Thanks for Support")
    # Função para ler as mensagens do chat
    def retrieve_messages(Request_URL):
        res = requests.get(Request_URL, headers=headers)
        jsonn = json.loads(res.text)
        for value in jsonn:
            print(value['content'])

    st.subheader("⚙️ Bot Configuration")

    #Default Values
    Request_URLs = """""" 
    Servers_Name = """""" 
    Phrases = """"""  
    Authorization = "" 
    min_time = 1 
    max_time = 1 
    lower_time = 0 
    higher_time = 0

    # Upload para carregar configurações
    uploaded_file = st.file_uploader("Upload Configuration CSV", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        Request_URLs, Servers_Name, Phrases, Authorization, min_time, max_time, lower_time, higher_time = carregar_configuracoes(df)
        Request_URLs = '\n'.join(Request_URLs) + '\n'
        Servers_Name = '\n'.join(Servers_Name) + '\n'
        Phrases = '\n'.join(Phrases) + '\n'
        st.success("✅ Configuration Loaded Successfully!")
        # Você pode atualizar os campos no app ou só usar direto as variáveis carregadas

    user_input1 = st.text_area("Insert the Discord Chat URLs that you Desire to Send Messages (one by line):",
                               value = Request_URLs)
    # Separar em lista de strings
    Request_URLs = []
    if user_input1:
        Request_URLs = user_input1.splitlines()
        #st.write("Lista de Chats do Discord:")
        #st.write(Request_URLs)

    user_input2 = st.text_area("Insert the name o the Discord Channels (one by line):",
                               value = Servers_Name)

    # Separar em lista de strings
    if user_input2:
        Servers_Name = user_input2.splitlines()
        #st.write("Lista de Canais:")
        #st.write(Servers_Name)

    user_input3 = st.text_area("Insert the List of Messages to be Sent (one by line):",value = Phrases)

    # Separar em lista de strings
    if user_input3:
        Phrases = user_input3.splitlines()
        #st.write("Lista de Canais:")
        #st.write(Servers_Name)

    # Separar em lista de strings
    Authorization = st.text_input(
        "Insert the Authorization Code (Exclusive of your user, do not disclose it!):",
        value = Authorization,
        type = "password"
    )


    # Inicialização

    sending = False # Espera o comando do teclado para rodar o Bot

    # URL de cada chat no canal do discord
    #Request_URL = [
    #    f"https://discord.com/api/v9/channels/1361468674812280882/messages", #Linera
    #    f"https://discord.com/api/v9/channels/1361468674812280882/messages", # Sahara
    #    f"https://discord.com/api/v9/channels/1361468674812280882/messages", #Portal
    #    f"https://discord.com/api/v9/channels/1361468674812280882/messages", #IKA
    #    f"https://discord.com/api/v9/channels/1361468674812280882/messages", #AETHIR
    #    f"https://discord.com/api/v9/channels/1361468674812280882/messages" #Teste
    #]
    #Servers_Name = ["Linera","Sahara","Portal","IKA","Aethir","Teste"]

    # User Authorization (único para cada usuário e aplicável em totos os canais)
    headers = {
        "Authorization" : Authorization
    }

    # Envia Mensagens nos Canais(Request_URL) do Discord

    # Inicializa o estado se ainda não estiver definido
    if "loop_ativo" not in st.session_state:
        st.session_state.loop_ativo = False

    # Funções para iniciar e parar o loop
    def iniciar_loop():
        st.session_state.loop_ativo = True

    def parar_loop():
        st.session_state.loop_ativo = False

    # Botões para ativar e desativar o loop
    col1, col2 = st.columns(2)
    with col1:
        min_time = st.number_input(
        "Minimum time (in minutes) to Resend the List of Messages: ",
        min_value=1,
        max_value=1000000,
        value=min_time,   # valor padrão
        step=1
        )
    with col2:
        max_time = st.number_input(
        "Maximum time (in minutes) to Resend the List of Messages: ",
        min_value=1,
        max_value=1000000,
        value=max_time,   # valor padrão
        step=1
        )

    # Define Rest Time
    check = st.checkbox("Enable Rest Time Interval (Time interval where none Message will be sent)")

    # Use the checkbox value
    lower_time = 0
    higher_time = 6
    if check:
        col1, col2 = st.columns(2) 
        with col1:
            lower_time = st.number_input("Lower Rest Time (UTC) in hour (0-24h)",
            min_value=0,
            max_value=24,
            value=lower_time,   # valor padrão
            step=1
        )
        with col2:
            higher_time = st.number_input("Higher Rest Time (UTC) in hour (0-24h)",
            min_value=0,
            max_value=24,
            value=higher_time,   # valor padrão
            step=1
        )
        if lower_time >= higher_time:
            lower_time = higher_time
            higher_time = lower_time + 6
    
    # Botão para salvar configurações
    if st.button("💾 Save Configuration"):
        df = salvar_configuracoes()
        # Transformar listas em texto separado por quebras de linha
        for col in ["Request_URLs", "Servers_Name", "Phrases"]:
            if isinstance(df[col].iloc[0], list):
                df[col] = df[col].apply(lambda x: "\n".join(map(str, x)))
        # Agora exporta para CSV normalmente
        csv = df.to_csv(index=False).encode('utf-8')
        # Botão de download
        st.download_button(
            label="📥 Download Configuration CSV",
            data=csv,
            file_name='discord_bot_config.csv',
            mime='text/csv'
        )

    st.write("")
    st.subheader("▶️ Bot Activation")
    st.write("")

    # Botões para ativar e desativar o loop
    col1, col2 = st.columns(2)
    with col1:
        st.button("▶ Run Bot", on_click=iniciar_loop)
    with col2:
        st.button("🟧 Stop Bot", on_click=parar_loop)

    st.write("")
    st.subheader("🖥️ Log:")
    st.write("")

    # Cria um espaço vazio para o log
    log_area = st.empty()

    # Inicializa log se necessário
    if "log" not in st.session_state:
        st.session_state.log = ""
    payload = []
    # Loop de exemplo (mostrando números enquanto o loop estiver ativo)
    if st.session_state.loop_ativo:
        i = 0
        if len(Request_URLs)>0:
            while True:
                st.session_state.log = ""  # limpa o log antes de começar
                now_utc = datetime.now().now(timezone.utc)
                
                if lower_time <= now_utc.hour < higher_time:
                    nova_linha = f"Time to rest the bot until {higher_time} h UTC"
                    st.session_state.log += nova_linha
                    log_area.text(st.session_state.log)
                else:
                    for ph in range(len(Phrases)):
                        try: 
                            # Lista de Mensagens para Envio
                            for channel in range(len(Request_URLs)):                           
                                payload = {"content" : Phrases[ph]}
                                # Posta Mensagem
                                res = requests.post(Request_URLs[channel], payload, headers=headers)
                                nova_linha = f"Message - {payload["content"]} - Sended to {Servers_Name[channel]} Discord Channel\n"
                                st.session_state.log += nova_linha
                                log_area.text(st.session_state.log)
                                time.sleep(5 + 15*random.randint(0, 1))
                        except:
                            st.session_state.log = ""
                            nova_linha = f"⚠️ Was Not Possible to Send the Message to the Discord Channel. Please Verify your Connection or if you was Blocked in the Channel!"
                            st.session_state.log += nova_linha
                            log_area.text(st.session_state.log)
                        send_time = 60*random.randint(min_time, max_time) # envio aleatório na faixa de tempo especificados em min_time e max_time
                        nova_linha = f"\nSending Next Message in " + str(send_time/60) + " min\n"
                        st.session_state.log += nova_linha
                        log_area.text(st.session_state.log)
                        i += 1
                        if i == len(Phrases):
                            i = 0
                            nova_linha = f"\nResending List of Messages\n"
                            st.session_state.log += nova_linha
                            log_area.text(st.session_state.log)
                        time.sleep(send_time)
        else:
            st.session_state.log = ""  # limpa o log antes de começar
            nova_linha = f"⚠️ No Channel or Message Configured!"
            st.session_state.log += nova_linha
            log_area.text(st.session_state.log)
else:
    st.write("")


