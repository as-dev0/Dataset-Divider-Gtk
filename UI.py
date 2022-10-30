import time
import matplotlib
import matplotlib.pyplot as plt
import gi 

from Graph import divided_dataset as divided_dataset
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk 

matplotlib.use('GTK3Agg')  # or 'GTK3Cairo'

graphs = {}

class DatasetDivider(Gtk.Window):

    def __init__(self):

        super().__init__(title="Dataset Divider")
        self.set_size_request(300,200)
        self.set_border_width(20)
        self.connect("destroy", Gtk.main_quit)

        self.selectGraphOne = Gtk.Button(label="Select first data set")
        self.selectGraphOne.connect("clicked", self.clickGraphOne)

        self.selectGraphTwo = Gtk.Button(label="Select second data set")
        self.selectGraphTwo.connect("clicked", self.clickGraphTwo)

        self.labelOne = Gtk.Label(label="                     ")
        self.labelTwo = Gtk.Label(label="                     ")

        self.displayGraph =  Gtk.Button(label="Display graph")
        self.displayGraph.connect("clicked", self.plot)

        self.resetButton = Gtk.Button(label="Reset")
        self.resetButton.connect("clicked", self.reset)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        vbox.add(self.selectGraphOne)
        vbox.add(self.labelOne)
        vbox.add(self.selectGraphTwo)
        vbox.add(self.labelTwo)
        vbox.add(self.displayGraph)
        vbox.add(self.resetButton)

        self.add(vbox)

    # Takes a string, and returns the string with the / symbol removed
    def removeSlash(self, s):
        
        if s.find("/") != -1:

            s = s[::-1]
            a = s[0:s.index("/")]
            a = a[::-1]
            return a

    # Takes a string (a filename), and returns the string with the extension removed
    def removeExtension(self, s):
        return s[0:s.index(".")]

    # This function is run when the user click on "Select first data set"
    # It retrieves the name of the file that the user clicks on
    def clickGraphOne(self, widget):
        global graphs

        dialog = Gtk.FileChooserDialog(title="Choose a file", action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK)
        dialog.set_current_folder('./csv')

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

            if filename != () and filename != None:
                newfile = self.removeSlash(filename)
                print("File selected: " + newfile)
                if newfile != None:
                    graphs[0] = newfile
                    self.labelOne.set_text(self.removeExtension(graphs[0]))
                    
            print("click1")
            
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    # This function is run when the user click on "Select second data set"
    # It retrieves the name of the file that the user clicks on
    def clickGraphTwo(self, widget):
        global graphs

        dialog = Gtk.FileChooserDialog(title="Choose a file", action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK)
        dialog.set_current_folder('./csv')

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

            if filename != () and filename != None:
                newfile = self.removeSlash(filename)
                print("File selected: " + newfile)

                if newfile != None:
                    graphs[1] = newfile
                    self.labelTwo.set_text(self.removeExtension(graphs[1]))

            print("click2")

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    # This function is run when the user click on the "Display graph"
    # It displays the graph of the data set obtained from dividing the first
    # data set by the second data set
    def plot(self, widget):

        startTime = time.time_ns()
        
        if len(graphs.keys()) == 2:
            last = graphs[1]
            first = graphs[0]
        else:
            print("You have not selected two graphs!")
            return


        # Obtaining the data
        # ------------------------------------------------------------------
        startTimeData = time.time_ns()
        
        data = divided_dataset(first,last)
        x = data[0]
        y = data[1]
            
        timeTakenData = (time.time_ns() - startTimeData)/1000000000
        print("Total time taken in seconds to obtain data = " + str(timeTakenData))
        # ------------------------------------------------------------------


        # Setting up the graph
        # ------------------------------------------------------------------
        startTimePlot = time.time_ns()
        
        # This figure will contain the plot
        fig, ax = plt.subplots()
        
        ax.plot(x,y)

        ax.set_ylabel(self.removeExtension(first) + "/" + self.removeExtension(last), color = "red", fontsize=14)
        ax.set_xlabel("Dates")

        # Selecting the dates to be shown on the x axis
        dates = []
        counter = 0
        for i in x:
            if counter % (len(y)//8) == 0:
                dates.append(str(i))
            counter += 1

        # Setting the dates on the x axis
        ax.set_xticks(dates)
        fig.set_figwidth(20)
        fig.set_figheight(10)
        timeTaken = (time.time_ns() - startTime)/1000000000
        print("Total time taken in seconds to run plot() = " + str(timeTaken))
        print("plot")
        plt.show()

    # This function is run when the user click on "Reset"
    # It removes the graph and resets the names of the files selected
    def reset(self, widget):

        global graphs

        graphs = {}

        self.labelOne.set_text("")
        self.labelTwo.set_text("")
        plt.close()
            
        print("reset")


win = DatasetDivider()
win.show_all()
Gtk.main()