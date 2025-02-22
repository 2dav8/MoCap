from mocap_bridge.readers.natnet_reader import NatnetReader

import sys
if sys.version_info[0] >= 3:
    import tkinter as tk
else:
    import Tkinter as tk
    

class NatnetReaderView:
    def __init__(self, natnet_reader=None, parent=None, manager=None):
        self.reader = natnet_reader
        self.parent = parent
        self.manager = manager

        if self.reader == None:
            self.reader = NatnetReader(manager=self.manager)

        self.setup()

    def setup(self):
        # create gui-elements
        self.frame = tk.LabelFrame(self.parent, text='NatNet', padx=10, pady=10)
        self.frame.grid()

        self.host_label = tk.Label(self.frame, text="Natnet Host")
        self.host_entry = tk.Entry(self.frame, width=10)
        self.multicast_label = tk.Label(self.frame, text="Multicast IP")
        self.multicast_entry = tk.Entry(self.frame, width=10)
        self.port_label = tk.Label(self.frame, text="Port")
        self.port_entry = tk.Entry(self.frame, width=5)
        self.connect_button = tk.Button(self.frame, text='(re-)connect', command=self.onConnectButton)
        self.disconnect_button = tk.Button(self.frame, text='disconnect', command=self.onDisconnectButton)
        self.status_label = tk.Label(self.frame, text='')

        # position elements
        self.host_label.grid(column=0, row=0)
        self.host_entry.grid(column=1, row=0)
        self.multicast_label.grid(column=2, row=0)
        self.multicast_entry.grid(column=3, row=0)
        self.port_label.grid(column=4, row=0)
        self.port_entry.grid(column=5, row=0)
        self.connect_button.grid(column=6, row=0)
        self.disconnect_button.grid(column=7, row=0)
        self.status_label.grid(column=0, row=1, columnspan=8)

        # initialize
        if self.reader:
            self.host_entry.insert(0, self.reader.host)
            if self.reader.multicast: self.multicast_entry.insert(0, str(self.reader.multicast))
            self.port_entry.insert(0, self.reader.port)

            self.reader.connectEvent += self.onConnect
            self.reader.connectionLostEvent += self.onDisconnect
            self.reader.connectionStatusUpdateEvent += self.onConnectionStatusUpdate

            self.updateStatus(self.reader)

    #     self.update()
    #
    # def update(self):
    #     timeValue = str(self.json_reader.getTime())
    #     self.time_value_label.configure(text=timeValue)
    #     self.parent.after(1, self.update) # schedule next update (tkinter doesn't seem to provide a nice way to do every-iteration-updates)

    def destroy(self):
        self.frame.grid_forget()

    def onConnectButton(self):
        self.reader.stop()
        self.reader.configure(host=self.host_entry.get(), port=self.port_entry.get(), multicast=self.multicast_entry.get())
        self.reader.start()

    def onDisconnectButton(self):
        self.reader.stop()

    def onConnect(self, reader):
        self.updateStatus(reader)

    def onDisconnect(self, reader):
        self.updateStatus(reader)

    def onConnectionStatusUpdate(self, reader):
        self.updateStatus(reader)

    def updateStatus(self, reader):
        if reader.connected == False:
            self.status_label.config(text='Disconnected')
            return

        if reader.connection_status != None:
            self.status_label.config(text=self.connectionInfo(reader) + '-' + reader.connection_status)
            return

        self.status_label.config(text=self.connectionInfo(reader))

    def connectionInfo(self, reader):
        if reader.multicast:
            return 'Connected to '+str(reader.host)+'@'+str(reader.port)+' ('+reader.multicast+')'

        return 'Connected to '+str(reader.host)+'@'+str(reader.port)
