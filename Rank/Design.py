import tkinter
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from Rank.Graph import *
from Rank.GraphConfig import *
from Rank.PowerMethod import *


class Design:
    def __init__(self):
        self.graph_to_plot = Graph([1, ["a", "b"], [("a", "b")]])
        self.root_widget = object()
        self.max_width_rank_text_box = 15

    @staticmethod
    def load_file(nodes_num_entry, nodes_text, edges_text, eps_entry):
        filename = tkinter.filedialog.askopenfilename(filetypes=(("Txt files", "*.txt"), ("All files", "*.*")))
        if filename:
            try:
                gc = GraphConfig()
                data = gc.data_to_fields(gc.read_from_file(filename))
                nodes_num_entry.delete(0, END)
                nodes_text.delete('1.0', END)
                edges_text.delete('1.0', END)
                eps_entry.delete(0, END)
                nodes_num_entry.insert(END, data[0])
                nodes_text.insert(END, data[1])
                edges_text.insert(END, data[2])
                eps_entry.insert(END, data[3])
            except FileNotFoundError:
                tkinter.messagebox.showerror("Open Source File", "Failed to read file \n'%s'" % filename)

    def generate_graph(self, nodes_num_entry, nodes_textbox, edges_textbox, eps_entry, nb_widget):
        try:
            nodes_num = int(nodes_num_entry.get())
            eps = int(eps_entry.get())
            if nodes_num < 1:
                tkinter.messagebox.showerror("Error", "Incorrect number of nodes parameter.")
                return
            if eps < 1:
                tkinter.messagebox.showerror("Error", "Incorrect epsilon parameter.")
                return
            eps = 10 ** -eps
            nodes = nodes_textbox.get('1.0', END)
            edges = edges_textbox.get('1.0', END)
            g_info = GraphConfig.data_proceed(nodes_num, nodes, edges)
            graph = Graph(g_info)
            self.graph_to_plot = graph
            list_of_frames = list(nb_widget.children.keys())
            self.tab2_setup(nb_widget.children[list_of_frames[1]], eps)
            nb_widget.tab(1, state=NORMAL)
            nb_widget.select(1)
        except ValueError:
            tkinter.messagebox.showerror("Error", "Incorrect number of nodes  or epsilon parameters.")
        except IndexError:
            tkinter.messagebox.showerror("Error", "It seems your graph is not defined properly.")

    def max_width_for_rank_textbox(self, ranks):
        for i in range(len(ranks)):
            if len(str(ranks[i])) > self.max_width_rank_text_box:
                self.max_width_rank_text_box = len(str(ranks[i]))
        return self.max_width_rank_text_box

    def print_ranks(self, graph, textbox):
        ranks = graph.page_ranks
        ranks_as_text = ""
        ranks_as_text_list = []
        for i in range(len(ranks)):
            value = str(graph.nodes[i]) + ": " + str(ranks[i])
            ranks_as_text_list.append(value)
            ranks_as_text += value + "\n"
        textbox.configure(state=NORMAL)
        textbox.delete('1.0', END)
        textbox.insert(END, ranks_as_text)
        textbox.configure(state=DISABLED)
        max_width = self.max_width_for_rank_textbox(ranks_as_text_list)
        textbox.configure(width=max_width + 1)
        return ranks_as_text

    @staticmethod
    def design_matrix(root_widget, mtr):
        matrix_form = Toplevel(root_widget)
        matrix_form.minsize(width=300, height=300)
        matrix_form.focus_set()
        matrix_form.wm_title("MATRIX")
        Grid.rowconfigure(matrix_form, 0, weight=1)
        Grid.columnconfigure(matrix_form, 0, weight=1)
        frame = Frame(matrix_form)
        frame.grid(row=0, column=0)
        for textbox in frame.grid_slaves():
            if int(textbox.grid_info()["row"]) >= 0:
                textbox.grid_forget()
        for row_ind in range(len(mtr)):
            for col_ind in range(len(mtr[row_ind])):
                new_textbox = Entry(frame)
                new_textbox.delete(0, END)
                new_textbox.insert(0, mtr[row_ind][col_ind])
                new_textbox.grid(row=row_ind, column=col_ind, sticky=N + E + W)
        ok_button = Button(frame, text="   OK   ", command=lambda: matrix_form.destroy())
        ok_button.grid(row=len(mtr) + 1, column=int(len(mtr) / 2))
        ok_button.focus_set()

    def tab1_setup(self, nb):
        list_of_tabs = list(nb.children.keys())
        tab1 = nb.children[list_of_tabs[0]]
        Grid.rowconfigure(tab1, 0, weight=1)
        Grid.columnconfigure(tab1, 0, weight=1)
        frame = Frame(tab1)
        frame.grid(row=0, column=0, sticky=N + S + E + W)
        panel_frame = Frame(frame)
        panel_frame.grid(row=0, column=0, sticky=N + S + E + W)
        nodes_edges_frame = Frame(frame)
        nodes_edges_frame.grid(row=1, column=0, sticky=N + S + E + W)
        Grid.rowconfigure(frame, 1, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        blank_text = "  "

        for col_index in range(9):
            for row_index in range(4):
                if row_index == 3:
                    Grid.rowconfigure(nodes_edges_frame, row_index, weight=1)
                if col_index == 1 or col_index == 5:
                    Grid.columnconfigure(nodes_edges_frame, col_index, weight=1)
                if (row_index % 2 == 0 and col_index == 0 and row_index != 2) \
                        or (col_index % 2 == 0 and row_index == 0 and col_index != 2):
                    blank_label = Label(nodes_edges_frame, text=blank_text)
                    blank_label.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                elif row_index == 1 and col_index == 1:
                    nodes_label = Label(nodes_edges_frame, text="List of nodes:")
                    nodes_label.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                elif row_index == 3 and col_index == 1:
                    y_scrollbar1 = Scrollbar(nodes_edges_frame)
                    nodes_textbox = Text(nodes_edges_frame, yscrollcommand=y_scrollbar1.set, wrap=WORD, width=10)
                    y_scrollbar1.config(command=nodes_textbox.yview)
                    y_scrollbar1.grid(row=row_index, column=col_index + 1, sticky=N + S + E + W)
                    nodes_textbox.grid(row=row_index, column=col_index, columnspan=1, sticky=N + S + E + W)
                elif row_index == 1 and col_index == 5:
                    edges_label = Label(nodes_edges_frame, text="List of edges:")
                    edges_label.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                elif row_index == 3 and col_index == 5:
                    y_scrollbar2 = Scrollbar(nodes_edges_frame)
                    edges_textbox = Text(nodes_edges_frame, yscrollcommand=y_scrollbar2.set, wrap=WORD, width=10)
                    y_scrollbar2.config(command=edges_textbox.yview)
                    y_scrollbar2.grid(row=row_index, column=col_index + 1, sticky=N + S + E + W)
                    edges_textbox.grid(row=row_index, column=col_index, columnspan=1, sticky=N + S + E + W)

        for col_index in range(12):
            for row_index in range(2):
                if (row_index % 2 == 0 and col_index == 0) or (col_index % 2 == 0 and row_index == 0):
                    blank_label = Label(panel_frame, text=blank_text)
                    blank_label.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                elif row_index == 1 and col_index == 1:
                    nodes_num_label = Label(panel_frame, text="Number of nodes:")
                    nodes_num_label.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                elif row_index == 1 and col_index == 3:
                    nodes_entry = Entry(panel_frame, width=5)
                    nodes_entry.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                elif row_index == 1 and col_index == 5:
                    eps_label = Label(panel_frame, text="ε = 10^-")
                    eps_label.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                elif row_index == 1 and col_index == 6:
                    eps_entry = Entry(panel_frame, width=5)
                    eps_entry.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                elif row_index == 1 and col_index == 9:
                    from_file_button = Button(panel_frame, text="LOAD FROM FILE",
                                              command=lambda: self.load_file(nodes_entry, nodes_textbox, edges_textbox,
                                                                             eps_entry))
                    from_file_button.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                elif row_index == 1 and col_index == 11:
                    run_button = Button(panel_frame, text="GENERATE GRAPH",
                                        command=lambda: self.generate_graph(nodes_entry, nodes_textbox, edges_textbox,
                                                                            eps_entry, nb))
                    run_button.grid(row=row_index, column=col_index, sticky=N + S + E + W)

    def tab2_setup(self, tab2, eps_value):
        for widget in tab2.winfo_children():
            widget.destroy()
        frame_for_canvas = Frame(tab2)
        frame_for_canvas.pack(side=TOP, fill=BOTH, expand=1)
        frame_for_toolbar = Frame(tab2)
        frame_for_toolbar.pack(anchor=W)
        f = Figure(figsize=(1, 1), dpi=100)
        a = f.add_subplot(111)
        gr_instance = self.graph_to_plot
        gr_instance.graph_build(a)
        canvas = FigureCanvasTkAgg(f, master=frame_for_canvas)
        canvas.show()
        canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, frame_for_toolbar)
        toolbar.update()
        canvas._tkcanvas.pack(side=LEFT, fill=BOTH, expand=1)

        def power_iter():
            old_ranks = gr_instance.page_ranks
            try:
                gr_instance.page_ranks = pm.power_method(mtr, old_ranks)
            except IndexError:
                tkinter.messagebox.showerror("Error", "It seems your graph is not defined properly.")
            iteration_num = pm.iteration
            new_ranks = gr_instance.page_ranks
            if pm.convergence(old_ranks, new_ranks) and not pm.is_final_iteration:
                final_ranks_text = self.print_ranks(gr_instance, textbox_with_ranks)
                pm.is_final_iteration = True
                final_rank_label.configure(text="Final iteration is " + str(pm.iteration) + "\n" + final_ranks_text)
            self.print_ranks(gr_instance, textbox_with_ranks)
            gr_instance.view_ranks(gr_instance.plot_params, new_ranks)
            canvas.draw()
            iter_label.configure(text="Iteration " + str(iteration_num))

        def find_final_rank():
            pm.iteration = 0
            pm.is_final_iteration = False
            gr_instance.page_ranks = gr_instance.set_start_rank(gr_instance.nodes_num)
            while True:
                try:
                    old_ranks = gr_instance.page_ranks
                    gr_instance.page_ranks = pm.power_method(mtr, old_ranks)
                    if pm.convergence(old_ranks, gr_instance.page_ranks):
                        break
                    if pm.iteration % 1000 == 0:
                        result = tkinter.messagebox.askyesno("Warning", "Iteration number is " + str(
                            pm.iteration) + ". Do you still want to continue with final rank?", icon='warning')
                        if not result:
                            break
                except IndexError:
                    tkinter.messagebox.showerror("Error", "It seems your graph is not defined properly.")
            pm.is_final_iteration = True
            iteration_num = pm.iteration
            final_ranks = gr_instance.page_ranks
            final_ranks_text = self.print_ranks(gr_instance, textbox_with_ranks)
            iter_label.configure(text="Iteration " + str(iteration_num))
            final_rank_label.configure(text="Final iteration is " + str(iteration_num) + "\n" + final_ranks_text)
            gr_instance.view_ranks(gr_instance.plot_params, final_ranks)
            canvas.draw()

        mtr = gr_instance.get_matrix(gr_instance.designed_graph)
        pm = PowerMethod(eps_value)
        frame = Frame(frame_for_canvas)
        frame.pack(anchor=W, pady=10, padx=5)
        frame.focus_set()
        blank_text = "   "
        textbox_with_ranks = Text(frame, height=gr_instance.nodes_num + 1, wrap=WORD)
        textbox_with_ranks.grid(row=1, column=0)
        for row_index in range(10):
            if row_index % 2 == 0 and row_index > 1:
                blank_label = Label(frame, text=blank_text)
                blank_label.grid(row=row_index, column=0, sticky=N + S + E + W)
            if row_index == 0:
                iter_label = Label(frame, text="Iteration 0")
                iter_label.grid(row=row_index, column=0, sticky=N + S + E + W)
            elif row_index == 3:
                button_iter = Button(master=frame, text='Iterate', command=lambda: power_iter())
                button_iter.grid(row=row_index, column=0)
                button_iter.focus_set()
            elif row_index == 5:
                button_matrix = Button(master=frame, text='Matrix',
                                       command=lambda: self.design_matrix(self.root_widget, mtr))
                button_matrix.grid(row=row_index, column=0)
            elif row_index == 7:
                button_final_rank = Button(master=frame, text='Final Rank', command=lambda: find_final_rank())
                button_final_rank.grid(row=row_index, column=0)
            elif row_index == 9:
                final_rank_label = Label(frame, text="", foreground="green")
                final_rank_label.grid(row=row_index, column=0, sticky=N + S + E + W)

        self.print_ranks(gr_instance, textbox_with_ranks)

    def design_function(self):
        matplotlib.use('TkAgg')
        root = Tk()
        root.wm_title("PAGE RANK")
        min_width = 500
        min_height = 500
        root.minsize(width=min_width, height=min_height)
        note = Notebook(root)
        note.grid(row=0, column=0, sticky=N + S + E + W)
        Grid.rowconfigure(root, 0, weight=1)
        Grid.columnconfigure(root, 0, weight=1)
        tab1 = Frame(note)
        tab2 = Frame(note)
        note.add(tab1, text="Configuration")
        note.add(tab2, text="Output")
        note.tab(1, state=DISABLED)
        self.root_widget = root
        self.tab1_setup(note)
        root.mainloop()
