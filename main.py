from flet import *
import pandas as pd
import nltk

# INSTALL SKLEARN IN YOU PC WITH PIP AND INSTALL nltk 
# INSTALL ALL PACKAGE 
# BECAUSE I NOT PRACTICAL
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

# AND INSTALL WIKIPEDIA WITH PIP
import wikipedia


# AND LOAD data.csv 
data = pd.read_csv("data.csv")
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data["Gejala"])

clf = MultinomialNB()
clf.fit(X,data["Penyakit (ID)"])




def main(page:Page):
	page.scroll ="auto"
	youInput = TextField(label="state you symtomps in Indonesia Lang")
	resultDiagnose = Text(weight="bold",size=30)

	explanation = Text()

	def diagnosenow(e):
		symptoms_are_felt = vectorizer.transform([youInput.value])
		suitable_disease = clf.predict(symptoms_are_felt)
		if len(suitable_disease) == 0:
			print("sorry, diagnosis is wrong")
		else:

			# AND SHOW CONTAINER DIAGNOZING
			diagnoseCon.visible = True
			page.update()
			disease_indonesia = ", ".join(suitable_disease)
			disease_english = data[data["Penyakit (ID)"].isin(suitable_disease)][["Penyakit (ID)","Penyakit (EN)"]]	
			disease_english.columns = ["Penyakit (ID)","Penyakit (EN)"]
			disease_english = disease_english.drop_duplicates()
			disease_en = ", ".join(disease_english["Penyakit (EN)"].astype(str)).lower()
			disease_en = disease_en.replace("nan,","").replace(",nan","")
	
			disease_en = disease_en.strip()
			print("result",disease_en)


			# AND SET TO WIDGET
			resultDiagnose.value = disease_en
			page.update()


			# AFTER THAT THE SEARCH YOU DiSEASE TO WIKIPEDIA
			# FOR EXPLANATION AND DETAIL INFORMATION
			article = wikipedia.page(disease_en)

			# AND WRITE TO FILE AND SAVE TO youcase FOLDER
			# THEN YOU CAN SEE FILE .txt IN youcase FOLDER

			with open(f"youcase/{disease_indonesia}.txt","w") as file:
				file.write(article.content)

			# AND READ FILE txt AND PUSH TO WIDGET
			with open(f"youcase/{disease_indonesia}.txt","r") as file:
				explanation.value = file.read()
		page.update()





	diagnoseCon = Container(
		content=Column([
			Text("You Diagnostic",weight="bold",size=25),
			resultDiagnose,
			Divider(),
			Text("diagnose explanation",
				size=25,weight="bold"
				),
			explanation

			])

		)

	# AND GET PASTE FROM YOU CLIPBOARD INPUT TEXT 
	def getpaste(e):
		paste = page.get_clipboard()
		youInput.value = paste
		page.update()

	# SET DEFAULT TO HIDE FOR RESULT BECAUSE NO INPUT VALUE
	diagnoseCon.visible = False

	page.add(
		AppBar(
		title=Text("FLet doctor",size=30,color="white"),
		bgcolor="blue"
		),
		Column([
			Row([
				youInput,
				IconButton("copy",
					on_click=getpaste
					)

				]),
		ElevatedButton("diagnostic check",
			bgcolor="blue",color="white",
			on_click=diagnosenow

			),
		diagnoseCon


			])
		)

flet.app(target=main)
