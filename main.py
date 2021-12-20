import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from bin.text_process import TextProcessing

nama = "Agus Kuncoro"
nim = "2516897"
judul = "Identifikasi Word Sense Disambiguation (WSD) Pada Kalimat Berbahasa Indonesia Menggunakan Metode N-Gram Dan Cosine Similarity"
logo = Image.open('img/logo.png')
resize_logo = logo.resize((250, 200))


class MyApp(tk.Tk):
	
	def __init__(self):
		super().__init__()
		self.title("Penguji Tingkat Ambigu")
		self.list_kalimat = []
	
		window_width = 800
		window_height = 550

		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()

		center_x = int(screen_width/2 - window_width/2)
		center_y = int(screen_height/2 - window_height/2)
		
		self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

		self.headerWidget()
		
		self.mainFrame()
		

	def headerWidget(self):
		header_frame = ttk.Frame(self)
		header_frame.pack(fill='x', pady=10)
		
		# Frame nama
		name_frame = ttk.Frame(header_frame)
		name_frame.pack(fill='x')
		name1 = ttk.Label(name_frame, text="Nama", font=(14), width=5)
		name1.pack(padx=10, side='left', anchor='w')
		name2 = ttk.Label(name_frame, text=":", font=(14), width=2)
		name2.pack(side='left')
		name3 = ttk.Label(name_frame, text=nama, font=(14))
		name3.pack(anchor='w')

		# Frame NIM
		nim_frame = ttk.Frame(header_frame)
		nim_frame.pack(fill='x')
		nim1 = ttk.Label(nim_frame, text="NIM", font=(14), width=5)
		nim1.pack(padx=10, side='left', anchor='w')
		nim2 = ttk.Label(nim_frame, text=":", font=(14), width=2)
		nim2.pack(side='left')
		nim3 = ttk.Label(nim_frame, text=nim, font=(14))
		nim3.pack(anchor='w')

		# Judul

		title = tk.Label(header_frame, text=judul, font=("Helvetica", 18), wraplength= 670 )
		title.pack(pady=25, expand=True)

	def mainFrame(self):
		frame = ttk.Frame(self)
		frame.pack(
			fill='both',
			expand=True
			)
		logo_frame =ttk.Frame(frame)
		logo_frame.pack(
			fill= 'both',
			expand = True
			)
		logo_img = ImageTk.PhotoImage(resize_logo)	
		logo_label = tk.Label(
			logo_frame,
			image = logo_img
			)
		logo_label.image = logo_img
		logo_label.pack(expand=True)

		button_frame =ttk.Frame(frame)
		button_frame.pack(
			expand = True
			)
		next_button = ttk.Button(button_frame, 
			text='Identifikasi',
			command=lambda:(frame.pack_forget(), self.prosesFrame()),
			)
		next_button.pack(ipadx=50, ipady=10, pady=8, expand=True)

	def prosesFrame(self):
		frame = ttk.Frame(self)
		frame.pack(
			fill='both',
			expand=True
			)
		button_frame=ttk.Frame(frame)
		button_frame.pack(
			fill = 'x',
			pady = 10,
			padx = 70,
			)
		browse_file_button = ttk.Button(button_frame, 
			text="Select File",
			command = lambda: self.browseFile(),
			)
		browse_file_button.pack(side='left', ipadx=20, ipady=10, anchor='w')

		self.proses_button = ttk.Button(button_frame, 
			text="Proses",
			command = lambda: self.prosesFile(),
			)
		self.proses_button['state'] = "disabled"
		self.proses_button.pack(anchor='e', ipadx=20, ipady=10)


		result_frame=tk.Frame(frame)
		result_frame.pack(
			fill='both',
			padx=70,
			pady=10,
			expand= True
			)
		result_list_kalimat_frame = tk.Frame(result_frame)
		result_list_kalimat_frame.pack(
			side='left',
			fill='both',
			expand=True,
			
			)
		result_list_arti_frame = tk.Frame(result_frame)
		result_list_arti_frame.pack(
			expand=True,
			fill='both',
			side='right',
			padx=15
			)

		self.result_list_kalimat = self.createListBox(result_list_kalimat_frame)


		self.result_list_arti = self.createTreeView(result_list_arti_frame)
		
	def createListBox(self, container):
		frame1 = ttk.Frame(container)
		frame1.pack(
			fill='both',
			expand=True
			)
		create_listbox = tk.Listbox(frame1,
			)
		create_listbox.pack(fill='both', side='left', expand=True)
		vertical_scrollbar = ttk.Scrollbar(frame1, 
			orient= 'vertical', 
			command= create_listbox.yview,
			)
		vertical_scrollbar.pack(anchor='e', fill='y', expand=True)
		frame2 = ttk.Frame(container)
		frame2.pack(fill='x')
		
		create_listbox['yscrollcommand'] =vertical_scrollbar.set

		horizontal_scrollbar = ttk.Scrollbar(frame2, 
			orient= 'horizontal', 
			command= create_listbox.xview,
			)
		horizontal_scrollbar.pack(fill='x', expand=True)
		create_listbox['xscrollcommand'] = horizontal_scrollbar.set

		return create_listbox

	def createTreeView(self, container):
		frame1 = ttk.Frame(container)
		frame1.pack(
			fill='both',
			expand=True)
		
		columns = ('input_kalimat',
			'ambigu_word',
			'type',
			'sense',
			'similarity'
			)
		create_tree = ttk.Treeview(frame1,
			columns= columns,
			show='headings',
			)
		create_tree.column('input_kalimat')
		create_tree.column('ambigu_word', anchor='center', width=100)
		create_tree.column('type', anchor='center', width=100)
		create_tree.column('sense')
		create_tree.column('similarity', anchor='center', width=60)

		create_tree.heading('input_kalimat', text="Kalimat")
		create_tree.heading('ambigu_word', text="Kata Ambigu")
		create_tree.heading('type', text="Type Kata")
		create_tree.heading('sense', text="Makna Kata")
		create_tree.heading('similarity', text="Kemiripan")

		create_tree.pack(side='left', fill="both", expand=True, anchor='e')
		vertical_scrollbar = ttk.Scrollbar(frame1, 
			orient= 'vertical', 
			command= create_tree.yview,
			)
		vertical_scrollbar.pack(expand=True, fill='y', anchor='e')
		frame2 = ttk.Frame(container)
		frame2.pack(fill='x')
		
		create_tree['yscrollcommand'] =vertical_scrollbar.set

		horizontal_scrollbar = ttk.Scrollbar(frame2, 
			orient= 'horizontal', 
			command= create_tree.xview,
			)
		horizontal_scrollbar.pack(expand=True, fill='x', anchor='e')
		create_tree['xscrollcommand'] = horizontal_scrollbar.set

		return create_tree

	def browseFile(self):
		try:
			self.file_name = askopenfilename()
			self.data = TextProcessing(self.file_name)
			self.list_kalimat = self.data.showList()
			self.proses_button['state'] = "normal"
			# delete list box
			self.result_list_kalimat.delete(0, tk.END)
			
			# delete treeview
			for item in self.result_list_arti.get_children() :
				self.result_list_arti.delete(item)
			
				
			x=0
			for kalimat in self.list_kalimat:
				self.result_list_kalimat.insert(x, kalimat)
				x+=1
		except:
			print("File not found")
			
	def prosesFile(self):
		result = self.data.wordProses()
		self.proses_button['state'] = "disabled"
		for li in result:
			self.result_list_arti.insert('', tk.END, values=(
					self.list_kalimat[li['id_kalimat']],
					li['kata'],
					li['tipe'][0],
					li['arti'][0],
					li['result'][0]
					))
			if len(li['tipe'])>1:
				for i in range(1,len(li['tipe'])):
					self.result_list_arti.insert('', tk.END, values=(
						'',
						'',
						li['tipe'][i],
						li['arti'][i],
						li['result'][i]
						))

				


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()