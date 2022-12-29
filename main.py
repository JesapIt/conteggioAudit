import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import date
import datetime



scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']

creds = ServiceAccountCredentials.from_json_keyfile_name('key_conteggio.json', scope)
client = gspread.authorize(creds)



# --- Interfaccia ----
form = st.form('form1')
nome = form.text_input('Inserisci il tuo nome')
options = ['call', 'formazione', 'task', 'altro']
att = form.selectbox('Attività', options)
n_ore = form.time_input('Numero di ore', datetime.time(1, 0))
data = form.date_input('Data', value=date.today())

sub = form.form_submit_button("Submit")


sht = client.open_by_url("https://docs.google.com/spreadsheets/d/1f8zJ0iEwYia6sagTV11EDsDDgvwTm60SrdQvMhtJ3RI/edit#gid=0")
# -- Selecting current worksheet ---
if sub and nome != '':
	for w in sht.worksheets():
		lower_title = w.title.lower()
		lower_name = nome.lower()
		if lower_name in lower_title:
			current_work = w
	
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
