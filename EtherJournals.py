import json, ast, requests
from tkinter import *
from tkinter import filedialog, messagebox
from web3.auto import w3, Web3

# Using a public node!
w = Web3(Web3.HTTPProvider
         ('https://ropsten.infura.io/v3/*****'))


class MainApp(Tk):

    def __init__(self):
        Tk.__init__(self)

        self._frame = None

        self.width = 500

        self.height = 500

        self.privkey = ""

        self.address = ""

        self.logo = PhotoImage(file="assets/StartPage.gif").subsample(2)

        self.encodeLogo = PhotoImage(file="assets/Encode.gif").subsample(2)

        self.enterDetailsLogo = PhotoImage(file="assets/EnterDetails.gif") \
            .subsample(2)

        self.decodeLogo = PhotoImage(file="assets/Decode.gif").subsample(2)

        self.exitLogo = PhotoImage(file="assets/exitIcon.gif")

        self.addButtonOriginal = PhotoImage(file="assets/addButton.gif") \
            .subsample(2)

        self.uploadImage = PhotoImage(file="assets/Upload.gif").subsample(2)

        self.geometry('%dx%d' % (self.width, self.height))

        self.switch_frame(StartPage)

    def switch_frame(self, frame_name):
        # Destroys current frame and replaces it with a new one.
        new_frame = frame_name(self)

        # Destroys the current frame
        if self._frame is not None:
            self._frame.destroy()

        # Creates the new frame
        self._frame = new_frame

        # Render the new frame
        self._frame.pack()


# Starting Page, first to be rendered, then it can be switched to other frames
# API Call format from https://etherscan.io/apis#contracts

"""
@Params: start_button, start_label, decode_button, encode_button
start_label:    The background image for Ether Journals
exit_button:    The button will exit the frames or exit the program
decode_button:  The button to switch to the decode frame
encode_button:  The button to switch to the encode frame
"""


class StartPage(Frame):
    def __init__(self, master):
        # Take in all the images from the parent class
        Frame.__init__(self, master)

        self.start_label = Label(master, image=master.logo)

        self.exit_button = Button(master, command=quit)

        self.exit_button.config(image=master.exitLogo)

        self.decode_button = Button(master, text="Decode Data", font="Arial 14",
                                    fg="white", bg="#42a5f5", command=
                                    lambda: master.switch_frame(DecodePage),
                                    borderwidth=0)

        self.encode_button = Button(master, text="Encode Data", font="Arial 14",
                                    fg="white", bg="#42a5f5", command=
                                    lambda: master.switch_frame(EnterVariables),
                                    borderwidth=0)

        # Places the buttons onto the frame
        self.start_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.exit_button.place(x=20, y=20)

        self.decode_button.place(x=20, y=455)

        self.encode_button.place(x=350, y=455)


"""
@Params:
txid:           The transaction ID to decode
decodeValid:    Boolean to check if the ID is legal to decode
apikey:         Etherscan API key
apiurl:         Etherscan API url header
decode_label:   Background for decode labels
enter_key:      Button to enter the information
exit_button:    Button to go back to the starting page
transactionID:  Entry for the transaction ID
"""


class DecodePage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.txid = ""

        self.decodeValid = False

        self.apikey = '*****'

        self.apiurl = 'http://ropsten.etherscan.io/api?'

        self.decode_label = Label(master, image=master.decodeLogo)

        self.enter_key = Button(master, text="Enter",
                                command=lambda: self.retrieveInput(self),
                                font="Arial 14", fg="white",
                                bg="#42a5f5", borderwidth=0)

        self.exit_button = Button(master,
                                  command=
                                  lambda: master.switch_frame(StartPage),
                                  font="Arial 14", borderwidth=0)

        self.exit_button.config(image=master.exitLogo)

        self.decode_button = Button(master, text="Decode Data",
                                    command=lambda:
                                    print(self.decodeTransaction()),
                                    font="Arial 14", bg="#42a5f5",
                                    fg="white", borderwidth=0)

        self.transactionID = Entry(master, borderwidth=0)

        self.decode_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.enter_key.place(x=310, y=390)

        self.transactionID.place(x=115, y=397)

        self.exit_button.place(x=20, y=20)

        self.decode_button.place(x=185, y=450)

    """
    It first makes sure the transactionID is valid
    Then it sets the @param decodeValid to true
    """

    def retrieveInput(master, self):

        master.txid = master.transactionID.get()

        # TXID is empty
        if master.txid == "":
            messagebox.showwarning("Warning", "Transaction ID is empty!")
            return

        # TXID always starts with 0x
        if not master.txid.startswith("0x"):
            messagebox.showwarning("Warning", "Transaction ID is invalid!")
            return

        messagebox.showinfo("Transaction Update",
                            "Transaction ID has been updated to \"%s\"" %
                            master.txid)
        # Transaction ID valid, set the boolean to True
        self.decodeValid = True

    def decodeTransaction(self):
        # Only run if we allow it to decode
        if self.decodeValid:

            null = 0  # Fixes entries where null is the value

            targeturl = '%smodule=proxy&action=eth_getTransactionByHash&' \
                        'txhash=%s&apikey=%s' % \
                        (self.apiurl, self.txid, self.apikey)

            reply = requests.get(targeturl)

            output = reply.json()

            try:
                encoded = output['result']['input']
            except:
                messagebox.showerror("Error",
                                     "There is no data within the transaction "
                                     "or the transaction ID is malformed")
                return

            # Returns bytes instead of text, allows raw data output
            decodedValue = w3.toBytes(hexstr=encoded)

            self.writeDataToFile(decodedValue)

        else:

            messagebox.showwarning("Warning",
                                   "Provide a valid transaction!")


    def writeDataType(self, dataNum):

        if dataNum == 1:
            return "txt"

        elif dataNum == 2:
            return "jpg"

        elif dataNum == 3:
            return "mp3"

        elif dataNum == 4:
            return "pdf"

        elif dataNum == 5:
            return "mp4"

        else:
            return "unknown"

    def writeDataToFile(self, decodeddata):

        transaction = json.loads(decodeddata)

        fileName = "%s by %s.%s" % (transaction['1'], transaction['4'],
                                    self.writeDataType(transaction['2']))

        file = open(fileName, "wb")

        # Only evaluate the literals
        byteTransaction = ast.literal_eval(transaction['3'])

        file.write(byteTransaction)

        file.close()

        messagebox.showinfo("Success!",
                            "%s has been written to the disk" % (fileName))
        return


class EnterVariables(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)

        self.enterVariables_label = Label(master, image=master.enterDetailsLogo)

        # This is the button to return to the starting page
        self.start_button = Button(master,
                                   command=
                                   lambda: master.switch_frame(StartPage),
                                   image=master.exitLogo)

        self.multiUseButton = Button(master,
                                     command=lambda: self.retrieveInput(self),
                                     borderwidth=0, bg="#4e8ee9",
                                     image=master.addButtonOriginal)

        self.privkey_entry = Entry(master, borderwidth=0)

        self.address_entry = Entry(master, borderwidth=0)

        self.enterVariables_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.start_button.place(x=20, y=20)

        self.address_entry.place(x=170, y=17)

        self.privkey_entry.place(x=170, y=59)

        self.multiUseButton.place(x=230, y=400)

    def retrieveInput(self, master):
        master.master.privkey = self.privkey_entry.get()

        master.master.address = self.address_entry.get()

        displayPriv = str(master.master.privkey)

        displayAddr = str(master.master.address)

        if len(displayAddr) < 40 or len(displayPriv) < 1:
            messagebox.showwarning("Invalid",
                                   "Invalid keys, please enter valid address"
                                   " and key, or else the program will not work"
                                   " as intended.")
            return
        messagebox.showinfo("Keys entered",
                            "Address: %s\nPrivate Key: %s" %
                            (displayAddr, displayPriv))

        # Switching to the EncodePage frame
        master.master.switch_frame(EncodePage)


class EncodePage(Frame):

    def __init__(self, master):

        Frame.__init__(self, master)

        self.apikey = '****'

        self.apiurl = 'http://ropsten.etherscan.io/api?'

        self.privkey = master.privkey

        self.address = master.address

        # In case if a user don't select anything
        self.directory = ""

        self.encode_label = Label(master, image=master.encodeLogo)

        # This is the button to return to the starting page
        self.start_button = Button(master,
                                   command=
                                   lambda: master.switch_frame(StartPage),
                                   image=master.exitLogo)

        self.multiUseButton = Button(master,
                                     command=lambda: self.addFile(master),
                                     borderwidth=0, bg="#4e8ee9",
                                     image=master.addButtonOriginal)

        # Creates the entries for author and title, if none, default values

        self.author_entry = Entry(master, borderwidth=0)

        self.title_entry = Entry(master, borderwidth=0)

        # Place the labels and buttons onto the board

        self.encode_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.start_button.place(x=20, y=20)

        self.multiUseButton.place(x=230, y=400)

        self.author_entry.place(x=170, y=17)

        self.title_entry.place(x=170, y=59)

    def addFile(self, master):

        self.setVariables()

        if len(self.directory) > 0:
            self.multiUseButton.configure(
                command=lambda: self.broadcast(master))

    def broadcast(self, master):
        try:
            self.basicTransaction(self.directory)

            self.multiUseButton.configure(command=lambda: self.addFile(master))

        except:
            messagebox.showwarning("Wrong Key/Address", "Please go back to "
                                                        "start and re-enter "
                                                        "your keys and "
                                                        "address!")
            master.switch_frame(StartPage)

    def setVariables(self):

        self.directory = \
            filedialog.askopenfilename(title="Select file",
                                       filetypes=(("text files", "*.txt"),
                                                  ("jpeg files", "*.jpg"),
                                                  ("video files", "*.mp4"),
                                                  ("PDF Document", "*.pdf"),
                                                  ("audio files", "*.mp3")))

        # Set the default @params for author and title
        # since the modules are required
        self.author = "Anonymous"

        self.title = "Untitled"

        tempAuthor = self.author_entry.get()

        tempTitle = self.title_entry.get()

        if len(tempAuthor) > 0:
            self.author = tempAuthor

        if len(tempTitle) > 0:
            self.title = tempTitle

        if len(self.directory) <= 1:
            messagebox.showwarning("No file", "No file chosen!")
            return

        messagebox.showinfo("Info", "Author: %s\nTitle: %s\nFile: %s" %
                            (self.author, self.title, self.directory))

        messagebox.showinfo("Broadcast",
                            "Broadcast the transaction by hitting the button"
                            " again!")

    """
    Nonce is the transaction sequence
    of the account, having Nonce ensures
    an attacker cannot copy the transaction
    hex and rebroadcast it to the network
    """

    def getNonce(self):
        return w.eth.getTransactionCount(self.address)

    # getDataType can be programmed to add in data types in the future, and it
    # is also backwards compatible

    def getDataType(self):

        if self.directory.endswith(".txt"):
            return 1

        if self.directory.endswith(".jpg"):
            return 2

        if self.directory.endswith(".mp3"):
            return 3

        if self.directory.endswith(".pdf"):
            return 4

        if self.directory.endswith(".mp4"):
            return 5

    def generateTransaction(self, dataToEncode):

        """
        Basic values:
        'value': 10 ** 11
        'chainId': 3
        """
        finalData = dict()

        finalData[1] = self.title

        finalData[2] = self.getDataType()

        finalData[3] = dataToEncode

        finalData[4] = self.author

        finalData = json.dumps(finalData)

        finalData = str.encode(finalData)

        transaction = {
            'to': '****',
            'value': 10**18,
            'nonce': self.getNonce(),
            # Gas value and price stable on Ropsten
            'gas': int(4.7 * 10 ** 6),
            'gasPrice': 10 ** 9,
            'data': finalData,
            'chainId': 3
        }

        return transaction

    """
    Broadcasts the transaction onto
    the Ropsten Ethereum chain
    """

    def broadcastTransaction(self, transaction):

        signed = w.eth.account.signTransaction(transaction, self.privkey)

        transaction_id = w.eth.sendRawTransaction(signed.rawTransaction)

        # Returns the hex id instead of the raw id for readability
        return transaction_id.hex()

    # Creates the transaction and prints out the TXID
    def basicTransaction(self, directory):

        if directory == "":
            messagebox.showerror("Error","No file selected")
            return

        with open(directory, 'rb') as info:
            data = info.read()
            data = str(data)

        transaction = self.generateTransaction(data)

        result = self.broadcastTransaction(transaction)
        messagebox.showinfo\
            ("Success!", "Transaction broadcasted to %s" % result)
        super().clipboard_clear()
        super().clipboard_append(result)
        messagebox.showinfo("Copied", "TXID copied to clipboard")


# Runs the main app.
if __name__ == "__main__":
    app = MainApp()

    app.wm_title("Ether Journals Alpha")

    app.mainloop()
