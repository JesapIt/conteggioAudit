import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import date
import datetime

st.set_page_config(page_title='Conteggio Ore', page_icon = '🕰️', initial_sidebar_state = 'auto')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']

creds = ServiceAccountCredentials.from_json_keyfile_name('key_conteggio.json', scope)
client = gspread.authorize(creds)


st.markdown('## [Link al foglio google di test ](https://docs.google.com/spreadsheets/d/1f8zJ0iEwYia6sagTV11EDsDDgvwTm60SrdQvMhtJ3RI/edit?usp=sharing)')

st.markdown('> Il campo nome non richiede una corrispondenza esatta e non è case sensitive, tuttavia, nel caso di più risorse con lo stesso nome, è bene inserire e/o parti del congome')
st.markdown('> ES: Per accedere al foglio Michele Vitulli, posso inserire mic, MIchele, MICHELE etc; se venissero trovate più corrispondenze <omonimi> il sistema genererà una notifica; (Per essere sicuro di accecere al mio foglio posso inserire semplicemente vit)')
# --- Interfaccia ----
form = st.form('form1')
nome = form.text_input('Nome')
options = ['call', 'formazione', 'task', 'altro']
att = form.selectbox('Attività', options)
n_ore = form.time_input('Numero di ore', datetime.time(1, 0))
data = form.date_input('Data', value=date.today())

sub = form.form_submit_button("Invia")


sht = client.open_by_url("https://docs.google.com/spreadsheets/d/1f8zJ0iEwYia6sagTV11EDsDDgvwTm60SrdQvMhtJ3RI/edit#gid=0")
# -- Selecting current worksheet ---
if sub and nome != '':
	double = 0
	for w in sht.worksheets():
		lower_title = w.title.lower()
		lower_name = nome.lower()
		if lower_name in lower_title:
			double +=1
			current_work = w
	if double > 1:
		st.warning('Sono stati trovati più fogli con questo nome, cerca di essre più specifico')
	else:
	# --- adding elements to google sheet ---
		def next_available_row(worksheet):
			str_list = list(filter(None, worksheet.col_values(1)))
			return str(len(str_list)+1)

		row = next_available_row(current_work)
		current_work.update_cell(row , 1, str(data))
		current_work.update_cell(row , 2, att)
		current_work.update_cell(row , 3, str(n_ore).replace(':', '.'))


		st.success('Conteggio ore aggiornato')
	

# --- trovo la colonna libera successiva ---
