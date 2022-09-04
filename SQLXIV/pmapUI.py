import tkinter as tk


def main():
	input_pmap()

def input_pmap():

	def button_click():
		print(Row1)

	root = tk.Tk()
	root.title("Enter potency map")
	root.geometry("700x500")

	entry = tk.Entry(root)
	label = tk.Label(root, text='Potency')
	label.grid(row=0, column=1, pady=5, padx=5)
	entry.grid(row=1, column=1, pady=5, padx=5)

	labels = ['']


	Row1 = []
	for x in range(5):
		entry = tk.Entry(root)
		entry.grid(row=2, column=x, pady=5, padx=5)
		Row1.append(entry)

	

	button = tk.Button(root, text="Submit", command=button_click)
	button.grid(row=7, column=2, pady=20)



	root.mainloop()


if __name__ == '__main__':
	main()